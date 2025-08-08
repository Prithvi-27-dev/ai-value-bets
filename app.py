import streamlit as st
import pandas as pd
from predictions import get_predictions
from odds_scraper import get_odds
from email_sender import send_value_bets_email
from cache_manager import get_today_cache, add_to_cache

st.set_page_config(page_title="AI Value Bets", layout="wide")
st.title("⚽ AI-Powered Value Bet Finder")

with st.spinner("Fetching predictions and odds..."):
    predictions = get_predictions()
    odds = get_odds()

df_pred = pd.DataFrame(predictions)
df_odds = pd.DataFrame(odds)
df = pd.merge(df_pred, df_odds, on=["Match", "Market"])
df["AI Confidence"] = df["AI Confidence"].str.rstrip("%").astype(float)
df["Value %"] = (df["AI Confidence"] / (df["Bookie Odds"].astype(float) * 100) * 10000).round(2)
df["Value Bet?"] = df["Value %"].apply(lambda x: "✅" if x > 0 else "❌")

# Load today's cached matches
cached = get_today_cache()
def is_new(match_row):
    match_dict = {
        "Match": match_row["Match"],
        "Market": match_row["Market"],
        "Prediction": match_row["Prediction"],
        "Bookie Odds": match_row["Bookie Odds"],
        "AI Confidence": f"{match_row['AI Confidence']}%"
    }
    return tuple(match_dict.items()) not in cached

value_bets = df[df["Value Bet?"] == "✅"].copy()
value_bets = value_bets[value_bets.apply(is_new, axis=1)].reset_index(drop=True)

st.subheader("🔍 Top Value Bets Today (Uncached)")
st.dataframe(value_bets, use_container_width=True)

if st.button("📩 Send Email with Value Bets"):
    records = value_bets.to_dict(orient="records")
    if records:
        success, msg = send_value_bets_email(records)
        if success:
            add_to_cache(records)
            st.success(msg)
        else:
            st.error(f"Failed to send email: {msg}")
    else:
        st.info("No new value bets to email today.")