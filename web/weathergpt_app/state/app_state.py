import reflex as rx
import httpx
import json
from typing import List, Dict, Any, Optional, TypedDict

BACKEND_URL = "http://localhost:8000/api/v1"

INDIAN_LANGUAGES = [
    {"code": "en", "name": "English", "native": "English"},
    {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
    {"code": "bn", "name": "Bengali", "native": "বাংলা"},
    {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
    {"code": "te", "name": "Telugu", "native": "తెలుగు"},
    {"code": "mr", "name": "Marathi", "native": "मराठी"},
    {"code": "gu", "name": "Gujarati", "native": "ગુજરાતી"},
    {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ"},
    {"code": "ml", "name": "Malayalam", "native": "മലയാളം"},
    {"code": "or", "name": "Odia", "native": "ଓଡ଼ିଆ"},
    {"code": "pa", "name": "Punjabi", "native": "ਪੰਜਾਬੀ"},
    {"code": "as", "name": "Assamese", "native": "অসমীয়া"},
    {"code": "ur", "name": "Urdu", "native": "اردو"},
    {"code": "mai", "name": "Maithili", "native": "मैथिली"},
    {"code": "ks", "name": "Kashmiri", "native": "कश्मीरी"},
    {"code": "ne", "name": "Nepali", "native": "नेपाली"},
    {"code": "sd", "name": "Sindhi", "native": "سنڌي"},
    {"code": "sa", "name": "Sanskrit", "native": "संस्कृतम्"},
    {"code": "kok", "name": "Konkani", "native": "कोंकणी"},
    {"code": "mni", "name": "Manipuri", "native": "মৈতৈলোন্"},
    {"code": "doi", "name": "Dogri", "native": "डोगरी"},
    {"code": "brx", "name": "Bodo", "native": "बड़ो"},
]

class ChatFacts(TypedDict, total=False):
    source: str
    model: str
    updated: str
    rain_prob: str
    precipitation: str
    risk: str

class ChatMessage(TypedDict, total=False):
    sender: str
    text: str
    timestamp: str
    show_why: bool
    facts: ChatFacts

class AppState(rx.State):
    """Global Application State for WeatherGPT Reflex Web Interface."""

    # Location & Search State
    current_pincode: str = "700001"
    search_query: str = ""
    location_name: str = "Kolkata, West Bengal"
    district: str = "Kolkata"
    state_name: str = "West Bengal"
    lat: float = 22.5726
    lon: float = 88.3639
    is_loading: bool = False
    error_message: str = ""

    # Preferences & Accessibility
    current_language: str = "en"
    theme_mode: str = "dark"  # dark, light, high_contrast
    font_size: str = "normal"  # small, normal, large, xlarge
    line_spacing: str = "normal" # compact, normal, wide
    read_aloud_enabled: bool = False
    high_contrast: bool = False
    selected_occupation: str = "student" # student, farmer, fisherman, driver, tourist, outdoor_worker

    # Weather Data
    temperature: float = 31.5
    feels_like: float = 36.2
    weather_condition: str = "Partly Cloudy with Evening Rain"
    rain_probability: int = 78
    humidity: int = 75
    wind_speed: float = 14.5
    wind_direction: str = "SE"
    uv_index: int = 8
    visibility_km: float = 8.0
    pressure_hpa: int = 1008
    sunrise: str = "05:22 AM"
    sunset: str = "06:14 PM"
    warning_level: str = "orange"  # green, yellow, orange, red
    warning_title: str = "Orange Alert — Heavy Rainfall & Thunderstorm Warning"
    warning_desc: str = "IMD reports convective cloud development over Kolkata division. Rain 12-25mm expected 17:00-20:00 IST."

    # Forecast Data Lists
    hourly_forecast: List[Dict[str, Any]] = [
        {"time": "14:00", "temp": "32°C", "pop": "30%", "icon": "sun", "cond": "Partly Cloudy"},
        {"time": "15:00", "temp": "33°C", "pop": "40%", "icon": "cloud-sun", "cond": "Humid & Hazy"},
        {"time": "16:00", "temp": "31°C", "pop": "60%", "icon": "cloud-drizzle", "cond": "Overcast"},
        {"time": "17:00", "temp": "28°C", "pop": "78%", "icon": "cloud-rain", "cond": "Heavy Rain"},
        {"time": "18:00", "temp": "27°C", "pop": "85%", "icon": "cloud-lightning", "cond": "Thunderstorm"},
        {"time": "19:00", "temp": "26°C", "pop": "70%", "icon": "cloud-rain", "cond": "Moderate Rain"},
        {"time": "20:00", "temp": "26°C", "pop": "40%", "icon": "cloud", "cond": "Passing Shower"},
    ]

    daily_forecast: List[Dict[str, Any]] = [
        {"day": "Today", "date": "Sep 01", "max": "33°C", "min": "26°C", "pop": "78%", "cond": "Thunderstorm Evening"},
        {"day": "Tomorrow", "date": "Sep 02", "max": "32°C", "min": "25°C", "pop": "65%", "cond": "Moderate Rain"},
        {"day": "Thursday", "date": "Sep 03", "max": "34°C", "min": "27°C", "pop": "30%", "cond": "Partly Sunny"},
        {"day": "Friday", "date": "Sep 04", "max": "35°C", "min": "28°C", "pop": "20%", "cond": "Hot & Humid"},
        {"day": "Saturday", "date": "Sep 05", "max": "31°C", "min": "26°C", "pop": "80%", "cond": "Heavy Monsoonal Rain"},
        {"day": "Sunday", "date": "Sep 06", "max": "30°C", "min": "25°C", "pop": "70%", "cond": "Scattered Showers"},
        {"day": "Monday", "date": "Sep 07", "max": "32°C", "min": "26°C", "pop": "40%", "cond": "Cloudy Breaks"},
    ]

    # AI Chat State
    chat_input: str = ""
    chat_history: List[ChatMessage] = [
        {
            "sender": "assistant",
            "text": "Namaste! I am WeatherGPT, India's Conversational Weather Intelligence System. Ask me anything about current weather, PIN code forecasts, agricultural advisories, or cyclone warnings in 22 Indian languages.",
            "timestamp": "14:30",
            "show_why": False,
            "facts": {
                "source": "IMD District Nowcast + Open-Meteo ECMWF IFS",
                "model": "WeatherGPT-7B (Reasoning Core)",
                "updated": "14:15 IST",
                "rain_prob": "78%",
                "precipitation": "14mm",
                "risk": "Orange Alert (Thunderstorm & Lightning)"
            }
        }
    ]

    # Active Tab / Page State
    current_page: str = "dashboard"
    show_accessibility_modal: bool = False
    show_why_modal: bool = False
    active_why_facts: Dict[str, Any] = {}
    emergency_mode: bool = False

    # Saved Places
    saved_places: List[Dict[str, Any]] = [
        {"name": "Home", "pincode": "700001", "location": "Kolkata, WB", "temp": "31.5°C", "cond": "Partly Cloudy", "rain": "78%", "alert": "orange"},
        {"name": "Office", "pincode": "110001", "location": "Connaught Place, Delhi", "temp": "38.2°C", "cond": "Hot & Clear", "rain": "10%", "alert": "yellow"},
        {"name": "Farm", "pincode": "411001", "location": "Pune, Maharashtra", "temp": "28.0°C", "cond": "Light Rain", "rain": "45%", "alert": "green"},
        {"name": "College", "pincode": "560001", "location": "Bengaluru, Karnataka", "temp": "26.4°C", "cond": "Pleasant", "rain": "20%", "alert": "green"},
    ]

    # NWP Model Matrix Data
    nwp_models: List[Dict[str, Any]] = [
        {"model": "ECMWF IFS (0.1°)", "temp": "31.5°C", "rain_prob": "78%", "precip": "14.2 mm", "wind": "15 km/h", "confidence": "High (92%)"},
        {"model": "GFS NCEP (0.25°)", "temp": "32.0°C", "rain_prob": "82%", "precip": "16.0 mm", "wind": "18 km/h", "confidence": "High (89%)"},
        {"model": "IMD NCUM (Regional)", "temp": "31.2°C", "rain_prob": "75%", "precip": "12.8 mm", "wind": "14 km/h", "confidence": "Very High (95%)"},
        {"model": "ICON-EU (0.12°)", "temp": "31.8°C", "rain_prob": "70%", "precip": "11.5 mm", "wind": "16 km/h", "confidence": "Moderate (84%)"},
    ]

    # Contextual Quick Prompts
    quick_prompts: List[str] = [
        "Will it rain in the evening today?",
        "Do I need an umbrella for my commute?",
        "Agromet advisory for farmers in this district",
        "Is there a cyclone alert for coastal areas?",
        "Compare weather between Kolkata and Delhi",
        "How hot will it feel during noon hours?",
    ]

    # India Weather Pulse Data
    pulse_locations: List[Dict[str, str]] = [
        {"city": "Rajasthan (Churu)", "temp": "42°C", "cond": "Heatwave Warning", "level": "red"},
        {"city": "Delhi (Safdarjung)", "temp": "38°C", "cond": "Hot & Humid", "level": "yellow"},
        {"city": "Kolkata (Alipore)", "temp": "31°C", "cond": "Thunderstorm Evening", "level": "orange"},
        {"city": "Bengaluru (HAL)", "temp": "26°C", "cond": "Pleasant Breeze", "level": "green"},
        {"city": "Mumbai (Santacruz)", "temp": "30°C", "cond": "High Humidity (84%)", "level": "yellow"},
        {"city": "Chennai (Meenambakkam)", "temp": "35°C", "cond": "Partly Cloudy", "level": "green"},
    ]

    def set_language(self, lang_code: str):
        self.current_language = lang_code

    def set_theme(self, mode: str):
        self.theme_mode = mode
        self.high_contrast = (mode == "high_contrast")

    def set_font_size(self, size: str):
        self.font_size = size

    def toggle_read_aloud(self):
        self.read_aloud_enabled = not self.read_aloud_enabled

    def toggle_accessibility_modal(self):
        self.show_accessibility_modal = not self.show_accessibility_modal

    def toggle_emergency_mode(self):
        self.emergency_mode = not self.emergency_mode

    def set_occupation(self, occ: str):
        self.selected_occupation = occ

    def set_search_query(self, query: str):
        self.search_query = query

    def set_chat_input(self, message: str):
        self.chat_input = message

    def select_prompt(self, prompt: str):
        self.chat_input = prompt

    def open_why_facts(self, facts: Dict[str, Any]):
        self.active_why_facts = facts
        self.show_why_modal = True

    def close_why_modal(self):
        self.show_why_modal = False

    def toggle_why(self, index: int):
        if 0 <= index < len(self.chat_history):
            self.chat_history[index]["show_why"] = not self.chat_history[index].get("show_why", False)
            self.chat_history = list(self.chat_history)

    async def search_pincode_action(self):
        query = self.search_query.strip() or self.current_pincode
        if not query:
            return
        self.is_loading = True
        self.error_message = ""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(f"{BACKEND_URL}/location/pincode/{query}")
                if res.status_code == 200:
                    data = res.json()
                    self.current_pincode = query
                    self.location_name = f"{data.get('office_name', 'Location')}, {data.get('district', '')}"
                    self.district = data.get('district', '')
                    self.state_name = data.get('state', '')
                    self.lat = data.get('lat', self.lat)
                    self.lon = data.get('lon', self.lon)
                    
                    w_res = await client.get(f"{BACKEND_URL}/weather/current?lat={self.lat}&lon={self.lon}&pincode={query}")
                    if w_res.status_code == 200:
                        w_data = w_res.json()
                        self.temperature = w_data.get("temperature", self.temperature)
                        self.feels_like = w_data.get("feels_like", self.feels_like)
                        self.humidity = w_data.get("humidity", self.humidity)
                        self.rain_probability = w_data.get("rain_probability", self.rain_probability)
                        self.weather_condition = w_data.get("condition", self.weather_condition)
                else:
                    self.location_name = f"PIN {query} (Local Intelligence Cache)"
        except Exception:
            self.error_message = "Using cached weather intelligence."
        finally:
            self.is_loading = False

    async def send_chat(self):
        msg = self.chat_input.strip()
        if not msg:
            return
        
        self.chat_history.append({
            "sender": "user",
            "text": msg,
            "timestamp": "Just now",
            "show_why": False
        })
        self.chat_input = ""
        
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.post(
                    f"{BACKEND_URL}/chat",
                    json={
                        "message": msg,
                        "pincode": self.current_pincode,
                        "language": self.current_language,
                        "occupation": self.selected_occupation
                    }
                )
                if res.status_code == 200:
                    bot_data = res.json()
                    reply = bot_data.get("response", "Rain is expected in your area after 5 PM.")
                    facts = bot_data.get("facts", {
                        "source": "IMD District Nowcast + Open-Meteo ECMWF IFS",
                        "model": "WeatherGPT-7B (Reasoning Core)",
                        "updated": "Just now",
                        "rain_prob": f"{self.rain_probability}%",
                        "precipitation": "14.2 mm",
                        "risk": "Orange Alert (Thunderstorm)"
                    })
                else:
                    reply = self._generate_fallback_response(msg)
                    facts = {"source": "IMD Regional Nowcast", "model": "WeatherGPT Local Rule Engine", "updated": "Now", "rain_prob": f"{self.rain_probability}%", "precipitation": "12.0 mm", "risk": "Orange Alert"}
        except Exception:
            reply = self._generate_fallback_response(msg)
            facts = {"source": "IMD + Open-Meteo ECMWF", "model": "WeatherGPT Rule Engine", "updated": "Now", "rain_prob": f"{self.rain_probability}%", "precipitation": "12.0 mm", "risk": "Orange Alert"}
            
        self.chat_history.append({
            "sender": "assistant",
            "text": reply,
            "timestamp": "Just now",
            "show_why": False,
            "facts": facts
        })

    def _generate_fallback_response(self, user_msg: str) -> str:
        msg_lower = user_msg.lower()
        if "rain" in msg_lower or "rainy" in msg_lower:
            return f"Rain probability is {self.rain_probability}% in {self.location_name} between 17:00–20:00 IST. Since your role is {self.selected_occupation}, carry rain gear and avoid waterlogged routes."
        elif "farmer" in msg_lower or "crop" in msg_lower or "agri" in msg_lower:
            return f"Agromet Advisory for {self.district}: Moderate rain (12-20mm) expected. Postpone chemical sprays and ensure adequate field drainage for standing crops."
        elif "temp" in msg_lower or "hot" in msg_lower or "weather" in msg_lower:
            return f"Current temperature in {self.location_name} is {self.temperature}°C (Feels like {self.feels_like}°C). Relative Humidity: {self.humidity}%. Winds SE at {self.wind_speed} km/h."
        else:
            return f"WeatherGPT analysis for PIN {self.current_pincode} ({self.location_name}): Weather is {self.weather_condition}. Temperature {self.temperature}°C, Rain probability {self.rain_probability}%. Advisory Level: {self.warning_level.upper()}."

