import os
import sys
sys.path.insert(0, os.path.abspath("."))

import pytest
from fastapi.testclient import TestClient
from Backend.app import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "CropGuard AI" in data["service"]
    assert "ml_models" in data["ai_engine"]
    assert "nlp_chatbot" in data["ai_engine"]

def test_weather_endpoint_default():
    response = client.get("/weather?city=New Delhi")
    assert response.status_code == 200
    data = response.json()
    assert "temperature" in data
    assert "humidity" in data
    assert "rainfall" in data
    assert "wind_speed" in data

def test_predict_endpoint_healthy():
    payload = {
        "crop": "Wheat",
        "weather": {
            "temperature": 20.0,
            "humidity": 60.0,
            "rainfall": 60.0,
            "wind_speed": 10.0,
            "location_name": "Punjab Research Farm"
        },
        "soil_ph": 6.8
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "Wheat"
    assert 0.0 <= data["crop_health_score"] <= 100.0
    assert data["health_status"] in ["Healthy", "At Risk", "High Risk"]
    assert len(data["causes"]) > 0
    assert len(data["precautions"]) > 0
    assert len(data["ai_explanation"]) > 0

def test_predict_endpoint_high_risk():
    # Extreme conditions for Tomato: 38C heat, 95% humidity, 250mm torrential rain, 45km/h wind
    payload = {
        "crop": "Tomato",
        "weather": {
            "temperature": 38.0,
            "humidity": 95.0,
            "rainfall": 250.0,
            "wind_speed": 45.0,
            "location_name": "Coastal Station"
        },
        "soil_ph": 6.5
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "Tomato"
    # Should flag high risk or at risk with causes and precautions
    assert data["risk_level"] in ["Moderate", "High"]
    assert len(data["causes"]) >= 1

def test_chat_endpoint_crop_requirement():
    payload = {
        "message": "What is the best temperature for wheat?",
        "crop": "Wheat"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "15" in data["answer"] or "Wheat" in data["answer"]
    assert data["confidence"] >= 0.70

def test_chat_endpoint_backward_chaining():
    payload = {
        "message": "Why did you say fungal risk is high?"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "RULE_FUNGAL_HIGH" in data["answer"] or "humidity" in data["answer"].lower()

def test_chat_endpoint_context_awareness():
    mock_prediction = {
        "crop": "Rice",
        "health_status": "Healthy",
        "risk_level": "Low",
        "crop_health_score": 85.0,
        "causes": ["Normal monsoon precipitation."],
        "precautions": ["Maintain standing water."],
        "ai_explanation": "Temperature and humidity are ideal."
    }
    payload = {
        "message": "What should I do?",
        "current_prediction": mock_prediction
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Rice" in data["answer"] or "Healthy" in data["answer"] or "standing water" in data["answer"].lower()

def test_chat_endpoint_out_of_domain():
    payload = {
        "message": "Who won the basketball championship?"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "sufficient agricultural knowledge" in data["answer"] or data["confidence"] <= 0.30

def test_history_endpoint():
    response = client.get("/history?user_id=test-farmer-123")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_profile_endpoint():
    response = client.get("/profile?user_id=test-farmer-123&email=farmer@test.com")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test-farmer-123"
