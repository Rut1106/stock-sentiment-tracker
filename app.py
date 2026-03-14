







# import streamlit as st
# import requests
# from textblob import TextBlob
# import plotly.express as px
# import pandas as pd

# # Setup secrets
# FINNHUB_KEY = st.secrets["FINNHUB_KEY"]
# NEWS_KEY = st.secrets["NEWS_KEY"]

# st.set_page_config(page_title="Magic Stock Tracker", layout="wide")
# st.title("📈 Magic Stock Sentiment Tracker")

# ticker = st.sidebar.text_input("Enter Ticker:", "AAPL").upper()

# if ticker:
#     # 1. Fetch Data
#     price_url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
#     news_url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_KEY}&pageSize=10"
    
#     price_data = requests.get(price_url).json()
#     news_data = requests.get(news_url).json()

#     # 2. Metrics UI
#     c1, c2, c3 = st.columns(3)
#     c1.metric("Current Price", f"${price_data.get('c', 0)}")
#     c2.metric("Change", f"{price_data.get('dp', 0)}%")
#     c3.metric("High", f"${price_data.get('h', 0)}")

#     # 3. Sentiment Analysis
#     articles = news_data.get('articles', [])
#     sentiments = [TextBlob(a['title']).sentiment.polarity for a in articles]
    
#     # Visual Magic: Simple Sentiment Chart
#     df = pd.DataFrame({'Sentiment': sentiments})
#     fig = px.histogram(df, x='Sentiment', nbins=10, title="News Sentiment Distribution")
#     st.plotly_chart(fig, use_container_width=True)

#     # 4. News Tabs
#     tab1, tab2 = st.tabs(["Positive Headlines", "Negative Headlines"])
#     with tab1:
#         for a in articles:
#             if TextBlob(a['title']).sentiment.polarity > 0: st.success(a['title'])
#     with tab2:
#         for a in articles:
#             if TextBlob(a['title']).sentiment.polarity < 0: st.error(a['title'])




import streamlit as st
import requests
from textblob import TextBlob
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Setup
FINNHUB_KEY = st.secrets["FINNHUB_KEY"]
NEWS_KEY = st.secrets["NEWS_KEY"]

st.set_page_config(page_title="Hybrid Stock Predictor", layout="wide")
st.title("🤖 AI-Driven Stock Sentiment & Prediction")

ticker = st.sidebar.text_input("Enter Ticker:", "AAPL").upper()

if ticker:
    # 1. Fetch Data
    price_url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
    news_url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_KEY}&pageSize=10"
    
    price_data = requests.get(price_url).json()
    news_data = requests.get(news_url).json()

    # 2. Display Metrics
    c1, c2, c3 = st.columns(3)
    current_price = price_data.get('c', 0)
    c1.metric("Current Price", f"${current_price}")
    c2.metric("Change", f"{price_data.get('dp', 0)}%")
    
    # 3. Sentiment Logic
    articles = news_data.get('articles', [])
    sentiments = [TextBlob(a['title']).sentiment.polarity for a in articles]
    avg_sentiment = np.mean(sentiments) if sentiments else 0
    c3.metric("Avg News Sentiment", f"{avg_sentiment:.2f}")

    # 4. Hybrid Prediction Model
    # Simulate historical data (Last 3 days for demo purposes)
    X = np.array([[150.0, 0.1], [152.0, 0.2], [151.0, -0.1]]) # [Price, Sentiment]
    y = np.array([152.0, 151.0, 153.0]) # Next Day Close
    
    model = LinearRegression()
    model.fit(X, y)
    
    prediction = model.predict([[current_price, avg_sentiment]])[0]
    st.success(f"Predicted Next Closing Price: ${prediction:.2f}")

    # 5. Visuals
    df = pd.DataFrame({'Sentiment': sentiments})
    fig = px.histogram(df, x='Sentiment', title="News Sentiment Distribution")
    st.plotly_chart(fig, use_container_width=True)