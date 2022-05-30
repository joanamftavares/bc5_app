## Group Z - Project Members:
- Ana Leonor Vital - m20210618
- Joana Tavares - m20210621
- Laura Santos - r20181094
- Maria Oliveira - m20210612


## Project Context:
Investments4Some is a long-standing Portuguese, privately held hedge funds management firm. They have been exploring Machine Learning models for market price forecasting, which is used to anticipate market trends. Our team was hired by Warner Buffer and Gil Bates, partners of Investments4Some, to develop a dashboard for their financial analysts. 
This Dashboard was thought as a tool to assist the internal financial team and external stakeholders in the investment planning, allowing them to collect useful insights and deeper knowledge about any arbitrary stock and digital currency, thus improving the quality of their portfolios and provide an easy way to keep track of the market trends.

## Description of the Dashboard:
The dashboard is composed of multiple pages, namely Home Page, Crypto Market Summary, Stock Market Summary, Trend Analysis, Forecast and Portfolio Page (available inside the folder "Apps").
- In the Home Page, the investor can take a short quiz to find out which type of investor he/she is and, for new investors, some tips are provided.
- The Market Summary pages display important visualizations regarding the most important stocks and crypto currencies up to this date, such as market capitalization, volume, and volatility. 
- The Trend Analysis page includes plots from 3 key indicators such as Moving Average (MA), Moving Average Convergence Divergence (MACD) and Relative Strength Index (RSI) indicators, and a candlestick plot. This page is personalized for each stock or crypto the user wishes to analyze, which can be achieved through the input of the symbol in the input box on the top of the page.
- The Forecast page includes the predictions for the close price and the user can use this forecasting tool for any stock or crypto and choose the time frame for the predicting, up to 10 days. Similarly to the trend analysis, the investor can benefit from this forecasting tool for any stock or cryptocurrency. The prediction model is an univariate LSTM that uses TensorFlow. In order to reduce the time the predictions were displayed in the app, after training the model, we saved it in a HDF5 file, and every time a different prediction is made in the app, it loads the compiled model identical to the one we saved. 
- Finally, the Portfolio page is dedicated to each individual investor profile and designed to assist the assessment of the performance of acquired stocks, which can support the planning of future investments. The investors can insert the stocks and digital currencies they own, and additionally provide information about their respective acquisition to take advantage of the complete analysis offered in this page.

The data is daily updated and automatically downloaded from *yfinance* – Yahoo! Finance’s API.
The dashboard was built using streamlit and the plots using Plotly. The dashboard can be run following the command “streamlit run app.py”, but was also deployed and the app is live in this link: https://bc5-5w01.onrender.com/

**Home Page**
![image](https://user-images.githubusercontent.com/90759149/170966173-b596e1e1-cd61-41ad-b49c-2510e3f412c6.png)

**Crypto Market Summary Page**
![image](https://user-images.githubusercontent.com/90759149/170966276-e3dd29a4-343d-4e06-bcfd-02c92fc2cbc4.png)
![image](https://user-images.githubusercontent.com/90759149/170966399-d9b7a07f-69f8-463b-b9d1-0eb697fce242.png)
![image](https://user-images.githubusercontent.com/90759149/170966455-82b3a3bf-691c-4d84-b656-3f1733c5313f.png)

**Stock Market Summary Page**
![image](https://user-images.githubusercontent.com/90759149/170966584-9f5a0b97-e359-442b-9e5e-152271b329f7.png)

**Trend Analysis Page**
![image](https://user-images.githubusercontent.com/90759149/170966713-baa667cd-4ade-4f69-aaa3-8d6f99276251.png)
![image](https://user-images.githubusercontent.com/90759149/170966772-21a22876-d697-4704-9abe-1bc1518927c0.png)

**Forecast Page**
![image](https://user-images.githubusercontent.com/90759149/170966876-8723fad3-c861-4fae-9616-2c72d9a5b688.png)
![image](https://user-images.githubusercontent.com/90759149/170966942-991ae343-ddc2-49d5-856b-5c84871dbee2.png)


**Portfolio Page**
![image](https://user-images.githubusercontent.com/90759149/170966059-3495e704-403c-427c-ac9f-a523e24dcf09.png)

