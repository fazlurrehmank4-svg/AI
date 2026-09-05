from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])

@router.get("/health")
def get_health():
    return {
        "status": "healthy",
        "service": "CropGuard AI Backend",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "ai_engine": {
            "ml_models": "scikit-learn (Linear Regression, Decision Tree, k-NN, K-Means)",
            "nlp_chatbot": "Local TF-IDF + Cosine Similarity + Reasoning Engine (Zero LLM API)",
            "reasoning": "Forward & Backward Chaining Rule Engine"
        }
    }
