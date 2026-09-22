import groq
from fastapi import APIRouter, HTTPException

from app.agent.weathergpt_agent import run_agent
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message must not be empty")
    try:
        return await run_agent(
            message=req.message,
            history=req.history,
            lat=req.lat,
            lon=req.lon,
            location_name=req.location_name,
            forced_language=req.language,
        )
    except RuntimeError as e:
        # e.g. missing GROQ_API_KEY
        raise HTTPException(status_code=500, detail=str(e)) from e
    except groq.NotFoundError as e:
        raise HTTPException(
            status_code=502,
            detail=(
                "The configured Groq model isn't available (it may have been "
                "deprecated). Check GROQ_MODEL in backend/.env against "
                "https://console.groq.com/docs/models for a currently supported model."
            ),
        ) from e
    except groq.AuthenticationError as e:
        raise HTTPException(
            status_code=502,
            detail="Groq rejected the API key. Check GROQ_API_KEY in backend/.env.",
        ) from e
    except groq.RateLimitError as e:
        raise HTTPException(
            status_code=502,
            detail="Groq rate limit hit. Wait a moment and try again.",
        ) from e
    except groq.APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"Groq API error: {e}") from e
