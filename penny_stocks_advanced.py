import streamlit as st
import pandas as pd
import requests
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 5 minutes
st_autorefresh(interval=300000, key="datarefresh")

# ---------------------------
# Finnhub API Key
# ---------------------------
FINNHUB_API_KEY = "d200o71r01qmbi8qhv00d200o71r01qmbi8qhv0g"  # Replace with your real key

# ---------------------------
# Streamlit App UI
# ---------------------------
st.title("🔥 Top Penny Stocks Dashboard")

# User controls
num_stocks = st.slider("How many stocks to display?", 5, 20, 10)
sort_by = st.radio("Sort by:", ["Strong Buy", "Volume"])
PRICE_LIMIT = st.slider("Max Stock Price ($)", 1.0, 10.0, 5.0)

# ---------------------------
# List of penny stock tickers
# ---------------------------
penny_stocks = ["NOK", "OCGN", "SNDL", "BBIG", "CTRM", "GPRO", "FCEL", "ZOM", "IDEX"]

# ---------------------------
# Finnhub recommendation API
# ---------------------------
def get_recommendation(ticker):
    url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={ticker}&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    if isinstance(response, list) and len(response) > 0:
        latest = response[0]  # Most recent recommendation
        return latest.get("strongBuy", 0), latest.get("buy", 0), latest.get("hold", 0), latest.get("sell", 0), latest.get("strongSell", 0)
    return 0, 0, 0, 0, 0

# ---------------------------
# Collect data for each stock
# ---------------------------
data = []
for stock in penny_stocks:
    try:
        ticker = yf.Ticker(stock)
        price = ticker.info.get("regularMarketPrice", 0)
        volume = ticker.info.get("volume", 0)

        if price is not None and price <= PRICE_LIMIT:  # Penny stock filter
            strong_buy, buy, hold, sell, strong_sell = get_recommendation(stock)

            # Only include stocks with at least one rating
            if (strong_buy + buy + hold + sell + strong_sell) > 0:
                data.append([stock, price, volume, strong_buy, buy, hold, sell, strong_sell])
    except Exception as e:
        st.write(f"Error loading {stock}: {e}")

# ---------------------------
# Create DataFrame
# ---------------------------
columns = ["Ticker", "Price", "Volume", "Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]
df = pd.DataFrame(data, columns=columns)

# Sort based on user selection
if sort_by == "Strong Buy":
    df = df.sort_values(by="Strong Buy", ascending=False)
else:
    df = df.sort_values(by="Volume", ascending=False)

# Limit number of results
df = df.head(num_stocks)

# ---------------------------
# Display Table
# ---------------------------
st.subheader(f"Top {len(df)} Penny Stocks (Price ≤ ${PRICE_LIMIT}) by {sort_by}")
st.dataframe(df)

# ---------------------------
# Download Option
# ---------------------------
st.download_button("Download as CSV", df.to_csv(index=False), "penny_stocks.csv", "text/csv")
