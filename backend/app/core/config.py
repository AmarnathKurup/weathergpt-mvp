import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: List[str] = ["*"]

    IMD_API_KEY: str = ""
    IMD_BASE_URL: str = "https://mausam.imd.gov.in/api"

    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"

    DEFAULT_LLM_PROVIDER: str = "local"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"

    BHASHINI_USER_ID: str = ""
    BHASHINI_API_KEY: str = ""
    BHASHINI_PIPELINE_ID: str = ""
    BHASHINI_BASE_URL: str = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

    PINCODE_DATA_PATH: str = "data/pincode/pincode.csv"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
