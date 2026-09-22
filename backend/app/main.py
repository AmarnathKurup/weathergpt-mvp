import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.routers import alerts, chat, community, forecast, location, weather

logger = logging.getLogger("weathergpt")

settings = get_settings()

app = FastAPI(
    title="WeatherGPT MVP",
    description="Local MVP: FastAPI backend + AI weather agent",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all so unexpected errors (e.g. a bad LLM model name, upstream API
    hiccups) come back as a normal JSON 500 with CORS headers attached, instead
    of an unhandled ASGI error. Without this, the browser sees a response with
    no Access-Control-Allow-Origin header and reports it as a network failure
    ("Could not reach the backend") even though the backend is running fine -
    which hides the real error from the user.
    """
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": f"{type(exc).__name__}: {exc}"})


app.include_router(chat.router)
app.include_router(weather.router)
app.include_router(forecast.router)
app.include_router(alerts.router)
app.include_router(location.router)
app.include_router(community.router)


@app.get("/")
async def root():
    return {"status": "ok", "service": "WeatherGPT MVP backend"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "env": settings.app_env,
        "groq_configured": bool(settings.groq_api_key),
    }
