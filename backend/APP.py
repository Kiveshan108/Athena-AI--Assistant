from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS if frontend/backend are on different ports

# Set your API key here, or use an environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyD7eMGnHbiN9Utal29HKkQRDQRwR3VQRs4")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("chat.html", bot_name="Athena")

@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        data = request.get_json()
        user_input = data.get("user_input", "").strip()

        if not user_input:
            return jsonify({"response": "Please type something first!"}), 400

        # Call Gemini API
        result = model.generate_content(user_input)
        bot_reply = result.text if result.text else "I didn't get a response. Try again?"

        return jsonify({"response": bot_reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Sorry, something went wrong on my end."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
