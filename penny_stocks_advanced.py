import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 5 minutes (300,000 ms)
st_autorefresh(interval=300000, key="datarefresh")

# -------------------------------
# PAGE SETTINGS
# -------------------------------
st.set_page_config(page_title="Top 10 Penny Stocks", layout="wide")
st.title("📈 Top 10 Penny Stocks (Under $5)")

# -------------------------------
# STEP 1: Define Penny Stock Criteria
# -------------------------------
PRICE_LIMIT = 5.00  # Stocks below $5
EXCHANGES = ["NASDAQ", "NYSE", "AMEX"]  # U.S. markets

# Example tickers (You can expand later or connect to an API)
# These are liquid penny stocks as examples.
TICKERS = ["SNDL", "AGRI", "CEI", "ZOM", "BBIG", "CLOV", "PROG", "IDEX", "HCMC", "VINO"]

# -------------------------------
# STEP 2: Fetch Data
# -------------------------------
def fetch_data(tickers):
    data_list = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            info = stock.info
            price = info.get("regularMarketPrice", None)
            recs = info.get("recommendationKey", "N/A")  # Analyst recommendation
            if price and price <= PRICE_LIMIT:
                data_list.append({
                    "Ticker": ticker,
                    "Price": price,
                    "Analyst Rating": recs.upper(),
                    "Volume": info.get("volume", 0)
                })
        except Exception as e:
            continue
    return pd.DataFrame(data_list)

df = fetch_data(TICKERS)

# -------------------------------
# STEP 3: Sort & Display
# -------------------------------
if not df.empty:
    df = df.sort_values(by="Volume", ascending=False).head(10)
    st.subheader("Top 10 Penny Stocks (Sorted by Volume)")
    st.dataframe(df)

    # -------------------------------
    # STEP 4: Show Chart for First Stock
    # -------------------------------
    first_ticker = df.iloc[0]["Ticker"]
    st.subheader(f"Price Chart: {first_ticker}")
    chart_data = yf.download(first_ticker, period="5d", interval="1h")

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=chart_data.index,
        open=chart_data['Open'],
        high=chart_data['High'],
        low=chart_data['Low'],
        close=chart_data['Close'],
        name='Candlestick'
    ))
    fig.update_layout(title=f"{first_ticker} (Last 5 Days)", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No penny stocks found under $5 right now.")
