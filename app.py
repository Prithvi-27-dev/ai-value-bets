# app.py
# (Streamlit app content placeholder)
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Value Bets", layout="wide")

st.title("⚽ AI-Powered Soccer Value Bets")

st.write("✅ This app is running. Live data and predictions coming soon.")

# Dummy data
data = {
    "Match": ["Arsenal vs Chelsea", "Real Madrid vs Barcelona"],
    "Market": ["1X2", "Over 2.5"],
    "Prediction": ["Arsenal", "Over"],
    "AI Confidence": [0.82, 0.76],
    "Odds": [2.1, 1.95],
    "Value Bet": ["✅", "✅"]
}

df = pd.DataFrame(data)

st.dataframe(df)