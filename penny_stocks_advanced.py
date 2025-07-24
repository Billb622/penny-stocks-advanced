import streamlit as st
import yfinance as yf
import pandas as pd
from finnhub import Client
import os

# -------------------------------
# CONFIGURE FINNHUB API
# -------------------------------
FINNHUB_API_KEY = "d200o71r01qmbi8qhv00d200o71r01qmbi8qhv0g"  # Replace with your actual Finnhub key
finnhub_client = Client(api_key=FINNHUB_API_KEY)

# -------------------------------
# APP TITLE
# -------------------------------
st.set_page_config(page_title="🔥 Top Penny Stocks Dashboard", layout="wide")
st.title("🔥 Top Penny Stocks Dashboard")

# -------------------------------
# USER INPUTS
# -------------------------------
max_stocks = st.slider("How many stocks to display?", min_value=5, max_value=20, value=10)
price_limit = st.number_input("Maximum Price for Penny Stock ($):", min_value=1.0, max_value=20.0, value=5.0)
sort_option = st.radio("Sort by:", ["Strong Buy", "Volume"])

# -------------------------------
# STOCK LIST (You can expand or make dynamic)
# -------------------------------
stocks_list = ["NOK", "OCGN", "SNDL", "BBIG", "CTRM", "GPRO", "FCEL", "ZOM", "IDEX", "PLTR"]

# -------------------------------
# FUNCTIONS
# -------------------------------
def get_recommendation(symbol):
    try:
        rec = finnhub_client.recommendation_trends(symbol)
        if rec and len(rec) > 0:
            latest = rec[0]
            return (
                latest.get("strongBuy", 0),
                latest.get("buy", 0),
                latest.get("hold", 0),
                latest.get("sell", 0),
                latest.get("strongSell", 0)
            )
        else:
            return (0, 0, 0, 0, 0)
    except:
        return (0, 0, 0, 0, 0)

# -------------------------------
# BUILD DATAFRAME
# -------------------------------
data = []
for stock in stocks_list:
    try:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period="1d")

        if hist.empty:
            continue

        price = hist["Close"].iloc[-1]
        volume = hist["Volume"].iloc[-1]

        # ✅ Skip if price is above user-defined limit
        if price > price_limit:
            continue

        strong_buy, buy, hold, sell, strong_sell = get_recommendation(stock)
        data.append([stock, price, volume, strong_buy, buy, hold, sell, strong_sell])

    except Exception as e:
        st.write(f"Error loading {stock}: {e}")

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Ticker", "Price", "Volume", "Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"])

# ✅ Sort
if sort_option == "Strong Buy":
    df = df.sort_values(by="Strong Buy", ascending=False)
else:
    df = df.sort_values(by="Volume", ascending=False)

# ✅ Limit Rows
df = df.head(max_stocks)

# -------------------------------
# DISPLAY
# -------------------------------
st.subheader(f"Top {max_stocks} Penny Stocks (Price <= ${price_limit}) by {sort_option}")
st.dataframe(df)
