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
    crop: str = Field(..., description="Crop name (e.g. Tomato, Rice, Wheat, Cotton)")
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
    user_id: Optional[str] = Field(None, description="Authenticated User UUID")

class ChatResponse(BaseModel):
    answer: str
    confidence: float
    matched_topic: str
    category: str
    reasoning_summary: str

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
