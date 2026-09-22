# WeatherGPT — Local MVP

A fully working local MVP of an AI-powered weather assistant: a Next.js dashboard/map/chat
frontend talking to a FastAPI backend, which fetches real weather data (Open-Meteo, NOAA/NWS)
and uses a Groq-hosted LLM (free tier) as a tool-calling agent.

This is intentionally a **local development MVP**, not production infrastructure. There's no
Docker, no database, no Redis, no cloud deployment — just two local dev servers.

```
weathergpt-mvp/
├── backend/     FastAPI app (Python)
└── frontend/    Next.js app (TypeScript/React)
```

## Architecture

```
Next.js frontend (dashboard, map, chat)
        │  fetch()
        ▼
FastAPI backend  /api/chat /api/weather /api/forecast /api/alerts /api/location
        │
        ├─► Weather services ─► Open-Meteo (current + forecast + geocoding, free, no key)
        │                    ─► NOAA/NWS alerts (free, US locations)
        │                    ─► OpenWeather (optional enrichment, if key provided)
        │
        ├─► WeatherGPT agent ─► Groq LLM (tool-calling) ─► calls the weather services above
        │
        ├─► Local meteorological knowledge base (IMD/monsoon/cyclone/heatwave/flood facts,
        │    simple keyword search over a local JSON file — no vector DB)
        │
        └─► Multilingual layer (langdetect + deep-translator) for non-English chat
```

In-memory TTL caching stands in for Redis. No database is used — data is fetched live from
free external APIs on each request (with short-lived in-memory caching).

## Prerequisites

- Python 3.11+ and pip
- Node.js 18+ and npm
- A free [Groq API key](https://console.groq.com/keys) (used for the chat agent's LLM)

## 1. Backend setup

**Python version matters:** use Python 3.11, 3.12, or 3.13. Python 3.14 is too new — some
dependencies (`pydantic-core`, a Rust extension) don't yet ship prebuilt wheels for it, so pip
tries to compile from source and fails unless you have a matching Rust toolchain. Using 3.11-3.13
avoids this entirely.

**Option A — plain venv:**

```bash
cd backend
python3.12 -m venv .venv        # use 3.11/3.12/3.13 specifically, not `python3` if that resolves to 3.14
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# then edit .env and set GROQ_API_KEY=your_key_here

uvicorn app.main:app --reload --port 8000
```

**Option B — conda:**

```bash
cd backend
conda create -n weathergpt python=3.12 -y
conda activate weathergpt
pip install -r requirements.txt

cp .env.example .env
# then edit .env and set GROQ_API_KEY=your_key_here

uvicorn app.main:app --reload --port 8000
```

Backend will be running at **http://localhost:8000**. Check http://localhost:8000/health and
http://localhost:8000/docs (interactive Swagger UI).

## 2. Frontend setup

In a second terminal:

```bash
cd frontend
npm install

cp .env.local.example .env.local
# defaults to NEXT_PUBLIC_API_BASE_URL=http://localhost:8000, edit if your backend runs elsewhere

npm run dev
```

Frontend will be running at **http://localhost:3000**.

## 3. Try it out

- **Dashboard** (`/`) — search a city or click 📍 for your location; see current conditions,
  a 7-day forecast strip, a composite **weather risk score**, active alerts/hazards, and an
  optional **Farmer Mode** for agriculture-specific advice.
- **Map** (`/map`) — interactive Leaflet map (OpenStreetMap tiles); click anywhere to check the
  weather at that point. Also shows and lets you submit **crowdsourced ground reports**
  (flooding, waterlogging, power outages, etc.) from people nearby.
- **Chat** (`/chat`) — ask WeatherGPT things like *"What's the weather right now?"*,
  *"Will it rain tomorrow?"*, *"Any alerts I should know about?"*, *"Any flooding reports near
  me?"*, *"Should I spray my crops today?"*, or general questions like *"What is a heatwave and
  how should I prepare?"*. The agent calls the real backend tools rather than guessing numbers —
  you'll see a small "🔧 used tools: ..." note under replies that needed live data. There's also
  a one-tap **🚨 Emergency Briefing** button that gets a full spoken safety summary immediately.

Multilingual: try typing in Hindi, Tamil, Spanish, etc. — the backend detects the language,
translates internally for the agent, and translates the reply back.

### What makes this more than a weather lookup app

- **🎯 Composite Weather Risk Score** — combines heat, wind, rain, and active alerts into one
  transparent 0-100 score with the contributing factors listed, so people get a fast read
  without parsing raw numbers. Rule-based and auditable (`analysis_service.compute_risk_score`),
  not a black box.
- **📢 Crowdsourced Ground-Truth Reports** — official weather/disaster data can lag reality
  during fast-moving events (flash flooding, localized waterlogging). Anyone nearby can report
  what's actually happening; it shows up on the map and the chat agent can reference it
  (`get_community_reports` tool) alongside official data, clearly labeled as user-submitted.
  Stored in-memory, auto-expires after 24h — no account or database needed for the MVP.
- **🌾 Farmer Advisory Mode** — turns raw forecast numbers into concrete agricultural decisions:
  whether it's a good window to spray pesticide/fertilizer (checks rain + wind), whether
  irrigation is needed (checks 3-day rain total), and livestock heat-stress risk. Available both
  as a dashboard toggle and a chat tool (`get_farmer_advisory`).
- **🚨 One-Tap Emergency Briefing** — a single button that asks the agent for a complete,
  safety-first briefing and reads it aloud immediately (bypassing the normal read-aloud toggle) —
  useful in a panic situation, for low-literacy users, or anyone who needs both hands free.

### Voice input/output

The Chat page has a 🎤 mic button and a 🔊 speaker button on each reply, plus a language
picker and a "read replies aloud" toggle. This uses the browser's **built-in Web Speech API**
(`SpeechRecognition` for voice-to-text, `speechSynthesis` for text-to-speech) — entirely
client-side, free, no API key, no backend involvement. Pick the language you're speaking
before hitting the mic (or leave it on the language that matches the reply you want read aloud).

Browser support: best in **Chrome and Edge** (desktop and Android). Safari has partial support;
Firefox does not support `SpeechRecognition` yet. If voice input isn't supported, the mic
button simply doesn't render — text chat still works everywhere. Available voices/languages
for text-to-speech depend on what's installed on the user's OS/browser.

## Environment variables

### `backend/.env` (see `backend/.env.example`)

| Variable | Required | Notes |
|---|---|---|
| `GROQ_API_KEY` | Yes, for chat | Free key from console.groq.com |
| `GROQ_MODEL` | No | Defaults to `llama-3.3-70b-versatile` |
| `OPENWEATHER_API_KEY` | No | Optional enrichment of current-weather descriptions |
| `CORS_ORIGINS` | No | Defaults to `http://localhost:3000` |
| `CACHE_TTL_SECONDS` | No | In-memory cache TTL, defaults to 600s |

### `frontend/.env.local` (see `frontend/.env.local.example`)

| Variable | Required | Notes |
|---|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | Yes | Defaults to `http://localhost:8000` |

## API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/weather?lat=&lon=` or `?name=` | Current weather |
| GET | `/api/weather/analysis?...` | Plain-language weather summary + risk score |
| GET | `/api/weather/farmer-advisory?...` | Farming-specific advisory (spray/irrigation/livestock) |
| GET | `/api/forecast?...&days=7` | Daily + hourly forecast |
| GET | `/api/alerts?...` | Official (NOAA/NWS) + generated hazard alerts |
| GET | `/api/location?q=` | Geocode a place name |
| GET | `/api/location/reverse?lat=&lon=` | Reverse geocode coordinates |
| GET | `/api/community/reports?lat=&lon=&radius_km=` | Nearby crowdsourced ground reports (last 24h) |
| POST | `/api/community/reports` | Submit a ground report (body: `{lat, lon, category, note?, location_name?}`) |
| POST | `/api/chat` | Conversational agent (body: `{message, history, lat?, lon?, location_name?, language?}`) |

Full interactive docs at `/docs` once the backend is running.

## Data sources used

- **[Open-Meteo](https://open-meteo.com/)** — current weather, forecast, and geocoding. Free,
  no API key required. Primary data source for the MVP.
- **[NOAA/NWS Alerts API](https://www.weather.gov/documentation/services-web-api)** — official
  active alerts, free, no key, but **US-only coverage**.
- **Generated hazard alerts** — for regions without a free structured alerts API (including
  India), the backend derives heatwave/heavy-rain/high-wind/thunderstorm alerts from
  IMD-style thresholds applied to the live current+forecast data.
- **OpenWeather** (optional) — if `OPENWEATHER_API_KEY` is set, its weather description is
  appended for extra color. Entirely optional; the MVP works fully without it.
- **Local knowledge base** (`backend/app/knowledge/data/domain_knowledge.json`) — basic
  IMD/monsoon/cyclone/heatwave/flood/AQI/disaster-preparedness facts used by the chat agent
  for conceptual questions.

Indian-government-specific structured APIs (IMD's own real-time feeds, MOSDAC/ISRO) generally
require registration/partnership access and aren't freely available for an MVP — the app
approximates this layer with the IMD-threshold-based hazard generation and local knowledge base
described above.

## What's intentionally NOT included

Per MVP scope, this project does **not** include: Redis, object storage, PostgreSQL/PostGIS,
production observability/metrics, Kubernetes, cloud deployment, production authentication,
message queues, or microservice infrastructure. Voice input/output uses the browser's free
built-in Web Speech API rather than a hosted STT/TTS service, to keep things simple.

## Testing the main flows manually

```bash
# Health
curl http://localhost:8000/health

# Current weather
curl "http://localhost:8000/api/weather?name=Mumbai"

# Forecast
curl "http://localhost:8000/api/forecast?name=Mumbai&days=5"

# Alerts
curl "http://localhost:8000/api/alerts?name=Mumbai"

# Location search
curl "http://localhost:8000/api/location?q=Mumbai"

# Chat (requires GROQ_API_KEY set)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather in Mumbai right now?", "history": []}'
```

## Troubleshooting

- **Chat returns a 500 "GROQ_API_KEY is not set"** — add your key to `backend/.env` and
  restart the backend.
- **Chat fails with "model does not exist or you do not have access to it" (in the backend
  terminal)** — Groq periodically deprecates/retires models. Check
  https://console.groq.com/docs/models for a currently supported model name, then update
  `GROQ_MODEL` in `backend/.env` (default is `openai/gpt-oss-120b`, current as of writing).
  This shows up as a specific 502 error in the browser, not a generic failure.
- **Frontend shows "Could not reach the WeatherGPT backend"** — this means the browser's
  `fetch()` call itself failed (no response at all), which usually means the backend process
  isn't running, or crashed with an error that had no CORS headers attached. Check the backend
  terminal for a traceback. If you see a Python exception there but the browser still shows
  "Could not reach", it means an older/unpatched build — the current version wraps all errors
  (including unexpected ones) in a proper JSON response with CORS headers, so they show as a
  real error message instead of a fake "can't reach" message. Make sure `NEXT_PUBLIC_API_BASE_URL`
  in `frontend/.env.local` also matches the backend's actual address (default
  `http://localhost:8000`).
- **CORS errors in the browser console** — check `CORS_ORIGINS` in `backend/.env` includes
  your frontend's origin (default `http://localhost:3000`).
- **Translation silently not happening** — `deep-translator` calls Google Translate over the
  network; if you're offline or on a restricted network, translation fails soft and the
  original text is returned rather than breaking the chat.
