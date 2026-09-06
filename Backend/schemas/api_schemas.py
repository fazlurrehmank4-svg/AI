from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class WeatherData(BaseModel):
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Relative humidity percentage (0-100)")
    rainfall: float = Field(..., description="Rainfall in mm")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    surface_pressure: Optional[float] = Field(None, description="Surface pressure in hPa")
    condition: Optional[str] = Field("Normal", description="Weather condition description")
    location_name: Optional[str] = Field("Local Farm", description="City / locality name")

class PredictRequest(BaseModel):
    crop: str = Field(..., description="Crop name (e.g. Tomato, Rice, Wheat, Cotton, Apple, Mango)")
    weather: WeatherData = Field(..., description="Observed or fetched weather data")
    soil_ph: Optional[float] = Field(6.5, description="Soil pH value (0-14)")
    n_content: Optional[float] = Field(80.0, description="Nitrogen content kg/ha")
    p_content: Optional[float] = Field(40.0, description="Phosphorus content kg/ha")
    k_content: Optional[float] = Field(40.0, description="Potassium content kg/ha")
    user_id: Optional[str] = Field(None, description="Authenticated Supabase User UUID")

class PredictResponse(BaseModel):
    crop: str
    location: str
    weather: WeatherData
    crop_health_score: float = Field(..., description="Continuous health score (0-100)")
    health_status: str = Field(..., description="'Healthy', 'At Risk', or 'High Risk'")
    risk_level: str = Field(..., description="'Low', 'Moderate', or 'High'")
    primary_risk_factor: str
    agro_climatic_regime: str
    causes: List[str]
    precautions: List[str]
    ai_explanation: str
    timestamp: str

class ChatRequest(BaseModel):
    message: str = Field(..., description="Farmer question or query")
    crop: Optional[str] = Field(None, description="Active crop context")
    current_prediction: Optional[Dict[str, Any]] = Field(None, description="Active prediction context")
    language: Optional[str] = Field("auto", description="Preferred response language: 'en', 'hi', 'ur', or 'auto'")
    user_id: Optional[str] = Field(None, description="Authenticated User UUID")

class ChatResponse(BaseModel):
    answer: str
    confidence: float
    matched_topic: str
    category: str
    reasoning_summary: str

class ChatFeedbackRequest(BaseModel):
    query: str = Field(..., description="Original user query")
    answer: str = Field(..., description="Chatbot answer generated")
    rating: int = Field(..., description="1 for helpful/thumbs-up, -1 for unhelpful/thumbs-down")
    correct_topic: Optional[str] = Field(None, description="Optional corrected topic or category")
    user_correction: Optional[str] = Field(None, description="Optional user supplied correct text")
    language: Optional[str] = Field("en", description="Language code")


class HistoryItem(BaseModel):
    id: Optional[str] = None
    user_id: str
    crop: str
    location: str
    weather: Dict[str, Any]
    crop_health_score: float
    health_status: str
    risk_level: str
    causes: List[str]
    precautions: List[str]
    created_at: Optional[str] = None

class ProfileSchema(BaseModel):
    id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    farm_location: Optional[str] = None
    primary_crops: Optional[List[str]] = []

class DailyForecastAlert(BaseModel):
    date: str
    day_name: str
    temp_max: float
    temp_min: float
    rainfall: float
    wind_speed: float
    condition: str
    weather_code: int
    risk_level: str
    has_harm: bool
    harm_summary: str
    precautions: List[str]

class ForecastAlertResponse(BaseModel):
    crop: str
    location: str
    overall_threat_level: str
    summary: str
    alerts: List[DailyForecastAlert]
    timestamp: str

# --- Crop Recommendation Schemas ---
class CropRecommendationRequest(BaseModel):
    n: float = Field(..., description="Soil Nitrogen (N) content in kg/ha")
    p: float = Field(..., description="Soil Phosphorus (P) content in kg/ha")
    k: float = Field(..., description="Soil Potassium (K) content in kg/ha")
    temperature: float = Field(..., description="Average ambient temperature in Celsius")
    humidity: float = Field(..., description="Relative humidity %")
    ph: float = Field(..., description="Soil pH value (0.0 - 14.0)")
    rainfall: float = Field(..., description="Annual or seasonal rainfall in mm")
    top_k: Optional[int] = Field(3, description="Number of top crop suggestions to return")

class SingleCropRecommendation(BaseModel):
    crop: str
    confidence: float
    category: str
    growing_season: str
    soil_type: str
    water_requirement: str
    emoji: str
    precautions: List[str]

class CropRecommendationResponse(BaseModel):
    success: bool
    recommended_crop: str
    confidence: float
    recommendations: List[SingleCropRecommendation]
    input_parameters: Dict[str, float]
    timestamp: str

# --- Computer Vision Leaf Scan Schemas ---
class LeafScanRequest(BaseModel):
    image_base64: Optional[str] = Field(None, description="Base64 encoded image string (JPEG/PNG/WebP)")
    crop_hint: Optional[str] = Field(None, description="Optional crop hint (e.g. Tomato, Apple)")

class TopPredictionItem(BaseModel):
    class_id: str
    name: str
    crop: str
    confidence: float

class LeafScanResponse(BaseModel):
    success: bool
    confidence: float
    class_id: str
    crop: str
    disease_name: str
    is_healthy: bool
    severity: str
    symptoms: str
    causes: str
    precautions: List[str]
    top_predictions: List[TopPredictionItem]

# --- Self-Improving AI Schemas ---
class FeedbackRequest(BaseModel):
    feedback_type: str = Field(..., description="'crop_recommendation', 'disease_scan', or 'health_prediction'")
    features: Dict[str, Any] = Field(..., description="Input features (e.g. NPK, weather, image meta)")
    ground_truth: str = Field(..., description="Correct verified crop or disease diagnosis label")
    predicted_label: Optional[str] = Field(None, description="What the AI originally predicted")
    confidence: Optional[float] = Field(None, description="Model confidence")
    user_notes: Optional[str] = Field(None, description="Agronomist / farmer comments")

class FeedbackResponse(BaseModel):
    success: bool
    feedback_id: str
    unprocessed_count: int
    auto_retrained: bool
    retrain_details: Optional[Dict[str, Any]] = None

class RetrainResponse(BaseModel):
    success: bool
    promoted: bool
    version: Optional[str] = None
    validation_accuracy: Optional[float] = None
    previous_accuracy: Optional[float] = None
    samples_trained: Optional[int] = None
    feedback_incorporated: Optional[int] = None
    reason: Optional[str] = None
    timestamp: str

class SelfImprovingStatusResponse(BaseModel):
    active_version: str
    last_retrained_at: str
    total_telemetry_count: int
    total_feedback_count: int
    unprocessed_feedback_count: int
    current_recommendation_acc: float
    current_health_acc: float
    retraining_trigger_threshold: int
    status: str
    history: List[Dict[str, Any]]
