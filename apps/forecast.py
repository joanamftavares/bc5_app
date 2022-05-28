import streamlit as st
from datetime import date
import pandas as pd

import yfinance as yf
from plotly import graph_objs as go
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from numpy import array

import tensorflow as tf
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import LSTM
from keras.models import model_from_json


def app():
    START = "2019-05-05"
    # current date
    TODAY = date.today().strftime("%Y-%m-%d")

    # create APP
    # APP title
    st.title("Stock Prediction")

    stock = st.text_input('Enter stock or crytocurrency', 'BTC-USD')
    st.write('The current stock  is', stock)
    st.info('Not sure about the symbol of the stock or crypto you are looking for? Check this [link](https://finance.yahoo.com/) to find out the available tickers')
    st.sidebar.header("Features")
    st.sidebar.markdown("Drag the sliders")

    row = st.sidebar.slider("Display Records:", 0, 100, 50)

    # cache the data of the stock we choose and doesn't have to run the code below again
    @st.cache(suppress_st_warning=True)
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        return data

    data_load_state = st.text("Load data...")
    data = load_data(stock)
    data_load_state.text("Loading data... done!")

    st.subheader('Raw data')
    st.write(data.tail(row))

    # DAILY PERCENTAGE CHANGE
    daily_price = data['Close']
    dpchange = daily_price / (daily_price.shift(1) - 1)
    dpchange = pd.DataFrame(dpchange)

    col1, col2 = st.columns(2)

    with col1:
        def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Open'], name='stock_open'))
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='stock_close'))
            fig.layout.update(title_text='Price Variation', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)

        plot_raw_data()

    with col2:
        def plot_dpc_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dpchange.index, y=dpchange['Close'], name='stock_close'))
            fig.layout.update(title_text='Daily Percentage change', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)

        plot_dpc_data()

    # PREDICTIONS

    col1, col2 = st.columns(2)

    with col1:
        row1 = st.sidebar.slider("Days for close price prediction:", 0, 10, 2)

        st.subheader('Forecast data')
        st.write('Loading Predicted Data...')

        def pred(data):
            scaler_1 = MinMaxScaler()

            def create_dataset(dataset, time_step=1):
                dataX, dataY = [], []
                for i in range(len(dataset) - time_step - 1):
                    a = dataset[i:(i + time_step), 0]
                    dataX.append(a)
                    dataY.append(dataset[i + time_step, 0])
                return np.array(dataX), np.array(dataY)

            closedf = data[['Close']]
            closedf = scaler_1.fit_transform(np.array(closedf).reshape(-1, 1))

            training_size = int(len(closedf) * 0.80)
            test_size = len(closedf) - training_size
            train_data, test_data = closedf[0:training_size, :], closedf[training_size:len(closedf), :1]

            time_step = 15
            X_train, y_train = create_dataset(train_data, time_step)
            X_test, y_test = create_dataset(test_data, time_step)

            X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
            X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

            # model=Sequential()
            # model.add(LSTM(10,input_shape=(None,1),activation="relu"))
            # model.add(Dense(1))
            # model.compile(loss="mean_squared_error",optimizer="adam")

            # model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=200,batch_size=32,verbose=1)

            # model_json = model.to_json()
            # with open("model.json", "w") as json_file:
            #    json_file.write(model_json)
            # serialize weights to HDF5
            # model.save_weights("model.h5")
            json_file = open('model.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            # load weights into new model
            loaded_model.load_weights("model.h5")

            train_predict = loaded_model.predict(X_train)
            test_predict = loaded_model.predict(X_test)

            train_predict = scaler_1.inverse_transform(train_predict)
            test_predict = scaler_1.inverse_transform(test_predict)
            original_ytrain = scaler_1.inverse_transform(y_train.reshape(-1, 1))
            original_ytest = scaler_1.inverse_transform(y_test.reshape(-1, 1))

            x_input = test_data[len(test_data) - time_step:].reshape(1, -1)
            temp_input = list(x_input)
            temp_input = temp_input[0].tolist()

            lst_output = []
            n_steps = time_step
            i = 0
            pred_days = row1
            while (i < pred_days):

                if (len(temp_input) > time_step):

                    x_input = np.array(temp_input[1:])
                    # print("{} day input {}".format(i,x_input))
                    x_input = x_input.reshape(1, -1)
                    x_input = x_input.reshape((1, n_steps, 1))

                    yhat = loaded_model.predict(x_input, verbose=0)
                    # print("{} day output {}".format(i,yhat))
                    temp_input.extend(yhat[0].tolist())
                    temp_input = temp_input[1:]
                    lst_output.extend(yhat.tolist())
                    i = i + 1

                else:

                    x_input = x_input.reshape((1, n_steps, 1))
                    yhat = loaded_model.predict(x_input, verbose=0)
                    temp_input.extend(yhat[0].tolist())

                    lst_output.extend(yhat.tolist())
                    i = i + 1

            last_days = np.arange(1, time_step + 1)
            day_pred = np.arange(time_step + 1, time_step + pred_days + 1)

            temp_mat = np.empty((len(last_days) + pred_days + 1, 1))

            temp_mat[:] = np.nan
            temp_mat = temp_mat.reshape(1, -1).tolist()[0]

            last_original_days = temp_mat
            next_predicted_days = temp_mat

            last_original_days[0:time_step + 1] = \
            scaler_1.inverse_transform(closedf[len(closedf) - time_step:]).reshape(1, -1).tolist()[0]
            next_predicted_days[time_step:] = \
            scaler_1.inverse_transform(np.array(lst_output).reshape(-1, 1)).reshape(1, -1).tolist()[0]

            new_pred_plot = pd.DataFrame({
                'last_original_days': last_original_days,
                'next_predicted_days': next_predicted_days
            })
            return new_pred_plot

        pred_data = pred(data)

        def plot_table_data():
            new_table = pred_data
            new_table['Date'] = pd.date_range(start=data.index[-15], periods=15 + row1, freq='D')
            new_table = new_table.set_index('Date')
            new_table = new_table.drop('next_predicted_days', axis=1)
            new_table = new_table.rename(columns={"last_original_days": "Close Price Prediction"})
            return new_table

        forecast_data = plot_table_data()
        st.write(forecast_data.tail(row1))

        month = forecast_data.index[-1].strftime("%B")
        day = forecast_data.index[-1].day
        year = forecast_data.index[-1].year
        date_forecast = str(str(month) + " " + str(day) + ", " + str(year))
        delta = ((forecast_data.iloc[-1, :] - forecast_data.iloc[14, :]) / forecast_data.iloc[-1, :]) * 100
        st.metric(label="Predicted Price for " + date_forecast, value=str(round(forecast_data.iloc[-1, 0], 2)) + " €",
                  delta=str(round(delta[0], 2)) + " %")

    with col2:

        def plot_pred_data():
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=forecast_data.iloc[0:16].index, y=forecast_data.iloc[0:-1, 0],
                                      name='Last 15 days close price', line_color='#8D539B'))
            fig1.add_trace(go.Scatter(x=forecast_data.iloc[15:].index, y=forecast_data.iloc[-row1:, 0],
                                      name='Predicted next days close price', line=dict(color='blue')))
            fig1.update_layout(width=800)
            fig1.layout.update(title_text='Close Price Prediction', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig1)

        plot_pred_data()




