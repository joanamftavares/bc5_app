from itertools import cycle
import streamlit as st
from datetime import date
import yfinance as yf
from plotly import graph_objs as go
import numpy as np

#st.set_page_config(layout="wide")
def app():
  START = "2019-05-05"
  # current date
  TODAY = date.today().strftime("%Y-%m-%d")

  # create APP
  # APP title
  selected_stock = st.text_input('Enter stock or crytocurrency', 'BTC-USD')
  st.write('The current stock  is', selected_stock)
  st.info('Not sure about the symbol of the stock or crypto you are looking for? Check this [link](https://finance.yahoo.com/) to find out the available tickers')


  # cache the data of the stock we choose and doesn't have to run the code below again
  @st.cache
  def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

  data = load_data(selected_stock)

  #Cria a coluna do change
  #diff for close price
  data['Change_close'] = round(data['Close'].pct_change()*100,2)
  #diff for open price
  data['Change_open'] = round(data['Open'].pct_change()*100,2)
  #diff for low price
  data['Change_high'] = round(data['High'].pct_change()*100,2)
  #diff for high price
  data['Change_low'] = round(data['Low'].pct_change()*100,2)

  box1, box2, box3, box4, box5 = st.columns(5)

  box1.metric(label="Close Price",
            value=round(data["Close"].tail(1), 2),
            delta="%s%%"%data["Change_close"][len(data["Change_close"]) - 1])

  box2.metric(label="Open Price",
            value=round(data["Open"].tail(1), 2),
            delta="%s%%"%data['Change_open'][len(data['Change_open']) - 1])

  box3.metric(label="High Price",
            value=round(data["High"].tail(1), 2),
            delta="%s%%"%data["Change_high"][len(data["Change_high"]) - 1])

  box4.metric(label="Low Price",
            value=round(data["Low"].tail(1), 2),
            delta="%s%%"%data["Change_low"][len(data["Change_low"]) - 1])

  #Criaçao das colunas do MACD para fazer o kip5
  k = data['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
  d = data['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
  data['MACD'] = k - d
  data['MACD_S'] = data['MACD'].ewm(span=9, adjust=False, min_periods=9).mean()

  if ((data['MACD'][len(data['MACD']) - 1]) < (data['MACD_S'][len(data['MACD_S']) - 1])):
      signal="Bearish"
  else:
      signal="Bullish"
  box5.metric(label="Signal", value= signal)

  ##########Grafico da variaçao do preço de fecho ao longo do tempo##############################################
  st.markdown("<h1 style='text-align: center; '>Closing price variation over time</h1>", unsafe_allow_html=True)

  col1, col2, col3 = st.columns(3)

  col1.write(' ')

  fig = go.Figure()
  fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Closing Price', line=dict(color='#33638D')))
  fig.update_xaxes(showgrid=False)
  fig.update_yaxes(showgrid=False)
  col2.plotly_chart(fig)

  col3.write(' ')

  ###########Gráfico dos indicadores#########################################################################
  #Criação das colunas necessárias para os indicadores
  #Moving average (MA)
  data['MA_20'] = data['Close'].rolling(window=20, min_periods=1).mean()
  data['MA_50'] = data['Close'].rolling(window=50, min_periods=1).mean()
  #create a new column 'Signal' such that if 20-day EMA is greater   # than 50-day EMA then set Signal as 1 else 0
  data['Signal'] = 0.0
  data['Signal'] = np.where(data['MA_20'] > data['MA_50'], 1.0, 0.0)
  # create a new column 'Position' which is a day-to-day difference of # the 'Signal' column
  data['Position'] = data['Signal'].diff()

  #Moving Average Convergence Divergence (MACD)
  # Get the 26-day EMA of the closing price
  #k = data['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
  # Get the 12-day EMA of the closing price
  #d = data['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
  # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
  #data['MACD'] = k - d
  # Get the 9-Day EMA of the MACD for the Trigger line
  #data['MACD_S'] = data['MACD'].ewm(span=9, adjust=False, min_periods=9).mean()
  # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
  data['MACD_H'] = data['MACD'] - data['MACD_S']
  colors = np.where(data['MACD_H'] < 0, '#BA7272', '#59C3C3')

  #RSI
  def computeRSI(df, time_window):
    diff = df.diff(1).dropna()

    up_chg = 0 * diff
    down_chg = 0 * diff

    up_chg[diff > 0] = diff[diff > 0]

    down_chg[diff < 0] = diff[diff < 0]

    up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

    rs = abs(up_chg_avg / down_chg_avg)
    rsi = 100 - 100 / (1 + rs)
    return rsi

  data['RSI'] = computeRSI(data['Close'], 14)

  #Criação dos gráficos
  st.markdown("<h1 style='text-align: center; '>Indicators</h1>", unsafe_allow_html=True)

  chart1, chart2, chart3 = st.columns(3)
  #Moving Average Convergence Divergence
  fig1 = go.Figure()
  fig1.add_trace(go.Scatter(x=data['Date'], y=data['MACD'], name='MACD', line=dict(color='#404788')))
  fig1.add_trace(go.Scatter(x=data['Date'], y=data['MACD_S'], name='SIGNAL', line=dict(color='#55C667')))
  fig1.add_trace(go.Bar(x=data['Date'],y=data['MACD_H'],name='Histogram',marker_color=colors))
  fig1.update_layout(title='Moving Average Convergence Divergence (MACD)', title_x=0.5, width=600, height=450)
  fig1.update_xaxes(showgrid=False)
  fig1.update_yaxes(showgrid=False)
  chart1.plotly_chart(fig1)

  #RSI
  fig2 = go.Figure()
  fig2.add_trace(go.Scatter(x=data['Date'], y=data['RSI'], name='Rsi', line=dict(color='#238A8D')))
  fig2.update_layout(title='Relative Strength Index (RSI)', title_x=0.5, width=600, height=450)
  fig2.update_xaxes(showgrid=False)
  fig2.update_yaxes(showgrid=False)
  chart2.plotly_chart(fig2)

  #Cria o grafico da MA com o buy e sell
  # plot close price, short-term and long-term moving averages
  fig3 = go.Figure()
  fig3.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Closing_price', line=dict(color='#33638D')))
  fig3.add_trace(go.Scatter(x=data['Date'], y=data['MA_20'], name='20_MA', line=dict(color='#3CBB75')))
  fig3.add_trace(go.Scatter(x=data['Date'], y=data['MA_50'], name='50_MA', line=dict(color='#453781')))
  fig3.add_trace(go.Scatter(x=data[data['Position'] == 1]['Date'], y=data['MA_20'][data['Position'] == 1], name='Buy', mode='markers', marker=dict(symbol='triangle-up', size=15, color = "green")))
  fig3.add_trace(go.Scatter(x=data[data['Position'] == -1]['Date'], y=data['MA_20'][data['Position'] == -1], name='Sell', mode='markers', marker=dict(symbol='triangle-down', size=15, color = "red")))
  fig3.update_layout(title='Simple Moving Average (SMA)', title_x=0.5, width=640, height=450)
  fig3.update_xaxes(showgrid=False)
  fig3.update_yaxes(showgrid=False)
  chart3.plotly_chart(fig3)

  ###########Pequena descriçao dos gráficos#######################################################
  text1, text2, text3 = st.columns([0.9, 0.9, 0.9])
  text1.write('Moving Average Convergence Divergence identifies the trend direction and time span by computing two moving averages of different lengths, and calculates the difference of the result, forming the MACD line, as well as the exponential moving average of the moving averages, which forms the signal line. If the MACD line is above zero, it means that the price is in an ascending phase, and if it is below zero, it means that it is in a descending phase.Thus, when the MACD line crosses below the signal line, it is a bearish signal, that indicates that it may be time to sell, and when the MACD line crosses above the signal line, the indicator gives a bullish signal, which suggests that the price of the asset is likely to experience upward momentum.')

  text2.write('Relative Strength Index is a momentum indicator that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset. The RSI oscillates between zero and 100 and, traditionally, it is considered overbought when above 70 and oversold when below 30.')

  text3.write('Moving averages help predict the future trend and determine whether an asset price will continue or reverse the trend. This indicator can use two or more moving averages, one generally short-term, that is, faster, and one long-term, that is, slower. When these two averages cross, it can be an indicator to decide whether to sell or buy assets. It is a buy signal when the short-term moving average crosses above the long-term moving average, and it is a good time to sell when the short-term moving average crosses below the long-term moving average.')

  ###########Outros links para mais pesquisa#####################################################
  texto1, texto2, texto3 = st.columns([0.9, 0.9, 0.9])
  texto1.info("Learn more about MACD here: [link](https://www.investopedia.com/terms/m/macd.asp)")
  texto2.info("Learn more about RSI here: [link](https://www.investopedia.com/terms/r/rsi.asp)")
  texto3.info("Learn more about RSI here: [link](https://www.investopedia.com/terms/s/sma.asp)")


  ###############Gráfico candlestick#################################################################
  st.markdown("<h1 style='text-align: center; '>Candlestick chart</h1>", unsafe_allow_html=True)

  cols1, cols2, cols3 = st.columns([1.5,2,1.5])
  cols1.write(' ')

  fig4 = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
  fig4.update_xaxes(showgrid=False)
  fig4.update_yaxes(showgrid=False)
  cols2.plotly_chart(fig4)

  cols3.write(' ')

  ##############Pequena descriçao do grafico do candlestick####################################
  coluna1, coluna2, coluna3 = st.columns([1,2,1])
  coluna1.write(' ')

  coluna2.write('A daily candlestick shows the markets open, high, low, and close price for the day. The rectangular part of the candlestick is called the "real body" which shows the connection between the opening and closing prices. This real body shows the price range between the open and close for that trading day. When the real body is red, it means that the closing price is lower than the opening price and is known as the bearish candle. If the actual body is green then it means that the closing price was higher than the opening price, known as a bullish candle.')

  coluna3.write(' ')

  ###########Outros links para mais pesquisa#####################################################
  colunas1, colunas2, colunas3 = st.columns([1,2,1])
  colunas1.write(' ')
  colunas2.info("Learn more about Candlesticks here: [link1](https://www.investopedia.com/trading/candlestick-charting-what-is-it/) and here [link2](https://www.elearnmarkets.com/blog/35-candlestick-patterns-in-stock-market/)")
  colunas3.write(' ')