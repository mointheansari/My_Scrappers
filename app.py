from flask import Flask, jsonify, request, abort
from scraper import run_scraper
import os

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

@app.route("/")
def home():
    return "Service running"

@app.route("/run", methods=["GET"])
def run():
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        abort(403)

    data = run_scraper()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
