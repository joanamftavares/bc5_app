from turtle import color
import streamlit as st
import datetime
from datetime import date
from datetime import timedelta
import pandas as pd

import yfinance as yf
from plotly import graph_objs as go
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from numpy import array
from streamlit_tags import st_tags
import plotly.express as px
from pandas_datareader import data as pdr


def app():
    st.title("Portfolio")

    START = "2021-05-25"
    # current date
    TODAY = date.today().strftime("%Y-%m-%d")

    @st.cache(suppress_st_warning=True)
    @st.cache(allow_output_mutation=True)
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        # data.reset_index(inplace=True)
        return data

    keywords = st_tags(
        label='Enter Keywords:',
        text='Press enter to add more',
        value=['BTC-USD'],
        maxtags=8,
        key='1')

    d = st.sidebar.date_input(
        "Enter Acquisition Date",
        datetime.date(2019, 7, 6))
    unit_cost = st.sidebar.number_input('Enter stock unitary cost (USD)', 0)
    quantity = st.sidebar.slider("Quantity:", 0, 100, 10)

    @st.cache(allow_output_mutation=True)
    def get_data():
        return []

    if st.sidebar.button("Add info for analysis"):
        get_data().append({"Acquisition Date": d, "Unitary_cost": unit_cost, "quantity": quantity})

    port_list = []
    index_list = []
    risk_list = []
    mon_ret = []
    for stock in keywords:
        data = load_data(stock)
        change = (data['Close'][len(data) - 1] - data['Close'][len(data) - 2])
        perc_change = ((data['Close'][len(data) - 1] - data['Close'][len(data) - 2]) / data['Close'][len(data) - 1])
        last_close = data['Close'][len(data) - 1]
        stock_name = yf.Ticker(stock)
        if stock.endswith('USD'):
            category = 'Cryptocurrency'
            volume = data['Volume'][len(data) - 1]
        else:
            category = stock_name.info['sector']
            volume = stock_name.info['volume']
        # monthly_returns = pd.DataFrame(data['Adj Close'].resample('M').ffill().pct_change()).iloc[:,0].to_list()
        info_list = [last_close, change, perc_change, category, volume]
        port_list.append(info_list)
        index_list.append(stock)
        # mon_ret.append(monthly_returns)

        # Calculate stock risk
        # Compute the returns of the stock
        df2 = data.copy()
        df2['Returns'] = df2['Adj Close'].pct_change()

        # Compute the standard deviation of the returns using standard deviation
        daily_sd_itc = df2['Returns'].std()

        # Annualized standard deviation
        # convert the daily volatilities to annual volatilities by multiplying with the square root of 252 (the number of trading days in a year)
        annual_sd_itc = daily_sd_itc * np.sqrt(252)
        risk_list.append(annual_sd_itc)

    def color_negative_red(value):
        if value < 0:
            color = 'red'
        elif value > 0:
            color = 'green'
        else:
            color = 'black'
        return 'color: %s' % color

    chart = pd.DataFrame(port_list, columns=['Last Close Price', 'Change', '% Change', 'Category', 'Volume'],
                         index=index_list)
    # TABLE
    st.dataframe(chart.style.applymap(color_negative_red, subset=['Change', '% Change'])
                 .format({'% Change': "{:.2%}", "Change'": "{:.4}"}))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('#### Portfolio Diversity')
        diversity = chart.groupby(by=["Category"]).agg({"Category": "count"})
        fig = px.pie(diversity, values='Category', names=diversity.index,
                     color_discrete_sequence=px.colors.sequential.Viridis)
        fig.update_layout(width=400, height=400)
        st.plotly_chart(fig)

    ## RISK GRAPHIC
    with col2:
        st.markdown('#### Risk Profile')
        avg_risk = sum(risk_list) / len(risk_list)
        fig_risk = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_risk,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [None, 1]},
                   'steps': [
                       {'range': [0, 0.2], 'color': "#E6E1E1"},
                       {'range': [0.2, 0.6], 'color': "lightgray"},
                       {'range': [0.6, 1], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))

        if (avg_risk < 0.20):
            risk_value = "Low risk"
        elif (avg_risk >= 0.20) & (avg_risk < 0.60):
            risk_value = "Moderate risk"
        else:
            risk_value = "High risk"

        fig_risk.add_annotation(x=0.5, y=0.55, text=risk_value, font=dict(color="white"), showarrow=False)
        fig_risk.update_layout(width=400, height=400)
        st.plotly_chart(fig_risk)

    with col3:

        # RETURNS GRAPHIC
        info_port = pd.DataFrame(get_data())
        info_port['Ticker'] = keywords

        tickers = keywords

        def get(tickers, startdate, enddate):
            def data(ticker):
                return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))

            datas = map(data, tickers)
            return (pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))

        def return_graph():
            st.markdown('#### Total Return - Annual Performance')

            stocks_end = date.today() - timedelta(days=1)
            stocks_start = "2021-05-25"
            all_data = get(tickers, stocks_start, stocks_end)
            all_data = all_data.reset_index()
            all_data = all_data.rename(columns={all_data.columns[0]: 'Ticker', all_data.columns[1]: 'Date'})
            all_data = all_data.set_index('Date')

            end_of_last_year = "2021-05-27"
            adj_close = all_data[['Adj Close', 'Ticker']].reset_index()

            # Grabbing the ticker close from the end of last year
            adj_close_start = adj_close[adj_close['Date'] == end_of_last_year]

            # Grab the latest stock close price
            # today= str(date.today())
            # stocks_end = datetime.datetime.strptime(today, "yyyy'-'MM'-'dd'T'HH':'mm':'ss")
            stocks_end = '2021-05-28T00:00:00'
            adj_close_latest = adj_close[adj_close['Date'] == stocks_end]
            adj_close_latest.set_index('Ticker', inplace=True)

            # Set portfolio index prior to merging with the adj close latest.
            info_port.set_index(['Ticker'], inplace=True)

            # Merge the information portfolio dataframe with the adj close dataframe
            merged_portfolio = pd.merge(info_port, adj_close_latest, left_index=True, right_index=True)

            # create new column - ticker return
            # ticker return is the result from the division between the last adjusted close price and the correspondent share cost
            merged_portfolio['ticker return'] = merged_portfolio['Adj Close'] / merged_portfolio['Unitary_cost'] - 1
            merged_portfolio.reset_index(inplace=True)

            info_port.reset_index(inplace=True)
            adj_close_acq_date = pd.merge(adj_close, info_port, on='Ticker')
            del adj_close_acq_date['quantity']
            del adj_close_acq_date['Unitary_cost']
            adj_close_acq_date.sort_values(by=['Ticker', 'Acquisition Date', 'Date'], ascending=[True, True, True],
                                           inplace=True)

            # value inferior to 0 means that the stock close was prior to acquisition
            adj_close_acq_date['Date Delta'] = pd.to_datetime(adj_close_acq_date['Date']) - pd.to_datetime(
                adj_close_acq_date['Acquisition Date'])

            adj_close_acq_date['Date Delta'] = adj_close_acq_date[['Date Delta']].apply(pd.to_numeric)

            adj_close_acq_date_modified = adj_close_acq_date[adj_close_acq_date['Date Delta'] >= 0]

            adj_close_pivot = adj_close_acq_date_modified.pivot_table(index=['Ticker', 'Acquisition Date'],
                                                                      values='Adj Close', aggfunc=np.max)
            adj_close_pivot.reset_index(inplace=True)

            adj_close_pivot_merged = pd.merge(adj_close_pivot, merged_portfolio
                                              , on=['Ticker', 'Acquisition Date'])

            trace1 = go.Bar(
                x=adj_close_pivot_merged['Ticker'][0:10],
                y=adj_close_pivot_merged['ticker return'][0:10], name='Ticker Total Return', marker_color='#8D539B')

            data = trace1
            layout = go.Layout(
                barmode='group'
                , yaxis=dict(title='Returns', tickformat=".2%")
                , xaxis=dict(title='Ticker')
                , legend=dict(x=.8, y=1)
            )
            fig_return = go.Figure(data=data, layout=layout)
            fig_return.update_layout(width=400, height=400)
            fig_return.update_xaxes(showgrid=False)
            fig_return.update_yaxes(showgrid=False)
            st.plotly_chart(fig_return)

        if st.sidebar.button("All info added"):
            return_graph()