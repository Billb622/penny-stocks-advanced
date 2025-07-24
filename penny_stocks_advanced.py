import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 5 minutes
st_autorefresh(interval=300000, key="datarefresh")

# App title
st.title("🔥 Top Penny Stocks Dashboard")

# Input for number of stocks
num_stocks = st.slider("How many stocks to display?", 5, 20, 10)

# Finnhub API key (replace with your key)
FINNHUB_API_KEY = d200o71r01qmbi8qhv00d200o71r01qmbi8qhv0g

# Sample penny stock tickers list (you can expand this later)
tickers = ["SNDL", "CEI", "NOK", "BBIG", "ZOM", "OCGN", "AHT", "GNUS", "HCMC", "AGRX"]

# Fetch data
data = []
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"][0]
        if price < 5:  # Penny stock filter
            # Get analyst rating from Finnhub
            url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={ticker}&token={FINNHUB_API_KEY}"
            response = requests.get(url).json()
            if response:
                latest_rating = response[0]
                strong_buy = latest_rating.get("strongBuy", 0)
                buy = latest_rating.get("buy", 0)
                sell = latest_rating.get("sell", 0)
                score = strong_buy * 3 + buy * 2 - sell
            else:
                score = 0
            data.append({
                "Ticker": ticker,
                "Price": round(price, 2),
                "Volume": int(stock.info.get("volume", 0)),
                "Analyst Score": score
            })
    except:
        pass

# Convert to DataFrame
df = pd.DataFrame(data)

# Sort options
sort_by = st.radio("Sort by:", ["Volume", "Analyst Score"])
df = df.sort_values(by=sort_by, ascending=False)

# Display top stocks
st.subheader(f"Top {num_stocks} Penny Stocks by {sort_by}")
st.dataframe(df.head(num_stocks))
