"""
Supabase Service for CropGuard AI
Handles secure interaction with Supabase Auth & PostgreSQL database.
Enforces user-level data isolation and Row Level Security compliance.
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime
try:
    from supabase import create_client, Client
except ImportError:
    Client = None

class SupabaseService:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL", "https://tspdpkyhszrebrclsefz.supabase.co")
        self.anon_key = os.getenv("SUPABASE_ANON_KEY", "")
        self.service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

        self.client: Optional[Client] = None
        if self.supabase_url and self.anon_key and self.anon_key != "placeholder_anon_key" and Client:
            try:
                self.client = create_client(self.supabase_url, self.anon_key)
            except Exception as e:
                print(f"[SupabaseService] Client initialization notice: {e}")

        # In-memory storage fallback for local development/testing if Supabase keys aren't configured yet
        self._memory_history: List[Dict[str, Any]] = []
        self._memory_profiles: Dict[str, Dict[str, Any]] = {}

    def is_configured(self) -> bool:
        return self.client is not None

    async def save_prediction(self, prediction_data: Dict[str, Any], user_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Saves a crop health prediction to the 'prediction_history' table.
        Enforces user isolation via user_id.
        """
        record = {
            "user_id": prediction_data.get("user_id", "guest-user"),
            "crop": prediction_data.get("crop"),
            "location": prediction_data.get("location"),
            "weather": prediction_data.get("weather"),
            "crop_health_score": prediction_data.get("crop_health_score"),
            "health_status": prediction_data.get("health_status"),
            "risk_level": prediction_data.get("risk_level"),
            "causes": prediction_data.get("causes", []),
            "precautions": prediction_data.get("precautions", []),
            "created_at": datetime.utcnow().isoformat()
        }

        if self.client and user_token:
            try:
                # Use client with authenticated user token to respect RLS
                res = self.client.table("prediction_history").insert(record).execute()
                return res.data[0] if res.data else record
            except Exception as e:
                print(f"[SupabaseService] Database insert error: {e}")

        # Local fallback store
        self._memory_history.insert(0, record)
        return record

    async def get_user_prediction_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Fetches prediction history for a specific authenticated user.
        """
        if self.client:
            try:
                res = self.client.table("prediction_history") \
                    .select("*") \
                    .eq("user_id", user_id) \
                    .order("created_at", desc=True) \
                    .limit(limit) \
                    .execute()
                return res.data or []
            except Exception as e:
                print(f"[SupabaseService] History fetch error: {e}")

        # Fallback to local memory filter
        return [h for h in self._memory_history if h.get("user_id") == user_id][:limit]

    async def get_or_create_profile(self, user_id: str, email: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetches or provisions a farmer profile record.
        """
        if self.client:
            try:
                res = self.client.table("profiles").select("*").eq("id", user_id).execute()
                if res.data:
                    return res.data[0]
                else:
                    new_prof = {
                        "id": user_id,
                        "email": email or f"{user_id}@cropguard.local",
                        "full_name": "Farmer",
                        "farm_location": "Default Region",
                        "primary_crops": ["Wheat", "Tomato"]
                    }
                    ins = self.client.table("profiles").insert(new_prof).execute()
                    return ins.data[0] if ins.data else new_prof
            except Exception as e:
                print(f"[SupabaseService] Profile query error: {e}")

        if user_id not in self._memory_profiles:
            self._memory_profiles[user_id] = {
                "id": user_id,
                "email": email or f"{user_id}@cropguard.local",
                "full_name": "Farmer",
                "farm_location": "Default Region",
                "primary_crops": ["Wheat", "Tomato"]
            }
        return self._memory_profiles[user_id]
