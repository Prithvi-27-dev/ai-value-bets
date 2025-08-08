import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_value_bets_email(matches):
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = sender

    subject = "📬 Today's AI Value Bets"
    body = ""

    for match in matches:
        body += f"{match['Match']} — {match['Market']} → {match['Prediction']} @ {match['Bookie Odds']} (AI: {match['AI Confidence']})"
        if match.get("Value Bet?") == "✅":
            body += " ✅"
        body += "\n"

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