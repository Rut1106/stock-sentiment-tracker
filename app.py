# import streamlit as st
# import requests


# from textblob import TextBlob

# # ... inside your news loop:
   
# # Setup
# FINNHUB_KEY = st.secrets["FINNHUB_KEY"]
# NEWS_KEY = st.secrets["NEWS_KEY"]

# st.title("Live Stock Sentiment Tracker 📈")
# ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", "AAPL")

# if ticker:
#     # 1. Fetch Real-time Price from Finnhub
#     price_url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
#     price_data = requests.get(price_url).json()
    
#     # 2. Fetch News from NewsAPI
#     news_url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_KEY}&pageSize=5"
#     news_data = requests.get(news_url).json()

#     # Display results
#     col1, col2 = st.columns(2)
#     col1.metric("Current Price", f"${price_data.get('c')}")
#     col2.metric("High of Day", f"${price_data.get('h')}")

#     st.subheader(f"Latest News for {ticker}")
#     for article in news_data.get('articles', []):
#         st.write(f"**{article['title']}**")
#         # Add this:
#         analysis = TextBlob(article['title'])
#         sentiment = "Positive 🟢" if analysis.sentiment.polarity > 0 else "Negative 🔴" if analysis.sentiment.polarity < 0 else "Neutral ⚪"
#         st.write(f"Sentiment: {sentiment}")








import streamlit as st
import requests
from textblob import TextBlob
import plotly.express as px
import pandas as pd

# Setup secrets
FINNHUB_KEY = st.secrets["FINNHUB_KEY"]
NEWS_KEY = st.secrets["NEWS_KEY"]

st.set_page_config(page_title="Magic Stock Tracker", layout="wide")
st.title("📈 Magic Stock Sentiment Tracker")

ticker = st.sidebar.text_input("Enter Ticker:", "AAPL").upper()

if ticker:
    # 1. Fetch Data
    price_url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
    news_url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_KEY}&pageSize=10"
    
    price_data = requests.get(price_url).json()
    news_data = requests.get(news_url).json()

    # 2. Metrics UI
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Price", f"${price_data.get('c', 0)}")
    c2.metric("Change", f"{price_data.get('dp', 0)}%")
    c3.metric("High", f"${price_data.get('h', 0)}")

    # 3. Sentiment Analysis
    articles = news_data.get('articles', [])
    sentiments = [TextBlob(a['title']).sentiment.polarity for a in articles]
    
    # Visual Magic: Simple Sentiment Chart
    df = pd.DataFrame({'Sentiment': sentiments})
    fig = px.histogram(df, x='Sentiment', nbins=10, title="News Sentiment Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # 4. News Tabs
    tab1, tab2 = st.tabs(["Positive Headlines", "Negative Headlines"])
    with tab1:
        for a in articles:
            if TextBlob(a['title']).sentiment.polarity > 0: st.success(a['title'])
    with tab2:
        for a in articles:
            if TextBlob(a['title']).sentiment.polarity < 0: st.error(a['title'])