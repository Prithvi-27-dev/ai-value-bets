
import streamlit as st
from odds_scraper import get_odds
from predictions import get_predictions
import pandas as pd

st.set_page_config(page_title="AI Value Bets", layout="centered")

st.title("⚽ AI-Powered Value Bets")
st.markdown("Daily predictions + bookmaker odds to find the best betting opportunities.")

# Load simulated data
predictions = get_predictions()
odds = get_odds()

# Merge predictions and odds
value_bets = []
for pred in predictions:
    for odd in odds:
        if pred["match"] == odd["match"] and pred["market"] == odd["market"] and pred["prediction"] == odd["outcome"]:
            confidence = pred["confidence"]
            bookmaker_odds = odd["odds"]
            value = (bookmaker_odds * confidence) - 1
            value_bets.append({
                "Match": pred["match"],
                "Market": pred["market"],
                "Prediction": pred["prediction"],
                "AI Confidence": f"{confidence:.0%}",
                "Bookie Odds": bookmaker_odds,
                "Value %": f"{value * 100:.1f}%",
                "Value Bet?": "✅" if value > 0 else "❌"
            })

if value_bets:
    df = pd.DataFrame(value_bets)
    st.success("🎯 Top Value Bets Today")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No value bets found today.")
