import pandas as pd
from predictions import get_predictions
from odds_scraper import get_odds
from email_sender import send_value_bets_email
from cache_manager import get_today_cache, add_to_cache
from value_calc import value_percent

def main():
    preds = pd.DataFrame(get_predictions())
    odds = pd.DataFrame(get_odds())
    df = pd.merge(preds, odds, on=["Match", "Market"], how="inner")
    df["AI Confidence"] = pd.to_numeric(df["AI Confidence"], errors="coerce")
    df["Bookie Odds"]   = pd.to_numeric(df["Bookie Odds"], errors="coerce")

    df["Value %"] = df.apply(lambda r: value_percent(r["AI Confidence"], r["Bookie Odds"]), axis=1)
    df["Value Bet?"] = df["Value %"].gt(0).map({True: "✅", False: "❌"})

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

    records = value_bets.to_dict(orient="records")
    ok, msg = send_value_bets_email(records)
    if ok and records:
        add_to_cache(records)
    print(msg if ok else f"FAILED: {msg}")

if __name__ == "__main__":
    main()