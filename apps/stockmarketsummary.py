import streamlit as st
from datetime import date
from plotly import graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from itertools import cycle
import plotly.express as px
#pip install yfinance
import yfinance as yf
import time
import pandas_datareader as pdr


def app():
    START = "2020-05-31"
    #current date
    TODAY= date.today().strftime("%Y-%m-%d")

#---------------------------------------------COLLECTING DATA ----------------------------------------------------------------#
    #import the data
    df_V = yf.download(tickers='V', start="2020-05-31", end=TODAY)
    df_NVDA = yf.download(tickers='NVDA',start="2020-05-31", end=TODAY)
    df_UNH = yf.download(tickers='UNH', start="2020-05-31", end=TODAY)
    df_JNJ = yf.download(tickers='JNJ',start="2020-05-31", end=TODAY)
    df_FB = yf.download(tickers='FB',start="2020-05-31", end=TODAY)
    df_TSLA = yf.download(tickers='TSLA',start="2020-05-31", end=TODAY)
    df_AMZN = yf.download(tickers='AMZN',start="2020-05-31", end=TODAY)
    df_AAPL = yf.download(tickers='AAPL',start="2020-05-31", end=TODAY)
    df_GOOG = yf.download(tickers='GOOG',start="2020-05-31", end=TODAY)
    df_MSFT = yf.download(tickers='MSFT',start="2020-05-31", end=TODAY)


    df_V['Date'] = df_V.index
    df_NVDA['Date'] = df_NVDA.index
    df_UNH['Date'] = df_UNH.index
    df_JNJ['Date'] = df_JNJ.index
    df_FB['Date'] = df_FB.index
    df_TSLA['Date'] = df_TSLA.index
    df_AMZN['Date'] = df_AMZN.index
    df_AAPL['Date'] = df_AAPL.index
    df_GOOG['Date'] = df_GOOG.index
    df_MSFT['Date'] = df_MSFT.index

    pallete = cycle(px.colors.sequential.Viridis)

    st.title("Stock Market Summary", anchor=0.5)

    marketCap_V = pdr.get_quote_yahoo('V')['marketCap']
    marketCap_NVDA = pdr.get_quote_yahoo('NVDA')['marketCap']
    marketCap_UNH = pdr.get_quote_yahoo('UNH')['marketCap']
    marketCap_JNJ = pdr.get_quote_yahoo('JNJ')['marketCap']
    marketCap_FB = pdr.get_quote_yahoo('FB')['marketCap']
    marketCap_TSLA = pdr.get_quote_yahoo('TSLA')['marketCap']
    marketCap_AMZN = pdr.get_quote_yahoo('AMZN')['marketCap']
    marketCap_AAPL = pdr.get_quote_yahoo('AAPL')['marketCap']
    marketCap_GOOG = pdr.get_quote_yahoo('GOOG')['marketCap']
    marketCap_MSFT = pdr.get_quote_yahoo('MSFT')['marketCap']

    marketCap_V = pd.DataFrame(marketCap_V)
    marketCap_NVDA = pd.DataFrame(marketCap_NVDA)
    marketCap_UNH = pd.DataFrame(marketCap_UNH)
    marketCap_JNJ = pd.DataFrame(marketCap_JNJ)
    marketCap_FB = pd.DataFrame(marketCap_FB)
    marketCap_TSLA = pd.DataFrame(marketCap_TSLA)
    marketCap_AMZN = pd.DataFrame(marketCap_AMZN)
    marketCap_AAPL = pd.DataFrame(marketCap_AAPL)
    marketCap_GOOG = pd.DataFrame(marketCap_GOOG)
    marketCap_MSFT = pd.DataFrame(marketCap_MSFT)
    marketCap_NVDA = pd.DataFrame(marketCap_NVDA)

    df_marketcap = pd.concat([marketCap_V , marketCap_NVDA, marketCap_UNH, marketCap_JNJ, marketCap_FB, marketCap_TSLA, marketCap_AMZN,
                                marketCap_AAPL,marketCap_GOOG, marketCap_MSFT ], axis=0)

    df_marketcap['Name'] = df_marketcap.index

#------------------------------------------------ Visualizations ----------------------------------------------------------------#
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:

        st.header('Treemap Stocks by Market Cap', anchor=0.5)

        fig8 = go.Figure()
        fig8 = px.treemap(df_marketcap, path=['Name'],
                     values='marketCap')

        fig8.update_layout(treemapcolorway = ["#bddf26", "#7ad151", "#44bf70", "#22a884", "#21918c", "#2a788e", "#355f8d", "#414487", "#482475"])
        st.plotly_chart(fig8)
    with col3:
        st.write("")




    col1, col2 = st.columns(2)

    with col1:

        st.header('Most Popular Stocks', anchor=0.5)

        fig1 = go.Figure(go.Bar(
                x=[df_V['Close'].mean(),df_NVDA['Close'].mean(),
                df_UNH['Close'].mean(), df_JNJ['Close'].mean(), df_FB['Close'].mean(), df_TSLA['Close'].mean(),
                df_AMZN['Close'].mean(), df_AAPL['Close'].mean(), df_GOOG['Close'].mean(), df_MSFT['Close'].mean()],
                y=['V', 'NVDA', 'UNH', 'JNJ', 'FB', 'TSLA', 'AMZN', 'AAPL', 'GOOG', 'MSFT'],
                marker_color=next(pallete),
                orientation='h'))

        fig1.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))

        st.plotly_chart(fig1)


    with col2:
        st.header('Closing Price Over Time', anchor=0.5)

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_V['Date'], y=df_V['Close'], name='V', marker_color=next(pallete)))
        fig3.add_trace(go.Scatter(x=df_NVDA['Date'], y=df_NVDA['Close'], name='NVDA', marker_color=next(pallete)))
        fig3.add_trace(go.Scatter(x=df_UNH['Date'], y=df_UNH['Close'], name='UNH', marker_color=next(pallete)))
        fig3.add_trace(go.Scatter(x=df_JNJ['Date'], y=df_JNJ['Close'], name='JNJ', marker_color=next(pallete)))
        fig3.add_trace(go.Scatter(x=df_FB['Date'], y=df_FB['Close'], name='FB', marker_color=next(pallete)))
        fig3.add_trace(go.Scatter(x=df_TSLA['Date'], y=df_TSLA['Close'], name='TSLA', marker_color=next(pallete)))
        fig3.add_trace(go.Scatter(x=df_AMZN['Date'], y=df_AMZN['Close'], name='AMZN', marker_color=next(pallete)))
        fig3.add_trace(go.Scatter(x=df_AAPL['Date'], y=df_AAPL['Close'], name='AAPL', marker_color=next(pallete)))
        fig3.add_trace(go.Scatter(x=df_GOOG['Date'], y=df_GOOG['Close'], name='GOOG', marker_color=next(pallete)))
        fig3.add_trace(go.Scatter(x=df_MSFT['Date'], y=df_MSFT['Close'], name='MSFT', marker_color=next(pallete)))

        fig3.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))

        st.plotly_chart(fig3)



    col1, col2 = st.columns(2)

    with col1:

        st.header('Stocks Volume', anchor=0.5)

        fig2 = go.Figure(go.Bar(
                x=[df_V['Volume'].mean(),df_NVDA['Volume'].mean(),
                df_UNH['Volume'].mean(), df_JNJ['Volume'].mean(), df_FB['Volume'].mean(), df_TSLA['Volume'].mean(),
                df_AMZN['Volume'].mean(), df_AAPL['Volume'].mean(), df_GOOG['Volume'].mean(), df_MSFT['Volume'].mean()],
                y=['V', 'NVDA', 'UNH', 'JNJ', 'FB', 'TSLA', 'AMZN', 'AAPL', 'GOOG', 'MSFT'],
                marker_color=next(pallete),
                orientation='h'))

        fig2.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))

        st.plotly_chart(fig2)


    with col2:

        st.header('Price Variation Over Time', anchor=0.5)

        df_5_V= df_V['Open']- df_V['Close']
        df_5_NVDA= df_NVDA['Open']- df_NVDA['Close']
        df_5_UNH= df_UNH['Open']- df_UNH['Close']
        df_5_JNJ= df_JNJ['Open']- df_JNJ['Close']
        df_5_FB= df_FB['Open']- df_FB['Close']
        df_5_TSLA= df_TSLA['Open']- df_TSLA['Close']
        df_5_AMZN = df_AMZN['Open']- df_AMZN['Close']
        df_5_AAPL = df_AAPL['Open']- df_AAPL['Close']
        df_5_GOOG = df_GOOG['Open']- df_GOOG['Close']
        df_5_MSFT = df_MSFT['Open']- df_MSFT['Close']


        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=df_V['Date'], y=df_5_V, name='V', marker_color=next(pallete)))
        fig5.add_trace(go.Scatter(x=df_NVDA['Date'], y=df_5_NVDA, name='NVDA', marker_color=next(pallete)))
        fig5.add_trace(go.Scatter(x=df_UNH['Date'], y=df_5_UNH, name='UNH', marker_color=next(pallete)))
        fig5.add_trace(go.Scatter(x=df_JNJ['Date'], y=df_5_JNJ, name='JNJ', marker_color=next(pallete)))
        fig5.add_trace(go.Scatter(x=df_FB['Date'], y=df_5_FB, name='FB', marker_color=next(pallete)))
        fig5.add_trace(go.Scatter(x=df_TSLA['Date'], y=df_5_TSLA, name='TSLA', marker_color=next(pallete)))
        fig5.add_trace(go.Scatter(x=df_AMZN['Date'], y=df_5_AMZN, name='AMZN', marker_color=next(pallete)))
        fig5.add_trace(go.Scatter(x=df_AAPL['Date'], y=df_5_AAPL, name='AAPL', marker_color=next(pallete)))
        fig5.add_trace(go.Scatter(x=df_GOOG['Date'], y=df_5_GOOG, name='GOOG', marker_color=next(pallete)))
        fig5.add_trace(go.Scatter(x=df_MSFT['Date'], y=df_5_MSFT, name='MSFT', marker_color=next(pallete)))

        fig5.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))

        st.plotly_chart(fig5)
