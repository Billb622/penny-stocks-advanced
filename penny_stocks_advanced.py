import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.title("📉 Top Penny Stocks Analyzer")
st.write("Top penny stocks (price < $5) ranked by analyst rating, with charts and filters.")

# Penny stocks list
penny_stocks_list = [
    "SNDL", "NAK", "AITX", "BNGO", "ZOM", "CTRM", "NNDM", "GNUS", "OCGN",
    "FCEL", "IDEX", "CENN", "MULN", "PLUG", "CEI", "TTOO", "SENS", "SOLO"
]

# Filters
min_volume = st.number_input("Minimum Volume (default: 1,000,000)", value=1000000)
min_gain = st.number_input("Minimum % Gain Today (default: 0%)", value=0)

if st.button("🔍 Find Top 10 Penny Stocks"):
    data = []
    with st.spinner("Fetching stock data..."):
        for ticker in penny_stocks_list:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info

                price = info.get("regularMarketPrice")
                rec_mean = info.get("recommendationMean")
                rec_key = info.get("recommendationKey")
                name = info.get("shortName")
                volume = info.get("volume")
                change_percent = info.get("regularMarketChangePercent")

                if (
                    price and price < 5 and rec_mean and
                    volume and volume >= min_volume and
                    change_percent and change_percent >= min_gain
                ):
                    data.append({
                        "Ticker": ticker,
                        "Company": name,
                        "Price": price,
                        "Rec Mean (1=Strong Buy)": rec_mean,
                        "Recommendation": rec_key,
                        "Volume": volume,
                        "% Change": round(change_percent, 2)
                    })
            except Exception:
                pass

    if data:
        df = pd.DataFrame(data)
        df = df.sort_values(by="Rec Mean (1=Strong Buy)").head(10)
        st.success("✅ Top Penny Stocks by Analyst Rating:")
        st.dataframe(df)

        # Interactive Chart for Selected Stock
        stock_choice = st.selectbox("Select a stock to view chart:", df["Ticker"].tolist())
        if stock_choice:
            chart_data = yf.download(stock_choice, period="1mo", interval="1d")
            fig = go.Figure(data=[go.Candlestick(
                x=chart_data.index,
                open=chart_data['Open'],
                high=chart_data['High'],
                low=chart_data['Low'],
                close=chart_data['Close']
            )])
            fig.update_layout(title=f"{stock_choice} - Last 1 Month", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig)

        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="top_penny_stocks.csv", mime="text/csv")
    else:
        st.warning("No penny stocks matched the filters.")