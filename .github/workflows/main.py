from flask import Flask, request, jsonify
import requests
import oshttps://github.com/sethikshitiz/testbot/blob/main/.github/workflows/main.py

app = Flask(__name__)

WATI_API_URL = "https://live-mt-server.wati.io/470621/api/v1/sendSessionMessage"
WATI_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4NTM1MjUzNC0yNzc5LTRlZjItYTI5Ni1hNjM3NjllYjBkMmYiLCJ1bmlxdWVfbmFtZSI6ImtzaGl0aXouYml0c0BnbWFpbC5jb20iLCJuYW1laWQiOiJrc2hpdGl6LmJpdHNAZ21haWwuY29tIiwiZW1haWwiOiJrc2hpdGl6LmJpdHNAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDcvMTgvMjAyNSAxMjowODozMSIsInRlbmFudF9pZCI6IjQ3MDYyMSIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.Kygoi28MM3yp9wbHor9Y-ZXJnMTwUa5iy214-s5Am9E"  # full token

@app.route("/", methods=["GET"])
def home():
    return "Bot is live ✅"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📨 Incoming webhook:", data)

    try:
        phone_number = data["waId"] or data["sender"]
        message_text = data["text"] or data["message"]
    except Exception as e:
        return jsonify({"error": "Invalid webhook format"}), 400

    # Compose reply
    reply = "Hi! You said: " + message_text

    # Call WATI API to send reply
    payload = {
        "phone": phone_number,
        "message": reply
    }
    headers = {
        "Authorization": f"Bearer {WATI_TOKEN}",
        "Content-Type": "application/json"
    }

    wati_response = requests.post(WATI_API_URL, json=payload, headers=headers)
    print("📤 Sent to WATI:", wati_response.status_code, wati_response.text)

    if wati_response.status_code == 200:
        return jsonify({"status": "sent"})
    else:
        return jsonify({"error": "WATI send failed", "wati_response": wati_response.text}), 401

if __name__ == "__main__":
    app.run(debug=True)
