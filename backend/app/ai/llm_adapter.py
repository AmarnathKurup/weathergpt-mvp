import httpx
from typing import Dict, Any, List, Optional
from backend.app.core.config import settings

class LLMAdapter:
    def __init__(self):
        self.provider = settings.DEFAULT_LLM_PROVIDER
        self.gemini_key = settings.GEMINI_API_KEY
        self.openai_key = settings.OPENAI_API_KEY
        self.gemini_failed = False
        self.openai_failed = False

    async def generate_advisory_response(
        self,
        query: str,
        intent: str,
        location_name: str,
        temperature: float,
        rain_prob: float,
        weather_desc: str,
        occupation: str,
        events: List[str],
        actions: List[str],
        rag_context: List[str]
    ) -> str:
        """
        Executes multi-provider LLM response generation with instant fallback
        between Gemini, OpenAI, and the deterministic WeatherGPT Rule-Engine synthesizer.
        """
        gemini_key = settings.GEMINI_API_KEY or self.gemini_key
        openai_key = settings.OPENAI_API_KEY or self.openai_key

        # 1. Try Gemini API if key looks valid and hasn't failed
        if gemini_key and gemini_key.startswith("AIzaSy") and not self.gemini_failed:
            try:
                res = await self._call_gemini(query, location_name, temperature, rain_prob, weather_desc, occupation, events, actions, gemini_key)
                if res:
                    return res
            except Exception as e:
                print(f"[LLMAdapter] Gemini API call exception: {e}")

        # 2. Try OpenAI API if key looks valid and hasn't failed
        if openai_key and openai_key.startswith("sk-") and not self.openai_failed:
            try:
                res = await self._call_openai(query, location_name, temperature, rain_prob, weather_desc, occupation, events, actions, openai_key)
                if res:
                    return res
            except Exception as e:
                print(f"[LLMAdapter] OpenAI API call exception: {e}")

        # 3. Default Zero-Cost Rule Engine Language Synthesizer Fallback
        return self._rule_engine_synthesizer(query, location_name, temperature, rain_prob, weather_desc, occupation, events, actions)

    def _rule_engine_synthesizer(
        self,
        query: str,
        location: str,
        temp: float,
        rain_prob: float,
        weather_desc: str,
        occupation: str,
        events: List[str],
        actions: List[str]
    ) -> str:
        intro = f"In {location}, the current weather is {weather_desc.lower()} with a temperature of {temp}°C."

        if rain_prob >= 70:
            rain_msg = f" There is a high rain probability of {rain_prob}%."
        elif rain_prob >= 40:
            rain_msg = f" Rain is moderately possible ({rain_prob}% chance)."
        else:
            rain_msg = f" Rain probability is low at {rain_prob}%."

        action_str = ""
        if actions:
            clean_actions = [a.replace("_", " ") for a in actions]
            action_str = f" Recommended actions for {occupation}s: " + "; ".join(clean_actions) + "."

        return f"{intro}{rain_msg}{action_str}"

    async def _call_gemini(self, query, location, temp, rain_prob, weather_desc, occupation, events, actions, api_key: str) -> Optional[str]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={api_key}"
        prompt = (
            f"You are WeatherGPT, an authoritative Indian weather intelligence assistant.\n"
            f"Location: {location}\n"
            f"Temperature: {temp}°C, Weather: {weather_desc}, Rain Probability: {rain_prob}%\n"
            f"User Occupation: {occupation}\n"
            f"Detected Events: {events}\n"
            f"Recommended Actions: {actions}\n"
            f"User Question: '{query}'\n"
            f"Convert these verified weather facts into a helpful, accurate, concise, personalized advisory in 2-3 sentences. Do not invent weather numbers."
        )
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.post(url, json=payload)
            if r.status_code == 200:
                data = r.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
            else:
                self.gemini_failed = True
        return None

    async def _call_openai(self, query, location, temp, rain_prob, weather_desc, occupation, events, actions, api_key: str) -> Optional[str]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}"}
        prompt = (
            f"You are WeatherGPT for India.\nLocation: {location}, Temp: {temp}°C, Rain Prob: {rain_prob}%, Weather: {weather_desc}.\n"
            f"Occupation: {occupation}. Events: {events}. Actions: {actions}.\nUser Query: {query}.\nProvide a concise personalized response."
        )
        payload = {
            "model": settings.OPENAI_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150
        }
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.post(url, json=payload, headers=headers)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"].strip()
            else:
                self.openai_failed = True
        return None

llm_adapter = LLMAdapter()
