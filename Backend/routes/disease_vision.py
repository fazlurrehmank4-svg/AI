from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body
from typing import Optional
from Backend.schemas.api_schemas import LeafScanRequest, LeafScanResponse
from Backend.ai.vision_classifier import CropDiseaseVisionClassifier
from Backend.ai.self_improving_engine import SelfImprovingEngine

router = APIRouter(prefix="/ai", tags=["Plant Disease Computer Vision"])
classifier = CropDiseaseVisionClassifier()
self_improving_engine = SelfImprovingEngine()

@router.post("/scan-leaf", response_model=LeafScanResponse)
async def scan_crop_leaf(payload: LeafScanRequest):
    """
    Diagnoses plant disease from base64 image string.
    Outputs disease class, confidence, severity, symptoms, causes, and curative precautions.
    """
    try:
        if not payload.image_base64:
            raise HTTPException(status_code=400, detail="image_base64 payload must not be empty.")

        result = classifier.diagnose_image(base64_str=payload.image_base64)

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Leaf scan diagnosis failed."))

        # Log prediction telemetry to self-improving engine
        self_improving_engine.log_telemetry(
            input_data={"crop_hint": payload.crop_hint, "type": "base64_scan"},
            prediction={
                "class_id": result["class_id"],
                "confidence": result["confidence"],
                "disease_name": result["disease_name"]
            },
            module="disease_vision_scan"
        )

        return LeafScanResponse(
            success=True,
            confidence=result["confidence"],
            class_id=result["class_id"],
            crop=result["crop"],
            disease_name=result["disease_name"],
            is_healthy=result["is_healthy"],
            severity=result["severity"],
            symptoms=result["symptoms"],
            causes=result["causes"],
            precautions=result["precautions"],
            top_predictions=result.get("top_predictions", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Leaf diagnosis error: {str(e)}")

@router.post("/scan-leaf-upload", response_model=LeafScanResponse)
async def scan_crop_leaf_file(file: UploadFile = File(...), crop_hint: Optional[str] = Form(None)):
    """
    Diagnoses plant disease from multipart image file upload.
    """
    try:
        image_bytes = await file.read()
        result = classifier.diagnose_image(image_bytes=image_bytes)

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Leaf scan diagnosis failed."))

        self_improving_engine.log_telemetry(
            input_data={"crop_hint": crop_hint, "filename": file.filename},
            prediction={
                "class_id": result["class_id"],
                "confidence": result["confidence"],
                "disease_name": result["disease_name"]
            },
            module="disease_vision_scan"
        )

        return LeafScanResponse(
            success=True,
            confidence=result["confidence"],
            class_id=result["class_id"],
            crop=result["crop"],
            disease_name=result["disease_name"],
            is_healthy=result["is_healthy"],
            severity=result["severity"],
            symptoms=result["symptoms"],
            causes=result["causes"],
            precautions=result["precautions"],
            top_predictions=result.get("top_predictions", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Leaf upload diagnosis error: {str(e)}")
