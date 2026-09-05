from fastapi import APIRouter, HTTPException, Query, Header
from typing import Optional, Dict, Any
from Backend.services.supabase_service import SupabaseService

router = APIRouter(tags=["User Profile"])
supabase_service = SupabaseService()

@router.get("/profile")
async def get_profile(
    user_id: str = Query(..., description="Farmer User ID"),
    email: Optional[str] = Query(None, description="User email"),
    authorization: Optional[str] = Header(None)
):
    try:
        profile = await supabase_service.get_or_create_profile(user_id=user_id, email=email)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {str(e)}")
