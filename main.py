import os
import time
import requests
from threading import Thread
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run_web).start()

TOKEN = "8951520880:AAH2pk8-MbFzzjeWJx2YgIc3QsctQjF2HIc"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"
session = requests.Session()

def send_message(chat_id, text, reply_to_id=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_to_id:
        payload["reply_to_message_id"] = reply_to_id
    try:
        session.post(BASE_URL + "sendMessage", json=payload, timeout=5)
    except Exception:
        pass

def get_updates(offset=None):
    params = {"timeout": 10, "limit": 20}
    if offset:
        params["offset"] = offset
    try:
        r = session.get(BASE_URL + "getUpdates", params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("result", [])
    except Exception:
        pass
    return []

print("⚡ 24/7 Active Escrow Bot Started!")
init_updates = get_updates(-1)
offset = init_updates[-1]["update_id"] + 1 if init_updates else None

while True:
    try:
        msgs = get_updates(offset)
        for u in msgs:
            offset = u["update_id"] + 1
            if "message" in u and "text" in u["message"]:
                m = u["message"]
                t = m["text"].strip()
                cid = m["chat"]["id"]
                mid = m["message_id"]

                if t.startswith("/start"):
                    welcome = (
                        "👋 *Welcome to ACTIVE ESCROW SERVICE!*\n\n"
                        "🛡️ *Support / Owner:* @ACTICE_HERE\n\n"
                        "🚀 Fees calculate karne ke liye type karein:\n"
                        "`/fees 5000`"
                    )
                    send_message(cid, welcome, mid)

                elif t.lower().startswith("/fees"):
                    parts = t.split()
                    if len(parts) < 2:
                        send_message(cid, "⚠️ Sahi format: `/fees 5000`", mid)
                    else:
                        try:
                            amt = float(parts[1].replace(",", ""))
                            fee = (amt * 5) / 100
                            total = amt + fee
                            reply = (
                                f"🛡️ *ACTIVE ESCROW SERVICE (5%)*\n\n"
                                f"• *Amount:* ₹{amt:,.2f}\n"
                                f"• *Fee:* ₹{fee:,.2f}\n"
                                f"• *Total:* ₹{total:,.2f}\n\n"
                                f"👤 *Support / Owner:* @ACTICE_HERE"
                            )
                            send_message(cid, reply, mid)
                        except ValueError:
                            send_message(cid, "❌ Galat number!", mid)
        time.sleep(0.5)
    except Exception:
        time.sleep(2)
  
