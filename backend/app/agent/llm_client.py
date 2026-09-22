from groq import Groq

from app.config import get_settings

_client: Groq | None = None


def get_client() -> Groq:
    global _client
    if _client is None:
        settings = get_settings()
        if not settings.groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to backend/.env (see .env.example)."
            )
        _client = Groq(api_key=settings.groq_api_key)
    return _client
