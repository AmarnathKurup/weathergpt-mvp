from typing import Dict, List, Optional

# Official 22 Indian Languages ISO 639 Mapping
INDIAN_LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {"name": "English", "native": "English", "bhashini_code": "en"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "bhashini_code": "hi"},
    "bn": {"name": "Bengali", "native": "বাংলা", "bhashini_code": "bn"},
    "ta": {"name": "Tamil", "native": "தமிழ்", "bhashini_code": "ta"},
    "te": {"name": "Telugu", "native": "తెలుగు", "bhashini_code": "te"},
    "mr": {"name": "Marathi", "native": "मराठी", "bhashini_code": "mr"},
    "gu": {"name": "Gujarati", "native": "ગુજરાતી", "bhashini_code": "gu"},
    "kn": {"name": "Kannada", "native": "কನ್ನಡ", "bhashini_code": "kn"},
    "ml": {"name": "Malayalam", "native": "മലയാളം", "bhashini_code": "ml"},
    "pa": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ", "bhashini_code": "pa"},
    "or": {"name": "Odia", "native": "ওড়িয়া", "bhashini_code": "or"},
    "as": {"name": "Assamese", "native": "অসমীয়া", "bhashini_code": "as"},
    "ur": {"name": "Urdu", "native": "اردو", "bhashini_code": "ur"},
    "sa": {"name": "Sanskrit", "native": "संस्कृतम्", "bhashini_code": "sa"},
    "ma": {"name": "Maithili", "native": "मैथिली", "bhashini_code": "mai"},
    "ne": {"name": "Nepali", "native": "नेपाली", "bhashini_code": "ne"},
    "ks": {"name": "Kashmiri", "native": "कॉशुर", "bhashini_code": "ks"},
    "sd": {"name": "Sindhi", "native": "سنڌي", "bhashini_code": "sd"},
    "kok": {"name": "Konkani", "native": "कोंकणी", "bhashini_code": "kok"},
    "doi": {"name": "Dogri", "native": "डोगरी", "bhashini_code": "doi"},
    "mni": {"name": "Manipuri", "native": "মৈতৈলোন্", "bhashini_code": "mni"},
    "sat": {"name": "Santali", "native": "ᱥᱟᱱᱛᱟᱲᱤ", "bhashini_code": "sat"},
    "brx": {"name": "Bodo", "native": "बर'", "bhashini_code": "brx"}
}

class LanguageService:
    @staticmethod
    def get_supported_languages() -> List[Dict[str, str]]:
        return [{"code": k, **v} for k, v in INDIAN_LANGUAGES.items()]

    @staticmethod
    def get_bhashini_code(lang_code: str) -> str:
        lang_info = INDIAN_LANGUAGES.get(lang_code.lower())
        return lang_info["bhashini_code"] if lang_info else "hi"

language_service = LanguageService()
