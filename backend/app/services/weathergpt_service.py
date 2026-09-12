from typing import Dict, Any, List
from backend.app.schemas.chat import ChatRequest, ChatResponse, ExplainabilityDetails
from backend.app.services.weather_service import weather_service
from backend.app.ai.intent_classifier import intent_classifier
from backend.app.alerts.risk_engine import risk_engine
from backend.app.ai.advisory_profiles import advisory_profiles
from backend.app.ai.rag_knowledge_base import rag_knowledge_base
from backend.app.ai.llm_adapter import llm_adapter
from backend.app.language.bhashini_adapter import bhashini_adapter

class WeatherGPTService:
    async def process_chat_query(self, req: ChatRequest) -> ChatResponse:
        # Step 1: Classify Intent
        intent = intent_classifier.classify(req.query)

        # Step 2: Fetch Normalized Weather & IMD Warnings for location
        snapshot = await weather_service.get_current_weather(
            location_query=req.location or req.query,
            lat=req.latitude,
            lon=req.longitude
        )

        # Step 3: Run Weather Rule & Risk Engine
        events, rule_actions = risk_engine.evaluate_risk(snapshot)

        # Step 4: Run Occupation Advisory Engine
        occupation = req.occupation or "general"
        profile_advisories = advisory_profiles.get_advisory(occupation, events)
        all_actions = list(set(rule_actions + profile_advisories))

        # Step 5: Retrieve RAG Meteorological Knowledge
        rag_context = rag_knowledge_base.retrieve(req.query)

        # Step 6: Generate LLM Advisory Response (with safe local rule-engine fallback)
        raw_answer_en = await llm_adapter.generate_advisory_response(
            query=req.query,
            intent=intent,
            location_name=snapshot.location.name,
            temperature=snapshot.temperature,
            rain_prob=snapshot.rain_probability,
            weather_desc=snapshot.weather_desc,
            occupation=occupation,
            events=events,
            actions=all_actions,
            rag_context=rag_context
        )

        # Step 7: Translate to target Indian language via BHASHINI Adapter
        target_lang = req.language or "en"
        final_answer = await bhashini_adapter.translate(raw_answer_en, target_lang=target_lang)

        # Step 8: Build Explainable "Why?" Details
        explainability = ExplainabilityDetails(
            temperature=snapshot.temperature,
            rain_probability=snapshot.rain_probability,
            rain_mm=snapshot.rain,
            wind_kmh=snapshot.wind_speed,
            uv_index=snapshot.uv_index,
            weather_code=snapshot.weather_code,
            weather_desc=snapshot.weather_desc,
            data_source=snapshot.source,
            nwp_model=snapshot.model,
            updated_at=snapshot.timestamp,
            active_warnings=snapshot.warnings,
            matched_rules=events
        )

        return ChatResponse(
            query=req.query,
            intent=intent,
            language=target_lang,
            location_name=snapshot.location.name,
            answer=final_answer,
            weather_snapshot=snapshot,
            detected_events=events,
            recommended_actions=all_actions,
            why_explainability=explainability,
            confidence=0.96
        )

weathergpt_service = WeatherGPTService()
