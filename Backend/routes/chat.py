from fastapi import APIRouter, HTTPException
from Backend.schemas.api_schemas import ChatRequest, ChatResponse
from Backend.ai.chatbot import get_chatbot

router = APIRouter(tags=["Local AI Chatbot"])
chatbot = get_chatbot()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_cropguard(payload: ChatRequest):
    try:
        response_dict = chatbot.ask(
            question=payload.message,
            active_crop=payload.crop,
            current_prediction=payload.current_prediction
        )
        return ChatResponse(
            answer=response_dict["answer"],
            confidence=response_dict["confidence"],
            matched_topic=response_dict["matched_topic"],
            category=response_dict["category"],
            reasoning_summary=response_dict["reasoning_summary"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot failed: {str(e)}")
