from langdetect import DetectorFactory, LangDetectException, detect

# Make detection deterministic across runs
DetectorFactory.seed = 0

# A small set of languages we expect WeatherGPT users to write in.
# langdetect returns ISO 639-1 codes.
SUPPORTED_LANGS = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh-cn": "Chinese",
    "ar": "Arabic",
}


def detect_language(text: str) -> str:
    """Detect the language of a piece of text, defaulting to English.

    langdetect is unreliable on very short strings, so short inputs
    (< 3 tokens) fall back to English to avoid mis-triggering translation.
    """
    if not text or len(text.strip()) < 3:
        return "en"
    try:
        code = detect(text)
    except LangDetectException:
        return "en"
    return code if code in SUPPORTED_LANGS else code


def language_name(code: str) -> str:
    return SUPPORTED_LANGS.get(code, code)
