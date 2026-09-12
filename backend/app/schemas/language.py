from pydantic import BaseModel
from typing import Optional, List, Dict

class TranslateRequest(BaseModel):
    text: str
    source_language: str = "en"
    target_language: str = "hi"

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider: str = "BHASHINI / Built-in"

class SpeechToTextRequest(BaseModel):
    audio_base64: str
    language: str = "hi"

class SpeechToTextResponse(BaseModel):
    transcribed_text: str
    detected_language: str
    confidence: float = 0.95

class TextToSpeechRequest(BaseModel):
    text: str
    language: str = "hi"
    gender: str = "female"

class TextToSpeechResponse(BaseModel):
    text: str
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    language: str
