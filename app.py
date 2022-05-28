import streamlit as st
from multipage_app import MultiApp
from apps import forecast, home, trend, portfolio, cryptomarketsummary, stockmarketsummary

st.set_page_config(layout="wide")
app = MultiApp()

st.markdown("""
# Investments4Some APP
 This app aims to help you take informed investment decisions, whether you are an internal financial team or an external stakeholder. 
""")

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Crypto Market Summary", cryptomarketsummary.app)
app.add_app("Stock Market Summary", stockmarketsummary.app)
app.add_app("Trend Analysis", trend.app)
app.add_app("Forecast", forecast.app)
app.add_app("Portfolio", portfolio.app)
# The main app
app.run()