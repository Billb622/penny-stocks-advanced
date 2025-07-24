import streamlit as st
import requests
import pandas as pd

# ✅ Finnhub API Key
FINNHUB_API_KEY = "your_finnhub_api_key"

# ✅ Penny stock list
PENNY_STOCKS = ["NOK", "SNDL", "OCGN", "BBIG", "ZOM", "TRCH", "HCMC", "NAKD", "SENS", "IDEX"]

# ✅ Streamlit UI
st.set_page_config(page_title="🔥 Top Penny Stocks Dashboard", layout="wide")
st.title("🔥 Top Penny Stocks Dashboard")

count = st.slider("How many stocks to display?", 5, 20, 10)
sort_option = st.radio("Sort by:", ["Strong Buy", "Volume"], index=0)

# ✅ Get recommendation data
def get_recommendation(symbol):
    url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    if isinstance(response, list) and len(response) > 0:
        latest = response[0]
        return latest.get("strongBuy", 0), latest.get("buy", 0), latest.get("hold", 0), latest.get("sell", 0), latest.get("strongSell", 0)
    return 0, 0, 0, 0, 0  # Default if no data

# ✅ Get stock price & volume
def get_quote(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    return response.get("c", 0), response.get("v", 0)

# ✅ Build data table
data = []
for stock in PENNY_STOCKS:
    strong_buy, buy, hold, sell, strong_sell = get_recommendation(stock)
    price, volume = get_quote(stock)
    if strong_buy > 0:  # Only show stocks with Strong Buy
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

# ✅ Sort by Strong Buy or Volume
if sort_option == "Strong Buy":
    df = df.sort_values(by="Strong Buy", ascending=False)
else:
    df = df.sort_values(by="Volume", ascending=False)

# ✅ Limit to user selection
df = df.head(count)

# ✅ Display
st.subheader(f"Top {count} Penny Stocks (Strong Buy Only)")
st.dataframe(df)
