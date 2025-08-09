import streamlit as st
import pandas as pd
from predictions import get_predictions
from odds_scraper import get_odds
from email_sender import send_value_bets_email
from cache_manager import get_today_cache, add_to_cache
from value_calc import value_percent, edge_percent

st.set_page_config(page_title="AI Value Bets", layout="wide")
st.title("⚽ AI-Powered Value Bet Finder")

with st.spinner("Fetching predictions and odds..."):
    predictions = get_predictions()
    odds = get_odds()

df_pred = pd.DataFrame(predictions)
df_odds = pd.DataFrame(odds)

# Merge & coerce types
df = pd.merge(df_pred, df_odds, on=["Match", "Market"], how="inner")
df["AI Confidence"] = pd.to_numeric(df["AI Confidence"], errors="coerce")
df["Bookie Odds"]   = pd.to_numeric(df["Bookie Odds"], errors="coerce")

# Correct value math
df["Value %"] = df.apply(lambda r: value_percent(r["AI Confidence"], r["Bookie Odds"]), axis=1)
df["Edge %"]  = df.apply(lambda r: edge_percent(r["AI Confidence"], r["Bookie Odds"]), axis=1)

# Flag value
df["Value Bet?"] = df["Value %"].gt(0).map({True: "✅", False: "❌"})

# Filter uncached value bets
cached = get_today_cache()
def is_new(row):
    d = {
        "Match": row["Match"],
        "Market": row["Market"],
        "Prediction": row["Prediction"],
        "Bookie Odds": str(row["Bookie Odds"]),
        "AI Confidence": float(row["AI Confidence"]),
        "Value %": float(row["Value %"]),
        "Value Bet?": row["Value Bet?"],
    }
    return tuple(d.items()) not in cached

value_bets = df[df["Value Bet?"] == "✅"].copy()
value_bets = value_bets[value_bets.apply(is_new, axis=1)].reset_index(drop=True)

# Display nicely
disp = value_bets.copy()
disp["AI Confidence"] = disp["AI Confidence"].round(1)
disp["Bookie Odds"]   = disp["Bookie Odds"].round(2)
disp["Value %"]       = disp["Value %"].round(1)
disp["Edge %"]        = disp["Edge %"].round(1)

st.subheader("🔍 Top Value Bets Today (Uncached)")
st.dataframe(disp, use_container_width=True)

# Email button
if st.button("📩 Send Email with Value Bets"):
    records = disp.to_dict(orient="records")
    if records:
        success, msg = send_value_bets_email(records)
        if success:
            add_to_cache(records)
            st.success(msg)
        else:
            st.error(f"Failed to send email: {msg}")
    else:
        st.info("No new value bets to email today.")