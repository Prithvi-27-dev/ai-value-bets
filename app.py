# app.py
# (Streamlit app content placeholder)
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Value Bets", layout="wide")

st.title("🔮 AI-Powered Soccer Value Bets")

st.write("This is a demo of today's predictions. Live data coming soon!")

# Sample table
sample_data = {
    "Match": ["Team A vs Team B", "Team C vs Team D"],
    "Predicted Winner": ["Team A", "Team D"],
    "AI Confidence": [0.78, 0.81],
    "Bookie Odds": [2.1, 1.9],
    "Market": ["1X2", "BTTS"],
    "Value Bet?": ["✅", "✅"]
}
df = pd.DataFrame(sample_data)

st.dataframe(df)