import requests

class Notifier:
    def __init__(self, tg_token, tg_chat_id):
        self.TG_TOKEN = tg_token
        self.TG_CHAT_ID = tg_chat_id


    def send_telegram(self, message):
        if not (self.TG_TOKEN and self.TG_CHAT_ID):
            print("Telegram not configured.")
            return
        url = f"https://api.telegram.org/bot{self.TG_TOKEN}/sendMessage"
        payload = {"chat_id": self.TG_CHAT_ID, "text": message}
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
        print("Telegram sent.")