from fastapi import APIRouter
from backend.app.api.v1.weather import router as weather_router
from backend.app.api.v1.warnings import router as warnings_router
from backend.app.api.v1.chat import router as chat_router
from backend.app.api.v1.language import router as language_router
from backend.app.api.v1.location import router as location_router
from backend.app.api.v1.climate import router as climate_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(weather_router)
api_router.include_router(warnings_router)
api_router.include_router(chat_router)
api_router.include_router(language_router)
api_router.include_router(location_router)
api_router.include_router(climate_router)
