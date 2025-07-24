import streamlit as st
import yfinance as yf
import pandas as pd
import requests

# 🔑 Replace with your Finnhub API Key
FINNHUB_API_KEY = "d200o71r01qmbi8qhv00d200o71r01qmbi8qhv0g"

# ✅ Title
st.title("🔥 Top Penny Stocks Dashboard")

# ✅ UI Controls
num_stocks = st.slider("How many stocks to display?", 5, 20, 10)
sort_option = st.radio("Sort by:", ["Strong Buy", "Volume"])

# ✅ Penny Stock Candidates (You can customize this list)
stocks_list = ["NOK", "OCGN", "SNDL", "BBIG", "ZOM", "IDEX", "CTRM", "GPRO", "FCEL", "PLTR"]

# ✅ Finnhub API - Get Recommendation
def get_recommendation(symbol):
    url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    if len(response) > 0:
        latest = response[0]
        return latest.get("strongBuy", 0), latest.get("buy", 0), latest.get("hold", 0), latest.get("sell", 0), latest.get("strongSell", 0)
    return 0, 0, 0, 0, 0

# ✅ Build DataFrame
data = []
for stock in stocks_list:
    try:
        ticker = yf.Ticker(stock)
        price = ticker.history(period="1d")["Close"].iloc[-1]
        volume = ticker.history(period="1d")["Volume"].iloc[-1]
        strong_buy, buy, hold, sell, strong_sell = get_recommendation(stock)
        data.append([stock, price, volume, strong_buy, buy, hold, sell, strong_sell])
    except Exception as e:
        st.write(f"Error loading {stock}: {e}")

df = pd.DataFrame(data, columns=["Ticker", "Price", "Volume", "Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"])

# ✅ Sort
if sort_option == "Strong Buy":
    df = df.sort_values(by="Strong Buy", ascending=False)
else:
    df = df.sort_values(by="Volume", ascending=False)

# ✅ Display
st.subheader(f"Top {num_stocks} Penny Stocks by {sort_option}")
st.dataframe(df.head(num_stocks))
