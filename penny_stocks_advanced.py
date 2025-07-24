import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

# Auto-refresh every 5 min (300 seconds)
st_autorefresh = st.experimental_rerun

st.set_page_config(page_title="Top Penny Stocks", layout="wide")
st.title("🔥 Top 10 Penny Stocks Analyzer")
st.write("Filters: Price < $5, sorted by % gain. Click a ticker for chart!")

# Filters
min_price = st.slider("Max Price", 0.1, 5.0, 5.0)
min_volume = st.number_input("Minimum Volume", value=100000)

# Refresh button
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

# Hardcoded penny stock sample list (expand later)
tickers = [
    "SNDL", "ZOM", "HCMC", "AITX", "IQST", "ENZC", "NSAV", "GAXY", "VYST", "MJNA",
    "XELA", "CTRM", "CEI", "METX", "NWBO", "RGBP", "COSM", "IDEX", "BTTX", "AGRI"
]

# Fetch stock data
data = []
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('regularMarketPrice', None)
        volume = info.get('volume', 0)
        change_percent = info.get('regularMarketChangePercent', 0)

        if price and price < min_price and volume > min_volume:
            data.append({
                "Ticker": ticker,
                "Price": round(price, 3),
                "% Change": round(change_percent, 2),
                "Volume": volume
            })
    except:
        pass

df = pd.DataFrame(data)

if not df.empty:
    df = df.sort_values(by="% Change", ascending=False).head(10)
    st.subheader("📊 Top 10 Penny Stocks:")
    st.dataframe(df)

    # Select a ticker for chart
    ticker_choice = st.selectbox("Select a ticker for chart:", df["Ticker"].tolist())

    if ticker_choice:
        st.subheader(f"📈 {ticker_choice} - Last 1 Month Candlestick Chart")
        hist = yf.download(ticker_choice, period="1mo", interval="1d")
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close']
        )])
        fig.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # CSV Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "top_penny_stocks.csv", "text/csv")
else:
    st.warning("⚠ No penny stocks found with current filters.")