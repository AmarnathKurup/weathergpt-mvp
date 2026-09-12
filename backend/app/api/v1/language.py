from fastapi import APIRouter
from typing import List, Dict
from backend.app.schemas.language import TranslateRequest, TranslationResponse
from backend.app.language.language_service import language_service
from backend.app.language.bhashini_adapter import bhashini_adapter

router = APIRouter(prefix="/language", tags=["Language & Multilingual"])

@router.get("/supported", response_model=List[Dict[str, str]])
async def get_supported_languages():
    return language_service.get_supported_languages()

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(req: TranslateRequest):
    translated = await bhashini_adapter.translate(
        text=req.text,
        target_lang=req.target_language,
        source_lang=req.source_language
    )
    return TranslationResponse(
        original_text=req.text,
        translated_text=translated,
        source_language=req.source_language,
        target_language=req.target_language,
        provider="BHASHINI / WeatherGPT Multilingual Core"
    )
