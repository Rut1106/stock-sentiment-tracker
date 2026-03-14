import streamlit as st
import requests

# Setup
FINNHUB_KEY = st.secrets["FINNHUB_KEY"]
NEWS_KEY = st.secrets["NEWS_KEY"]

st.title("Live Stock Sentiment Tracker 📈")
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", "AAPL")

if ticker:
    # 1. Fetch Real-time Price from Finnhub
    price_url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
    price_data = requests.get(price_url).json()
    
    # 2. Fetch News from NewsAPI
    news_url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_KEY}&pageSize=5"
    news_data = requests.get(news_url).json()

    # Display results
    col1, col2 = st.columns(2)
    col1.metric("Current Price", f"${price_data.get('c')}")
    col2.metric("High of Day", f"${price_data.get('h')}")

    st.subheader(f"Latest News for {ticker}")
    for article in news_data.get('articles', []):
        st.write(f"**{article['title']}**")
        st.caption(f"Source: {article['source']['name']}")