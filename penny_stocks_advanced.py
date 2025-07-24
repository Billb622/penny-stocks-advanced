import streamlit as st
import requests
import pandas as pd

# ✅ Finnhub API Key (replace with your key)
FINNHUB_API_KEY = "your_finnhub_api_key"

# ✅ Penny stock list (example: you can expand this later)
PENNY_STOCKS = ["NOK", "SNDL", "OCGN", "BBIG", "ZOM", "TRCH", "HCMC", "NAKD", "SENS", "IDEX"]

# ✅ Streamlit UI
st.set_page_config(page_title="🔥 Top Penny Stocks Dashboard", layout="wide")
st.title("🔥 Top Penny Stocks Dashboard")

# Slider for number of stocks to display
count = st.slider("How many stocks to display?", 5, 20, 10)

# Sort options
sort_option = st.radio("Sort by:", ["Strong Buy", "Volume"], index=0)

# ✅ Function to get recommendations
def get_recommendation(symbol):
    url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    if response:
        latest = response[0]  # latest recommendation
        return latest.get("strongBuy", 0), latest.get("buy", 0), latest.get("hold", 0), latest.get("sell", 0), latest.get("strongSell", 0)
    return 0, 0, 0, 0, 0

# ✅ Function to get quote data (price & volume)
def get_quote(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    return response.get("c", 0), response.get("v", 0)

# ✅ Collect Data
data = []
for stock in PENNY_STOCKS:
    strong_buy, buy, hold, sell, strong_sell = get_recommendation(stock)
    price, volume = get_quote(stock)

    # ✅ Only include stocks with at least 1 Strong Buy recommendation
    if strong_buy > 0:
        data.append({
            "Ticker": stock,
            "Price": price,
            "Volume": volume,
            "Strong Buy": strong_buy,
            "Buy": buy,
            "Hold": hold,
            "Sell": sell,
            "Strong Sell": strong_sell
        })

# ✅ Convert to DataFrame
df = pd.DataFrame(data)

# ✅ Sort
if sort_option == "Strong Buy":
    df = df.sort_values(by="Strong Buy", ascending=False)
else:
    df = df.sort_values(by="Volume", ascending=False)

# ✅ Limit by slider
df = df.head(count)

# ✅ Display table
st.subheader(f"Top {count} Penny Stocks (Strong Buy Priority)")
st.dataframe(df)
