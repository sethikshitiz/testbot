from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔐 Replace with your actual WATI API token
WATI_API_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4NTM1MjUzNC0yNzc5LTRlZjItYTI5Ni1hNjM3NjllYjBkMmYiLCJ1bmlxdWVfbmFtZSI6ImtzaGl0aXouYml0c0BnbWFpbC5jb20iLCJuYW1laWQiOiJrc2hpdGl6LmJpdHNAZ21haWwuY29tIiwiZW1haWwiOiJrc2hpdGl6LmJpdHNAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDcvMTgvMjAyNSAxMjowODozMSIsInRlbmFudF9pZCI6IjQ3MDYyMSIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.Kygoi28MM3yp9wbHor9Y-ZXJnMTwUa5iy214-s5Am9E"
HEADERS = {
    "Authorization": f"Bearer {WATI_API_TOKEN}",
    "Content-Type": "application/json"
}

WATI_API_URL = "https://app-server.wati.io/api/v1/sendSessionMessage"

def send_whatsapp_message(phone_number, message):
    payload = {
        "phone": phone_number,
        "message": message
    }
    response = requests.post(WATI_API_URL, json=payload, headers=HEADERS)
    print("WATI response:", response.status_code, response.text)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming:", data)

    msg = data.get("text", "").lower()
    sender = data.get("waId")
    name = data.get("senderName", "there")

    if "@bot" in msg:
        reply = f"👋 Hello {name}! I'm active and listening."
        send_whatsapp_message(sender, reply)

    return jsonify({"status": "received"})

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
