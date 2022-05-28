#---------------------------------------------  IMPORTING LIBRARIES -------------------------------------------------------------------#

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import coinmarketcapapi
import streamlit as st
import plotly.express as px


# create APP
# APP title
def app():
    st.title("Crypto Market Summary")


#----------------------------------------------- LOADING DATA ----------------------------------------------------------------------#

    @st.cache
    def get_data():
        cmc = coinmarketcapapi.CoinMarketCapAPI('21b35271-3a5e-4bea-ae8b-5483a46f64b3')
        # Obtain a list of 100 biggest active cryptocurrencies with latest market data
        data_listing = cmc.cryptocurrency_listings_latest()
        df = pd.DataFrame(data_listing.data)
        df = df[['name', 'symbol', 'cmc_rank', 'last_updated', 'quote']]
        # data in quote column are in form of json, for easier manipulation split them in to individual columns and change names
        quote = pd.json_normalize(df['quote']).iloc[:, :10]
        quote.rename(
            {'USD.price': 'price', 'USD.percent_change_24h': '%_change_24h', 'USD.percent_change_7d': '%_change_7d',
            'USD.percent_change_30d': '%_change_30d', 'USD.percent_change_60d': '%_change_60d',
            'USD.percent_change_90d': '%_change_90d',
            'USD.market_cap': 'market_cap', 'USD.volume_24h': 'volume', 'USD.volume_change_24h': 'volume_change'}, axis=1,
            inplace=True)
        quote.drop(quote.columns[[3]], axis=1, inplace=True)
        # concatenate two dataframes in to one and change datetime format
        data = pd.concat([df, quote], axis=1, join='inner')
        data = data.drop(columns=['quote'])
        # Drop rows containing USD (tether) or DAI
        data.drop(data[data['symbol'].str.contains('US|DAI')].index.tolist(), inplace=True)
        data['last_updated'] = pd.to_datetime(data['last_updated']).dt.strftime('%Y-%m-%d %H:%M')
        data['volatility'] = data['price'].pct_change().rolling(7).std().fillna(0)
        return data

#------------------------------------ LOAD DATAFRAMES -------------------------#
#1. treemap
    data = get_data()
    top10_crypto = data.loc[:, ["name", "symbol",'market_cap']].sort_values(by="market_cap", ascending=False)[:10]
    labels = ["%s\n%d \n" % (label) for label in zip(top10_crypto['symbol'].value_counts().index, top10_crypto['market_cap'].value_counts().index)]
    #2. barplot
    name = data['name'].head(12)
    price_24 = data['%_change_24h'].sort_values(ascending=False).head(12)
    price_7 = data['%_change_7d'].sort_values(ascending=False).head(12)
    price_30 = data['%_change_30d'].sort_values(ascending=False).head(12)
    price_60 = data['%_change_60d'].sort_values(ascending=False).head(12)
    price_90 = data['%_change_90d'].sort_values(ascending=False).head(12)
    #3. volume


    df1 = data[['name', 'volume', 'volatility',]].sort_values(by='volatility', ascending=False)[:10]


    #--------------------------------------------------------- Treemap --------------------------------------------------------------------#

    st.header("Treemap Cryptocurrencies by Market Cap")

    plt.style.use('dark_background')
    fig = px.treemap(top10_crypto, path=['symbol', 'market_cap'], values='market_cap', color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(fig)

    #------------------------------------------------------ Price Change ------------------------------------------------------------------#
    st.header("How much can the price change?")
    st.caption("Click the button and find out!")

    def barplot(name, price):
        # Horizontal Bar Plot
        fig = px.bar(data, x=price, y=name, orientation='h', text=price,
                     labels={'x': 'Cryptocurrency', 'y':'Price Change'})
        fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
        # Save chart
        st.plotly_chart(fig)


    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        if st.button('24h'):
            result = barplot(name, price_24)
            st.write(result)

    with col2:
        if st.button('7d'):
            result = barplot(name, price_7)
            st.write(result)

    with col3:
        if st.button('30d'):
            result = barplot(name, price_30)
            st.write(result)

    with col4:
        if st.button('60d'):
            result = barplot(name, price_60)
            st.write(result)

    with col5:
        if st.button('90d'):
            result = barplot(name, price_90)
            st.write(result)






    #-------------------------------------------------------------------------- Volume & Volatility ------------------------------------------------------------------------#
    st.header("7 day historic volatility and volume")

    fig = px.scatter(df1, x="volume", y='name',size="volatility", color= 'name',hover_name="name", size_max=60, color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False))
    fig.update_xaxes(row=1, col=2, zeroline=False)

    st.plotly_chart(fig)
