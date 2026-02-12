# Admin Authentication Setup

## Overview
A JWT-based authentication system for protecting admin endpoints.

## Hardcoded Admin Credentials
```
Email: admin@example.com
Password: admin123

Email: admin
Password: password123
```

## Usage Flow

### 1. Login (Get Token)
**POST** `/login`

Request body:
```json
{
    "email": "admin@example.com",
    "password": "admin123"
}
```

Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "message": "Login successful for admin@example.com"
}
```

### 2. Use Token for Protected Endpoints
Add the token to the Authorization header:
```
Authorization: Bearer <access_token>
```

Example - POST `/ingest/sitemap`:
```bash
curl -X POST http://localhost:8000/ingest/sitemap \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"sitemap_url": "https://example.com/sitemap.xml"}'
```

## Protected Endpoints
- `POST /ingest/sitemap` - Requires valid token

## Token Expiration
Tokens expire after 24 hours. Login again to get a new token.

## Configuration
To use a custom secret key, set the `SECRET_KEY` environment variable:
```bash
export SECRET_KEY="your-secret-key-here"
```

## Module Location
Auth logic is in: `/core/loginAuth.py`
