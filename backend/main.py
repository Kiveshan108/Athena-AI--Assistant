import os

from flask import Flask, jsonify, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")


def athena_response(prompt):
    """
    Athena - Your intelligent AI assistant powered by Gemini.
    """
    # Athena's system persona embedded in the conversation
    athena_context = """You are Athena, a helpful, knowledgeable, and friendly AI assistant. 
You provide clear, accurate answers with a warm and professional tone. 
You excel at explaining complex topics simply and are always eager to help."""

    response = model.generate_content(
        contents=[
            {"role": "user", "parts": [{"text": f"{athena_context}\n\nUser: {prompt}"}]}
        ],
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=100,
            temperature=0.7,
        ),
    )
    return response.text.strip()


@app.route("/")
def home():
    return render_template("index.html", bot_name="Athena")


@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.json
    user_input = data.get("user_input")
    bot_response = athena_response(user_input)
    return jsonify({
        "response": bot_response,
        "bot_name": "Athena"
    })


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("HTTP_PORT", 5000))
