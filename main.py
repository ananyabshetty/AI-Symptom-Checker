import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow frontend communication

# Configure the Generative AI client
# IMPORTANT: Replace with your actual API key
genai.configure(api_key="Google-gemini-API-key")

# Initialize the chat session model
model = genai.GenerativeModel("gemini-1.5-flash")
chat1 = model.start_chat(
    history=[
        {"role": "user", "parts": ["Hello"]},
        {"role": "model", "parts": ["Great to meet you. I'm IRIS, your medical AI assistant. What symptoms are you experiencing?"]}
    ]
)

# Medical context prompt to guide the AI's responses
MEDICAL_CONTEXT_PROMPT = """
YOU ARE A PROFESSIONAL MEDICAL AI ASSISTANT NAMED IRIS:
- Provide clear, compassionate, and informative responses about medical symptoms
- Do not diagnose or replace professional medical advice
- Suggest possible causes and general wellness recommendations
- Recommend consulting a healthcare professional for definitive diagnosis
- Be empathetic and supportive in your communication

Analyze the following symptoms and provide insights:
"""

# Route for homepage
@app.route("/")
def home():
    return render_template("chat.html")

# Route for chat (API)
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Send the user's message to the chat session with medical context
        full_prompt = MEDICAL_CONTEXT_PROMPT + user_message
        response = chat1.send_message(full_prompt)

        # Log the response for debugging
        print(f"Raw Response: {response}")

        # Extract the reply
        bot_reply = response.text.strip()
        return jsonify({"reply": bot_reply})

    except Exception as e:
        # Handle and log errors
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred processing your request"}), 500

if __name__ == "__main__":
    app.run(debug=True)
