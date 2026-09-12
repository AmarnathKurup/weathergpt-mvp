from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.location.pincode_service import pincode_service  # Fixed: removed backend.
from app.api.router import api_router                    # Fixed: removed backend.

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("================================================================")
    print(" WeatherGPT — Conversational Weather Intelligence Core starting")
    print("================================================================")
    # Index All India Pincode dataset on startup
    pincode_service.load_data()
    yield
    print("WeatherGPT Core backend shutdown.")

app = FastAPI(
    title="WeatherGPT API Core",
    description="Conversational Weather Intelligence Platform for India — IMD + Open-Meteo + BHASHINI + AI Decision Intelligence",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "online",
        "service": "WeatherGPT Weather Intelligence Core",
        "version": "1.0.0",
        "docs": "/docs",
        "authoritative_sources": ["India Meteorological Department (IMD)", "Open-Meteo NWP", "BHASHINI 22-Language AI"]
    }

if __name__ == "__main__":
    import uvicorn
    # Fixed: changed "backend.app.main:app" to "app.main:app"
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
