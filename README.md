# 🔗 URL Tester — Secure API Gateway

> A Flask-based API Gateway that validates URLs through a trusted internal service,
> with HMAC authentication, rate limiting, and CORS support.

---

## 📌 Overview

This project acts as a **public-facing API gateway** that accepts URL check requests,
signs them with a time-based HMAC secret, and forwards them securely to an internal
backend API. It prevents abuse via per-IP rate limiting and protects backend
communication using shared-secret authentication.

---

## 🚀 Features

- 🔐 **HMAC-SHA256 authentication** — time-based signed requests to the internal API
- 🚦 **Rate limiting** — 10 requests/minute per IP, 100/hour globally
- 🌐 **CORS enabled** — accessible from any frontend
- ❤️ **Health check endpoint** — `/health` for monitoring
- 🔒 **Environment-based secrets** — no hardcoded credentials via `.env`

---

## 🛠️ Tech Stack

| Component | Tool |
|-----------|------|
| Framework | Flask |
| Auth | HMAC-SHA256 + timestamp |
| Rate Limiting | Flask-Limiter |
| HTTP Client | requests |
| Config | python-dotenv |
| CORS | Flask-CORS |

---

## ⚙️ Setup & Run

```bash
git clone https://github.com/Prat-1234/URL-Tester.git
cd URL-Tester
pip install -r requirements.txt
```

Create a `.env` file:
```env
MOHIT_SHARED_SECRET=your_shared_secret_here
MOHIT_API_URL=https://your-internal-api/endpoint
```

Run the server:
```bash
python app.py
```

---

## 📡 API Endpoints

### `POST /check-url`
Checks a URL via the internal backend.

**Request:**
```json
{ "url": "https://example.com" }
```

**Response:** Returns the internal API's result with status code.

**Rate limit:** 10 requests/minute per IP

---

### `GET /health`
Returns gateway status and rate limit info.

```json
{
  "status": "API Gateway running",
  "access": "public",
  "rate_limit": "10 requests/minute per IP"
}
```

---

## 🔒 Security Design
Client → [Public API Gateway] → HMAC Sign → [Internal Backend API]
(rate limited)     (timestamp)     (validates secret)

Every forwarded request includes:
- `X-INTERNAL-SECRET` — HMAC-SHA256 hash of the current UTC timestamp
- `X-TIMESTAMP` — UTC timestamp used for signing (prevents replay attacks)

---

## 📂 Project Structure
URL-Tester/

├── app.py              # Main Flask gateway

├── .env                # Secrets (never commit this)

├── .env.example        # Template for environment variables

├── requirements.txt    # Dependencies

└── README.md

---

## 🔮 Future Improvements

- Add JWT-based auth for public clients
- Log all URL check requests to DynamoDB or a file
- Deploy on AWS Lambda + API Gateway
- Add URL reputation scoring

---

## 👤 Author

**Prateek Kumar Singh**
[LinkedIn](https://linkedin.com/in/prateeksingh6394/) • [GitHub](https://github.com/Prat-1234) •
[Portfolio](https://prat-1234.github.io)
