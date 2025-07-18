from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key (you’ll add this later in the environment variables)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Incoming:", data)

    user_msg = data.get("text", "")
    phone_number = data.get("waId", "")  # WhatsApp number

    if "summarize" in user_msg.lower():
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a WhatsApp group assistant that summarizes recent chat."},
                {"role": "user", "content": "Summarize the last 24 hours of our group chat."}
            ]
        )
        reply = response['choices'][0]['message']['content']
    else:
        reply = "Hi 👋 I'm your WhatsApp memory bot. Type 'summarize' to try me out."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
