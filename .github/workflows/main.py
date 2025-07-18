from flask import Flask, request, jsonify
import requests
import openai

app = Flask(__name__)

# === CONFIGURATION ===
WATI_API_URL = "https://app-server.wati.io/api/v1/sendSessionMessage"
WATI_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4NTM1MjUzNC0yNzc5LTRlZjItYTI5Ni1hNjM3NjllYjBkMmYiLCJ1bmlxdWVfbmFtZSI6ImtzaGl0aXouYml0c0BnbWFpbC5jb20iLCJuYW1laWQiOiJrc2hpdGl6LmJpdHNAZ21haWwuY29tIiwiZW1haWwiOiJrc2hpdGl6LmJpdHNAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDcvMTgvMjAyNSAxMjowODozMSIsInRlbmFudF9pZCI6IjQ3MDYyMSIsImRiX25hbWUiOiJtdC1wcm9kLVRlbmFudHMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.Kygoi28MM3yp9wbHor9Y-ZXJnMTwUa5iy214-s5Am9E"  # Replace with your real WATI Bearer token
GPT_API_KEY = "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"       # Replace with your OpenAI API key

# Initialize OpenAI
openai.api_key = GPT_API_KEY

def send_reply(phone_number, message_text):
    """Send a message via WATI"""
    headers = {
        "Authorization": WATI_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "phone": phone_number,
        "message": message_text
    }

    response = requests.post(WATI_API_URL, json=payload, headers=headers)
    print("WATI Response:", response.status_code, response.text)
    return response.status_code == 200

def get_gpt_response(prompt):
    """Get response from OpenAI GPT"""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you have access
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI Error:", e)
        return "I'm having trouble thinking right now 😔"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Incoming:", data)

    try:
        text = data.get("text", "")
        sender_number = data.get("waId")

        if "@bot" in text.lower():
            user_prompt = text.replace("@bot", "").strip()
            print("User Prompt:", user_prompt)

            gpt_reply = get_gpt_response(user_prompt)
            print("GPT Reply:", gpt_reply)

            success = send_reply(sender_number, gpt_reply)
            return jsonify({"status": "sent" if success else "failed"}), 200

        return jsonify({"status": "ignored"}), 200

    except Exception as e:
        print("Webhook Error:", e)
        return jsonify({"status": "error"}), 500

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
