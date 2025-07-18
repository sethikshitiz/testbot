from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming:", data)

    msg = data.get("text", "").lower()
    sender = data.get("waId")
    name = data.get("senderName", "there")

    if "@bot" in msg:
        reply = f"👋 Hello {name}! I'm active and ready."
        # Respond in WATI-compatible format
        return jsonify({
            "recipient": sender,
            "message": reply
        })

    return jsonify({"status": "ok"})

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
