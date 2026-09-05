# CropGuard AI: REST API Documentation

Base URL (Development - Android Emulator): `http://10.0.2.2:8000`  
Base URL (Development - Localhost): `http://127.0.0.1:8000`  
Swagger UI Interactive Docs: `http://localhost:8000/docs`  
ReDoc Documentation: `http://localhost:8000/redoc`  

---

## 1. Health Check
- **Endpoint:** `GET /health`
- **Description:** Returns API operational status, service version, and AI engine components.
- **Response `200 OK`:**
```json
{
  "status": "healthy",
  "service": "CropGuard AI Backend",
  "version": "1.0.0",
  "timestamp": "2026-09-06T01:45:00.000Z",
  "ai_engine": {
    "ml_models": "scikit-learn (Linear Regression, Decision Tree, k-NN, K-Means)",
    "nlp_chatbot": "Local TF-IDF + Cosine Similarity + Reasoning Engine (Zero LLM API)",
    "reasoning": "Forward & Backward Chaining Rule Engine"
  }
}
```

---

## 2. Weather Telemetry
- **Endpoint:** `GET /weather`
- **Query Parameters:**
  - `city` *(optional, string)*: City or district name (e.g. `Nashik`, `New Delhi`).
  - `lat` *(optional, float)*: Latitude coordinate.
  - `lon` *(optional, float)*: Longitude coordinate.
- **Response `200 OK`:**
```json
{
  "temperature": 28.4,
  "humidity": 72.0,
  "rainfall": 14.5,
  "wind_speed": 16.2,
  "surface_pressure": 1011.8,
  "condition": "Rain Showers",
  "location_name": "Nashik, India",
  "source": "Open-Meteo (Real-Time Service)"
}
```

---

## 3. Crop Health Prediction
- **Endpoint:** `POST /predict`
- **Description:** Runs multi-model ML inference (Regression, Decision Tree, K-Means) and Forward/Backward Chaining expert reasoning.
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <supabase-jwt>` *(optional)*
- **Request Body:**
```json
{
  "crop": "Tomato",
  "weather": {
    "temperature": 32.0,
    "humidity": 85.0,
    "rainfall": 120.0,
    "wind_speed": 24.0,
    "location_name": "Nashik Agricultural Zone"
  },
  "soil_ph": 6.5,
  "n_content": 80.0,
  "p_content": 40.0,
  "k_content": 40.0,
  "user_id": "usr_948271"
}
```
- **Response `200 OK`:**
```json
{
  "crop": "Tomato",
  "location": "Nashik Agricultural Zone",
  "weather": {
    "temperature": 32.0,
    "humidity": 85.0,
    "rainfall": 120.0,
    "wind_speed": 24.0,
    "location_name": "Nashik Agricultural Zone"
  },
  "crop_health_score": 58.2,
  "health_status": "At Risk",
  "risk_level": "Moderate",
  "primary_risk_factor": "Ambient temperature (32.0°C) exceeds Tomato's optimal threshold of 28.0°C.",
  "agro_climatic_regime": "Moderate Climate Stress",
  "causes": [
    "Ambient temperature (32.0°C) exceeds Tomato's optimal threshold of 28.0°C.",
    "Excess moisture lingering on plant canopy foliage",
    "Dense vegetative cover reducing air circulation",
    "Elevated relative humidity coupled with frequent precipitation"
  ],
  "precautions": [
    "Thin lower foliage to enhance ventilation through the canopy",
    "Switch to drip irrigation and suspend overhead sprinkling",
    "Apply prophylactic protective bio-fungicide or copper spray",
    "Use drip irrigation to keep foliage dry and minimize fungal spore germination."
  ],
  "ai_explanation": "Verified 'fungal_disease_risk_high' via RULE_FUNGAL_HIGH. Required conditions ['humidity_high', 'rainfall_high'] are all satisfied by current observations: Prolonged leaf wetness and high relative humidity (>80%) accelerate fungal spore germination.",
  "timestamp": "2026-09-06T01:46:20.000Z"
}
```

---

## 4. Local AI Chatbot
- **Endpoint:** `POST /chat`
- **Description:** Domain-specific conversational retrieval with zero external LLM API dependencies.
- **Request Body:**
```json
{
  "message": "Why are my tomato leaves turning yellow?",
  "crop": "Tomato",
  "current_prediction": null,
  "user_id": "usr_948271"
}
```
- **Response `200 OK`:**
```json
{
  "answer": "Yellowing leaves (chlorosis) in crops typically stems from either: 1) Nitrogen deficiency, 2) Waterlogged roots inhibiting nutrient uptake, or 3) Root rot or viral infection. Inspect the lower leaves first; if accompanied by wet soils, improve drainage and apply light balanced foliar nutrition.",
  "confidence": 0.67,
  "matched_topic": "yellow_leaves_symptom",
  "category": "retrieval_qa",
  "reasoning_summary": "Matched topic 'yellow_leaves_symptom' via TF-IDF cosine similarity (0.518)."
}
```

---

## 5. Prediction History
- **Endpoint:** `GET /history?user_id=usr_948271&limit=20`
- **Description:** Returns past prediction records for the authenticated user, enforcing user isolation.
- **Response `200 OK`:** Returns array of prediction objects.

---

## 6. Farmer Profile
- **Endpoint:** `GET /profile?user_id=usr_948271&email=farmer@cropguard.ai`
- **Response `200 OK`:** Returns farmer profile record.
