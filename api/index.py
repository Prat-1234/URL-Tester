from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import hashlib
import hmac
import datetime
import os
import requests
from dotenv import load_dotenv

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

MOHIT_SHARED_SECRET = os.getenv("MOHIT_SHARED_SECRET")
MOHIT_API_URL = os.getenv("MOHIT_API_URL")

app = Flask(__name__)
CORS(app)

# =========================
# RATE LIMITER
# =========================
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"]  # global limit
)

# =========================
# PUBLIC + LIMITED API
# =========================
@app.route("/check-url", methods=["POST"])
@limiter.limit("10 per minute")  # per IP limit
def check_url():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL missing"}), 400

    # ---- Secure hash-based trust with Mohit ----
    timestamp = str(int(datetime.datetime.utcnow().timestamp()))

    hashed_key = hmac.new(
        MOHIT_SHARED_SECRET.encode(),
        timestamp.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "X-INTERNAL-SECRET": hashed_key,
        "X-TIMESTAMP": timestamp
    }

    payload = {
        "url": url
    }

    try:
        response = requests.post(
            MOHIT_API_URL,
            json=payload,
            headers=headers,
            timeout=5
        )
    except requests.exceptions.RequestException:
        return jsonify({"error": "Mohit API unreachable"}), 503

    return jsonify(response.json()), response.status_code

# =========================
# HEALTH CHECK
# =========================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "API Gateway running",
        "access": "public",
        "rate_limit": "10 requests/minute per IP"
    })