from fastapi import APIRouter, HTTPException, Header, Query
from typing import Optional
from Backend.schemas.api_schemas import PredictRequest, PredictResponse, ForecastAlertResponse
from Backend.ai.predictor import CropGuardPredictor
from Backend.services.supabase_service import SupabaseService
from Backend.services.weather_service import WeatherService

router = APIRouter(tags=["Crop Health Prediction"])
predictor = CropGuardPredictor()
supabase_service = SupabaseService()
weather_service = WeatherService()

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

@router.get("/predict/forecast-alerts", response_model=ForecastAlertResponse)
async def get_crop_forecast_alerts(
    crop: str = Query("Wheat", description="Crop name"),
    city: Optional[str] = Query(None, description="City name"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude")
):
    try:
        forecast_days = await weather_service.get_3_day_forecast(
            latitude=lat, longitude=lon, city_name=city
        )
        resolved_loc = forecast_days[0].get("location_name", city or "Local Farm") if forecast_days else (city or "Local Farm")
        eval_result = predictor.evaluate_forecast_hazards(
            crop=crop,
            forecast_days=forecast_days,
            location_name=resolved_loc
        )
        return ForecastAlertResponse(**eval_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate forecast alerts: {str(e)}")

