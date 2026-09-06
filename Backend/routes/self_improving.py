from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from Backend.schemas.api_schemas import (
    CropRecommendationRequest, CropRecommendationResponse, SingleCropRecommendation,
    FeedbackRequest, FeedbackResponse,
    RetrainResponse, SelfImprovingStatusResponse
)
from Backend.ai.predictor import CropGuardPredictor
from Backend.ai.self_improving_engine import SelfImprovingEngine

router = APIRouter(prefix="/ai", tags=["Self-Improving AI & Crop Recommender"])
predictor = CropGuardPredictor()
self_improving_engine = SelfImprovingEngine()

@router.post("/recommend-crop", response_model=CropRecommendationResponse)
async def recommend_crop_species(payload: CropRecommendationRequest):
    """
    Recommends optimal crop species given Soil N, P, K levels, pH, and local climatic variables.
    """
    try:
        result = predictor.recommend_crops(
            n=payload.n,
            p=payload.p,
            k=payload.k,
            temperature=payload.temperature,
            humidity=payload.humidity,
            ph=payload.ph,
            rainfall=payload.rainfall,
            top_k=payload.top_k or 3
        )

        # Log prediction telemetry
        self_improving_engine.log_telemetry(
            input_data=payload.dict(),
            prediction={
                "recommended_crop": result["recommended_crop"],
                "confidence": result["confidence"]
            },
            module="crop_recommendation"
        )

        recommendations = [
            SingleCropRecommendation(
                crop=r["crop"],
                confidence=r["confidence"],
                category=r.get("category", "Field Crop"),
                growing_season=r.get("growing_season", "Seasonal"),
                soil_type=r.get("soil_type", "Loamy"),
                water_requirement=r.get("water_requirement", "Moderate"),
                emoji=r.get("emoji", "🌱"),
                precautions=r.get("precautions", [])
            )
            for r in result.get("recommendations", [])
        ]

        return CropRecommendationResponse(
            success=True,
            recommended_crop=result["recommended_crop"],
            confidence=result["confidence"],
            recommendations=recommendations,
            input_parameters=result["input_parameters"],
            timestamp=result["timestamp"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crop recommendation failed: {str(e)}")

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_ai_feedback(payload: FeedbackRequest):
    """
    Submits ground truth, verified diagnoses, or farmer yield feedback into the self-improving active learning loop.
    """
    try:
        fb_result = self_improving_engine.log_feedback(
            feedback_type=payload.feedback_type,
            features=payload.features,
            ground_truth=payload.ground_truth,
            predicted_label=payload.predicted_label,
            confidence=payload.confidence,
            user_notes=payload.user_notes
        )

        # If auto retrain triggered and model was promoted, reload predictor weights
        if fb_result.get("auto_retrained") and fb_result.get("retrain_details", {}).get("promoted"):
            predictor.reload_artifacts()

        return FeedbackResponse(
            success=True,
            feedback_id=fb_result["feedback_id"],
            unprocessed_count=fb_result["unprocessed_count"],
            auto_retrained=fb_result["auto_retrained"],
            retrain_details=fb_result.get("retrain_details")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest feedback: {str(e)}")

@router.post("/trigger-retrain", response_model=RetrainResponse)
async def trigger_self_improvement(reason: Optional[str] = Query("On-Demand User Retrain Trigger")):
    """
    Forces automated retraining with newly accumulated feedback data, validation gating, and model versioning.
    """
    try:
        retrain_result = self_improving_engine.trigger_retraining(reason=reason or "Manual Trigger")

        if retrain_result.get("promoted"):
            predictor.reload_artifacts()

        return RetrainResponse(
            success=retrain_result.get("success", False),
            promoted=retrain_result.get("promoted", False),
            version=retrain_result.get("version"),
            validation_accuracy=retrain_result.get("validation_accuracy"),
            previous_accuracy=retrain_result.get("previous_accuracy"),
            samples_trained=retrain_result.get("samples_trained"),
            feedback_incorporated=retrain_result.get("feedback_incorporated"),
            reason=retrain_result.get("reason"),
            timestamp=retrain_result.get("timestamp", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining execution failed: {str(e)}")

@router.get("/self-improving-status", response_model=SelfImprovingStatusResponse)
async def get_self_improving_status():
    """
    Returns active engine state, model versions, accumulated telemetry, and learning trajectory.
    """
    try:
        state = self_improving_engine.get_state()
        history = self_improving_engine.get_history()

        return SelfImprovingStatusResponse(
            active_version=state.get("active_version", "v1.0.0"),
            last_retrained_at=state.get("last_retrained_at", ""),
            total_telemetry_count=state.get("total_telemetry_count", 0),
            total_feedback_count=state.get("total_feedback_count", 0),
            unprocessed_feedback_count=state.get("unprocessed_feedback_count", 0),
            current_recommendation_acc=state.get("current_recommendation_acc", 0.99),
            current_health_acc=state.get("current_health_acc", 0.89),
            retraining_trigger_threshold=state.get("retraining_trigger_threshold", 10),
            status=state.get("status", "Operational"),
            history=history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch self-improving status: {str(e)}")
