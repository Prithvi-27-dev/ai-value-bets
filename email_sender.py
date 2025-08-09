import smtplib
from email.mime.text import MIMEText
from email.mime_multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_value_bets_email(matches):
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = sender

    subject = "📬 Today's AI Value Bets"
    lines = []
    for m in matches:
        try:
            ai_conf = float(m.get("AI Confidence", 0))
        except Exception:
            ai_conf = 0.0
        try:
            value_pct = float(m.get("Value %", 0))
        except Exception:
            value_pct = 0.0
        line = (
            f"{m['Match']} — {m['Market']} → {m['Prediction']} "
            f"@ {m['Bookie Odds']} (AI: {ai_conf:.0f}%, Value: {value_pct:.1f}%)"
        )
        if m.get("Value Bet?") == "✅":
            line += " ✅"
        lines.append(line)
    body = "\n".join(lines) if lines else "No new value bets today."

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        return True, "Email sent successfully!"
    except Exception as e:
        return False, str(e)
