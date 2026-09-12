from fastapi import APIRouter
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.weathergpt_service import weathergpt_service

router = APIRouter(prefix="/chat", tags=["WeatherGPT Chat Engine"])

@router.post("", response_model=ChatResponse)
async def process_chat(req: ChatRequest):
    return await weathergpt_service.process_chat_query(req)
