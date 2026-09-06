from fastapi import APIRouter, HTTPException
from Backend.schemas.api_schemas import ChatRequest, ChatResponse, ChatFeedbackRequest
from Backend.ai.chatbot import get_chatbot

router = APIRouter(tags=["Local AI Chatbot"])
chatbot = get_chatbot()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_cropguard(payload: ChatRequest):
    try:
        response_dict = chatbot.ask(
            question=payload.message,
            active_crop=payload.crop,
            current_prediction=payload.current_prediction,
            language=payload.language
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

@router.post("/chat/feedback")
async def record_chat_feedback(feedback: ChatFeedbackRequest):
    """
    Submits direct farmer feedback into CropGuard's Self-Learning Engine.
    Reinforces positive knowledge connections and auto-adapts vocabulary.
    """
    try:
        if hasattr(chatbot, "learning_engine") and chatbot.learning_engine is not None:
            stats = chatbot.learning_engine.ingest_feedback(
                query=feedback.query,
                rating=feedback.rating,
                corrected_answer=feedback.user_correction,
                suggested_topic=feedback.correct_topic,
                language=feedback.language or "auto"
            )
            # Live rebuild chatbot retrieval index with newly learned weights
            chatbot.rebuild_index()
            return {"status": "success", "learned": True, "stats": stats}
        return {"status": "success", "learned": False, "message": "Self-learning engine initialized"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback ingestion failed: {str(e)}")

@router.get("/chat/learning-stats")
async def get_learning_stats():
    """Returns real-time metrics from the self-learning memory engine."""
    try:
        if hasattr(chatbot, "learning_engine") and chatbot.learning_engine is not None:
            return chatbot.learning_engine.get_learning_stats()
        return {"total_interactions": 0, "learned_patterns": 0, "status": "active"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

