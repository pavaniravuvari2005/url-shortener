from flask import Flask, request, jsonify, redirect
import string
import random

app = Flask(__name__)

url_mapping = {}

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route("/")
def home():
    return jsonify({"message": "URL Shortener API is running"})

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    url_mapping[short_code] = original_url

    short_url = request.host_url + short_code
    return jsonify({"short_url": short_url})

@app.route("/<short_code>")
def redirect_url(short_code):
    original_url = url_mapping.get(short_code)
    if original_url:
        return redirect(original_url)
    return jsonify({"error": "URL not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
