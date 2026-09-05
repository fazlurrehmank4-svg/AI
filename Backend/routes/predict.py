from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from Backend.schemas.api_schemas import PredictRequest, PredictResponse
from Backend.ai.predictor import CropGuardPredictor
from Backend.services.supabase_service import SupabaseService

router = APIRouter(tags=["Crop Health Prediction"])
predictor = CropGuardPredictor()
supabase_service = SupabaseService()

@router.post("/predict", response_model=PredictResponse)
async def predict_crop_health(
    payload: PredictRequest,
    authorization: Optional[str] = Header(None)
):
    try:
        w = payload.weather
        result = predictor.predict(
            crop=payload.crop,
            temperature=w.temperature,
            humidity=w.humidity,
            rainfall=w.rainfall,
            wind_speed=w.wind_speed,
            soil_ph=payload.soil_ph or 6.5,
            location_name=w.location_name or "Field Station"
        )

        # Store in Supabase if user is logged in
        user_token = authorization.replace("Bearer ", "") if authorization else None
        user_id = payload.user_id or "anonymous-farmer"
        result["user_id"] = user_id

        # Async background persistence
        try:
            await supabase_service.save_prediction(result, user_token=user_token)
        except Exception as err:
            print(f"[PredictRoute] Optional history persistence note: {err}")

        return PredictResponse(
            crop=result["crop"],
            location=result["location"],
            weather=w,
            crop_health_score=result["crop_health_score"],
            health_status=result["health_status"],
            risk_level=result["risk_level"],
            primary_risk_factor=result["primary_risk_factor"],
            agro_climatic_regime=result["agro_climatic_regime"],
            causes=result["causes"],
            precautions=result["precautions"],
            ai_explanation=result["ai_explanation"],
            timestamp=result["timestamp"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
