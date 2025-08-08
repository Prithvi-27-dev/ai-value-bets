import streamlit as st
import pandas as pd
from predictions import get_predictions
from odds_scraper import get_odds
from email_sender import send_value_bets_email

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

st.subheader("🔍 Top Value Bets Today")
st.dataframe(df[df["Value Bet?"] == "✅"].reset_index(drop=True), use_container_width=True)

if st.button("📩 Send Email with Value Bets"):
    matches = df[df["Value Bet?"] == "✅"].to_dict(orient="records")
    success, msg = send_value_bets_email(matches)
    if success:
        st.success(msg)
    else:
        st.error(f"Failed to send email: {msg}")