# app.py
# (Streamlit app content placeholder)
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="AI Value Bets", layout="wide")

# Page title and info
st.title("⚽ AI-Powered Soccer Value Bets")
st.markdown("✅ This is a working test dashboard. Live data will be added next.")

# Example table data
sample_data = {
    "Match": ["Man City vs Arsenal", "PSG vs Marseille"],
    "Market": ["1X2", "Over 2.5 Goals"],
    "Prediction": ["Man City", "Over"],
    "AI Confidence": [0.81, 0.77],
    "Bookie Odds": [2.10, 1.88],
    "Value Bet?": ["✅", "✅"]
}

df = pd.DataFrame(sample_data)

# Display table
st.dataframe(df, use_container_width=True)