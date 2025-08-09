import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv


load_dotenv()


def send_value_bets_email(matches):
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL", sender)
    debug_flag = os.getenv("DEBUG_EMAIL", "0") == "1"

    if not sender or not password:
        return False, "Missing GMAIL_ADDRESS or GMAIL_APP_PASSWORD env vars."
    if not recipient:
        return False, "Missing RECIPIENT_EMAIL and no sender fallback."

    subject = "📬 Today's AI Value Bets"
    lines = []
    for m in matches:
        ai_conf = float(m.get("AI Confidence", 0) or 0)
        value_pct = float(m.get("Value %", 0) or 0)
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

    # Safe debug print (masked addresses, lengths only)
    safe_sender = sender[:3] + "…" + sender[-7:]
    safe_recipient = recipient[:3] + "…" + recipient[-7:]
    if debug_flag:
        print(f"[DEBUG] Preparing to send email")
        print(f"[DEBUG] From: {safe_sender}  To: {safe_recipient}")
        print(f"[DEBUG] Subject: {subject}")
        print(f"[DEBUG] Body lines: {len(lines)} (empty means sending fallback text)")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            if debug_flag:
                # Enable SMTP protocol debugging (no password is printed)
                server.set_debuglevel(1)
            server.login(sender, password)
            server.sendmail(sender, [recipient], msg.as_string())
        return True, f"Email sent successfully to {safe_recipient} from {safe_sender}. {len(lines)} lines."
    except Exception as e:
        return False, f"SMTP error: {e}"
