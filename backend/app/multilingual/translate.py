from deep_translator import GoogleTranslator

from app.utils.cache import cache


def translate_text(text: str, target_lang: str, source_lang: str = "auto") -> str:
    """Translate text using the free GoogleTranslator backend.

    Network access to Google Translate is required. If it's unavailable
    (offline dev, blocked network, rate limit) we fail soft and return the
    original text rather than breaking the chat flow.
    """
    if not text or target_lang == "en" and source_lang == "en":
        return text

    cache_key = f"translate:{source_lang}:{target_lang}:{hash(text)}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        if not translated:
            return text
        cache.set(cache_key, translated, ttl=3600)
        return translated
    except Exception:
        # Translation is a "nice to have" for the MVP - never break the response.
        return text
