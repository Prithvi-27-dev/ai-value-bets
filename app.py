# app.py
# (Streamlit app content placeholder)
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Value Bets", layout="wide")
st.title("⚽ AI-Powered Soccer Value Bets")
st.markdown("This is a live demo using simulated AI predictions + bookmaker odds. Value bets are shown below 👇")

# ---------------------
# Simulated AI Predictions (from Predicd)
ai_predictions = [
    {"match": "Liverpool vs Man City", "market": "1X2", "prediction": "Liverpool", "confidence": 0.72},
    {"match": "PSG vs Lyon", "market": "Over/Under 2.5", "prediction": "Over", "confidence": 0.81},
    {"match": "Arsenal vs Chelsea", "market": "BTTS", "prediction": "Yes", "confidence": 0.65},
    {"match": "Bayern vs Dortmund", "market": "1X2", "prediction": "Dortmund", "confidence": 0.62},
    {"match": "Inter vs AC Milan", "market": "BTTS", "prediction": "No", "confidence": 0.56}
]

# ---------------------
# Simulated Bookmaker Odds (from ValuePlus)
bookie_odds = [
    {"match": "Liverpool vs Man City", "market": "1X2", "outcome": "Liverpool", "odds": 2.10},
    {"match": "PSG vs Lyon", "market": "Over/Under 2.5", "outcome": "Over", "odds": 1.90},
    {"match": "Arsenal vs Chelsea", "market": "BTTS", "outcome": "Yes", "odds": 2.00},
    {"match": "Bayern vs Dortmund", "market": "1X2", "outcome": "Dortmund", "odds": 2.60},
    {"match": "Inter vs AC Milan", "market": "BTTS", "outcome": "No", "odds": 2.30}
]

# ---------------------
# Match predictions with odds and compute value
value_bets = []

for pred in ai_predictions:
    for odd in bookie_odds:
        if (
            pred["match"] == odd["match"]
            and pred["market"] == odd["market"]
            and pred["prediction"] == odd["outcome"]
        ):
            value = (odd["odds"] * pred["confidence"]) - 1
            value_bets.append({
                "Match": pred["match"],
                "Market": pred["market"],
                "Prediction": pred["prediction"],
                "AI Confidence": round(pred["confidence"], 2),
                "Bookie Odds": odd["odds"],
                "Expected Value": round(value, 3),
                "Value Bet?": "✅" if value > 0 else "❌"
            })

# Convert to DataFrame
df = pd.DataFrame(value_bets)

if df.empty:
    st.warning("No positive-value bets found today. Try again later.")
else:
    st.success(f"🎯 {len(df[df['Expected Value'] > 0])} high-value bets found!")
    st.dataframe(df[df["Expected Value"] > 0].sort_values(by="Expected Value", ascending=False), use_container_width=True)