# monitor.py
import hashlib
import requests
import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage
from notifier import Notifier
import json

load_dotenv()

URL = os.getenv("MONITOR_URL")
HASH_FILE = "last_hash.txt"


def fetch_and_normalize(url):
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    text = r.text
    # minimal normalization: remove whitespace runs and script/style blocks could be removed later
    return " ".join(text.split())

def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def read_last_hash():
    if os.path.exists(HASH_FILE):
        return open(HASH_FILE).read().strip()
    return ""

def write_last_hash(h):
    with open(HASH_FILE, "w") as f:
        f.write(h)

# def send_email(subject, body):
#     SMTP_USER = os.environ.get("SMTP_USER")
#     SMTP_PASS = os.environ.get("SMTP_PASS")
#     RECIPIENT = os.environ.get("RECIPIENT_EMAIL")
#     if not (SMTP_USER and SMTP_PASS and RECIPIENT):
#         print("Email credentials not configured.")
#         return
#     msg = EmailMessage()
#     msg["From"] = SMTP_USER
#     msg["To"] = RECIPIENT
#     msg["Subject"] = subject
#     msg.set_content(body)
#     # Gmail/Outlook: use smtp.gmail.com:587 or smtp.office365.com
#     server = smtplib.SMTP(os.environ.get("SMTP_SERVER", "smtp.gmail.com"), int(os.environ.get("SMTP_PORT", 587)))
#     server.starttls()
#     server.login(SMTP_USER, SMTP_PASS)
#     server.send_message(msg)
#     server.quit()
#     print("Email sent.")



def main():

    if not URL:
        raise SystemExit("Set MONITOR_URL environment variable.")
    
    TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TG_CHAT = os.getenv("TELEGRAM_CHAT_ID")

    notifier = Notifier(TG_TOKEN, TG_CHAT)

    print("Fetching", URL)
    content = fetch_and_normalize(URL)
    h = sha256(content)
    last = read_last_hash()
    if h != last:
        print("Change detected!")
        subject = f"Change detected on {URL}"
        body = f"The content at {URL} changed.\n\nHash: {h}\n\nYou should check the page: {URL}"

        # send notifications you configured:
        try:
            notifier.send_telegram(body)
        except Exception as e:
            print("Telegram failed:", e)

        write_last_hash(h)
    else:
        print("No change.")

if __name__ == "__main__":
    main()
