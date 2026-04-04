from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Athena AI API is running!", "status": "active"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("🦉 Athena AI Assistant Starting...")
    app.run(debug=True, port=5000)
