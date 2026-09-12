import httpx
from typing import Optional, Dict
from backend.app.core.config import settings
from backend.app.language.language_service import language_service

# Built-in offline fallback translations for primary Indian languages
OFFLINE_DICTIONARY: Dict[str, Dict[str, str]] = {
    "hi": {
        "rain": "बारिश",
        "umbrella": "छतरी या रेनकोट साथ रखें।",
        "thunderstorm": "बिजली गिरने की संभावना है, खुले मैदान में जाने से बचें।",
        "hot": "आज तेज धूप और गर्मी रहेगी, पानी पर्याप्त मात्रा में पिएं।"
    },
    "bn": {
        "rain": "বৃষ্টি",
        "umbrella": "ছাতা বা রেইনকোট সঙ্গে রাখুন।",
        "thunderstorm": "বজ্রপাতের সম্ভাবনা রয়েছে, খোলা জায়গা এড়িয়ে চলুন।",
        "hot": "প্রচণ্ড গরম থাকবে, প্রচুর জল পান করুন।"
    },
    "ta": {
        "rain": "மழை",
        "umbrella": "குடை அல்லது மழைக்கோட்டை உடன் எடுத்துச் செல்லவும்.",
        "thunderstorm": "இடி மின்னல் அபாயம் உள்ளது. திறந்தவெளிகளைத் தவிர்க்கவும்."
    },
    "te": {
        "rain": "వర్షం",
        "umbrella": "గొడుగు లేదా రెయిన్‌కోట్ తీసుకెళ్లండి.",
        "thunderstorm": "ఉరుములు మరియు మెరుపులు వచ్చే అవకాశం ఉంది."
    },
    "mr": {
        "rain": "पाऊस",
        "umbrella": "छत्री किंवा रेनकोट सोबत ठेवा.",
        "thunderstorm": "विजांचा कडकडाट होण्याची शक्यता आहे."
    }
}

class BhashiniAdapter:
    def __init__(self):
        self.user_id = settings.BHASHINI_USER_ID
        self.api_key = settings.BHASHINI_API_KEY
        self.pipeline_id = settings.BHASHINI_PIPELINE_ID
        self.base_url = settings.BHASHINI_BASE_URL

    async def translate(self, text: str, target_lang: str, source_lang: str = "en") -> str:
        if target_lang == "en" or not text:
            return text

        # If BHASHINI credentials available, invoke BHASHINI ULCA Pipeline
        if self.user_id and self.api_key and self.pipeline_id:
            try:
                b_source = language_service.get_bhashini_code(source_lang)
                b_target = language_service.get_bhashini_code(target_lang)

                payload = {
                    "pipelineTasks": [
                        {
                            "taskType": "translation",
                            "config": {
                                "language": {
                                    "sourceLanguage": b_source,
                                    "targetLanguage": b_target
                                }
                            }
                        }
                    ],
                    "inputData": {
                        "input": [{"source": text}]
                    }
                }
                headers = {
                    "userPyId": self.user_id,
                    "authorization": self.api_key,
                    "Content-Type": "application/json"
                }
                async with httpx.AsyncClient(timeout=8.0) as client:
                    r = await client.post(self.base_url, json=payload, headers=headers)
                    if r.status_code == 200:
                        res = r.json()
                        translated = res["pipelineResponse"][0]["output"][0]["target"]
                        if translated:
                            return translated
            except Exception:
                pass # Fall back to built-in translator

        # Built-in offline fallback synthesis
        return self._offline_translate(text, target_lang)

    def _offline_translate(self, text: str, target_lang: str) -> str:
        dict_lang = OFFLINE_DICTIONARY.get(target_lang.lower())
        if not dict_lang:
            return f"[{target_lang.upper()}] {text}"

        translated = text
        if "rain" in text.lower() or "umbrella" in text.lower():
            if "umbrella" in dict_lang:
                translated += f" ({dict_lang['umbrella']})"
        if "thunderstorm" in text.lower() or "lightning" in text.lower():
            if "thunderstorm" in dict_lang:
                translated += f" ({dict_lang['thunderstorm']})"

        return translated

bhashini_adapter = BhashiniAdapter()
