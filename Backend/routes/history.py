from fastapi import APIRouter, HTTPException, Query, Header
from typing import List, Optional, Dict, Any
from Backend.services.supabase_service import SupabaseService

router = APIRouter(tags=["Prediction History"])
supabase_service = SupabaseService()

@router.get("/history", response_model=List[Dict[str, Any]])
async def get_history(
    user_id: str = Query(..., description="Authenticated farmer UUID"),
    limit: int = Query(20, description="Max history records to return"),
    authorization: Optional[str] = Header(None)
):
    try:
        history = await supabase_service.get_user_prediction_history(user_id=user_id, limit=limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")
