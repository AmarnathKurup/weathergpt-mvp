import asyncio
import json

from app.agent import tools
from app.agent.llm_client import get_client
from app.config import get_settings
from app.models.schemas import ChatMessage, ChatResponse, LocationQuery, ToolCallTrace
from app.multilingual.language import detect_language, language_name
from app.multilingual.translate import translate_text

SYSTEM_PROMPT = """You are WeatherGPT, a helpful weather assistant.

Rules you must follow:
1. NEVER invent or guess actual weather numbers (temperature, rain, wind, forecasts, alerts).
   Always call the appropriate tool to fetch real data before answering a question
   that requires current conditions, forecasts, alerts, or a specific location lookup.
2. If the user doesn't specify a location but one was provided as context
   (see "Known user location" below), use that automatically without asking.
3. For general meteorology/climate/disaster-preparedness questions (e.g. "what is a
   heatwave", "how does IMD classify rainfall", "what should I do during a flood"),
   use the search_meteorology_knowledge tool to ground your answer in real domain facts.
4. Keep answers concise, clear, and practical. Use metric units (°C, km/h, mm).
5. If a tool call fails or returns an error, explain the issue plainly rather than
   fabricating a plausible-sounding answer.
6. When relevant, mention safety guidance for hazardous conditions.
7. When a user asks about real/current on-the-ground conditions (e.g. "is it actually
   flooding there", "any reports nearby"), use get_community_reports - official data can
   lag behind fast-moving local events, and nearby users may have reported it directly.
   Clearly label these as user-submitted reports, not official data.
8. When a user asks about farming, crops, spraying, irrigation, or livestock, use
   get_farmer_advisory rather than improvising general advice.
9. If asked for an "emergency briefing" or similarly urgent request, be direct and
   lead with the most critical safety information first, then supporting detail.

"""

MAX_TOOL_ITERATIONS = 4


async def _call_llm(client, **kwargs):
    """Run the sync Groq SDK call in a thread so we don't block the event loop."""
    return await asyncio.to_thread(client.chat.completions.create, **kwargs)


def _build_location_context(lat, lon, location_name) -> str:
    if lat is not None and lon is not None:
        return f"Known user location: lat={lat}, lon={lon}"
    if location_name:
        return f"Known user location: {location_name}"
    return "No known user location - ask for one if a location-specific question is asked and none is given."


async def run_agent(
    message: str,
    history: list[ChatMessage],
    lat: float | None,
    lon: float | None,
    location_name: str | None,
    forced_language: str | None = None,
) -> ChatResponse:
    settings = get_settings()

    detected_lang = forced_language or detect_language(message)

    # Translate the incoming message to English for reliable tool-calling/reasoning,
    # then translate the final reply back to the user's language.
    working_message = message
    if detected_lang != "en":
        working_message = translate_text(message, target_lang="en", source_lang="auto")

    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n" + _build_location_context(lat, lon, location_name)}
    ]
    for h in history[-8:]:  # keep recent context bounded
        messages.append({"role": h.role, "content": h.content})
    messages.append({"role": "user", "content": working_message})

    client = get_client()
    tool_traces: list[ToolCallTrace] = []

    for _ in range(MAX_TOOL_ITERATIONS):
        response = await _call_llm(
            client,
            model=settings.groq_model,
            messages=messages,
            tools=tools.TOOL_SCHEMAS,
            tool_choice="auto",
            temperature=0.3,
            max_tokens=800,
        )
        choice = response.choices[0]
        msg = choice.message

        if not msg.tool_calls:
            final_text = msg.content or "I couldn't generate a response. Please try again."
            break

        # Append the assistant's tool-call turn, then execute each tool and
        # append the results before looping back to the LLM.
        messages.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                    }
                    for tc in msg.tool_calls
                ],
            }
        )

        for tc in msg.tool_calls:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}

            # Auto-fill location from context if the model omitted it
            if not any(k in args for k in ("lat", "lon", "location_name", "name")):
                if lat is not None and lon is not None:
                    args["lat"], args["lon"] = lat, lon
                elif location_name:
                    args["location_name"] = location_name

            tool_traces.append(ToolCallTrace(tool=tc.function.name, arguments=args))

            try:
                result = await tools.execute_tool(tc.function.name, args)
            except Exception as e:  # noqa: BLE001 - surface tool errors to the LLM, not the user
                result = {"error": str(e)}

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result, default=str),
                }
            )
    else:
        final_text = (
            "I gathered some weather data but ran into trouble finalizing a response. "
            "Please try rephrasing your question."
        )

    if detected_lang != "en":
        final_text = translate_text(final_text, target_lang=detected_lang, source_lang="en")

    used_location = None
    if lat is not None and lon is not None:
        used_location = LocationQuery(lat=lat, lon=lon)
    elif location_name:
        used_location = LocationQuery(name=location_name)

    return ChatResponse(
        reply=final_text,
        detected_language=f"{detected_lang} ({language_name(detected_lang)})",
        tool_calls=tool_traces,
        used_location=used_location,
    )
