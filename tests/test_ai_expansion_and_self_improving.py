"""
Comprehensive Test Suite for AI Model Expansion, Crop Recommender,
Plant Disease Vision, and Self-Improving Continuous Learning Engine.
"""

import os
import json
import pytest
import numpy as np
from fastapi.testclient import TestClient

from Backend.app import app
from Backend.ai.predictor import CropGuardPredictor
from Backend.ai.vision_classifier import CropDiseaseVisionClassifier
from Backend.ai.self_improving_engine import SelfImprovingEngine

client = TestClient(app)

def test_expanded_knowledge_base():
    """Verify that all 28+ fruits and vegetables are present in the knowledge base."""
    kb_path = "Data/knowledge_base/crop_knowledge.json"
    assert os.path.exists(kb_path), "crop_knowledge.json missing"
    with open(kb_path, "r") as f:
        kb = json.load(f)

    # Check key representative fruits, vegetables, pulses, and cash crops
    expected_crops = [
        "Rice", "Wheat", "Maize", "Tomato", "Potato", "Pepper",
        "Apple", "Cherry", "Peach", "Grapes", "Strawberry",
        "Banana", "Mango", "Orange", "Papaya", "Pomegranate",
        "Watermelon", "Muskmelon", "Coconut", "Coffee",
        "Chickpea", "Kidneybeans", "Pigeonpeas", "Mothbeans",
        "Mungbean", "Blackgram", "Lentil", "Cotton", "Sugarcane", "Jute"
    ]

    for crop in expected_crops:
        assert crop in kb, f"Crop {crop} missing from knowledge base!"
        assert "temp_optimal" in kb[crop]
        assert "humidity_optimal" in kb[crop]
        assert "rainfall_optimal" in kb[crop]
        assert "diseases" in kb[crop] or "precautions" in kb[crop]
    print(f"\n[Test Passed] Verified {len(expected_crops)} distinct crops in knowledge base.")

def test_crop_predictor_multi_crop():
    """Verify prediction across diverse fruits and vegetables."""
    predictor = CropGuardPredictor()

    crops_to_test = ["Apple", "Mango", "Tomato", "Strawberry", "Rice", "Cotton"]
    for crop in crops_to_test:
        res = predictor.predict(
            crop=crop,
            temperature=24.0,
            humidity=60.0,
            rainfall=75.0,
            wind_speed=10.0,
            location_name="Test Farm"
        )
        assert res["crop"] == crop
        assert 0.0 <= res["crop_health_score"] <= 100.0
        assert res["health_status"] in ["Healthy", "At Risk", "High Risk"]
        assert len(res["causes"]) > 0
        assert len(res["precautions"]) > 0
    print(f"\n[Test Passed] Multi-crop health prediction successfully validated across {len(crops_to_test)} species.")

def test_crop_recommendation():
    """Verify crop recommendation ML model."""
    predictor = CropGuardPredictor()
    res = predictor.recommend_crops(
        n=90.0,
        p=42.0,
        k=43.0,
        temperature=21.0,
        humidity=82.0,
        ph=6.5,
        rainfall=200.0,
        top_k=3
    )
    assert res["success"] is True
    assert len(res["recommendations"]) == 3
    assert res["recommended_crop"] is not None
    assert 0.0 <= res["confidence"] <= 1.0
    print(f"\n[Test Passed] Crop recommendation returned top crop: {res['recommended_crop']} (Confidence: {res['confidence']})")

def test_self_improving_engine_feedback_and_retrain():
    """Verify continuous learning feedback ingestion and automated retraining."""
    engine = SelfImprovingEngine(store_dir="Data/feedback_store")
    
    initial_state = engine.get_state()
    assert initial_state is not None
    assert "active_version" in initial_state

    # Ingest verified farmer feedback
    fb_res = engine.log_feedback(
        feedback_type="crop_recommendation",
        features={
            "n": 85.0, "p": 50.0, "k": 40.0,
            "temperature": 23.0, "humidity": 80.0,
            "ph": 6.8, "rainfall": 210.0
        },
        ground_truth="rice",
        predicted_label="rice",
        confidence=0.98,
        user_notes="Field test verification in Punjab"
    )
    assert fb_res["success"] is True
    assert fb_res["feedback_id"] is not None

    # Trigger self-improvement retraining
    retrain_res = engine.trigger_retraining(reason="Unit Test Retraining")
    assert retrain_res["success"] is True
    assert "validation_accuracy" in retrain_res
    assert retrain_res["samples_trained"] >= 2200

    new_state = engine.get_state()
    assert new_state["unprocessed_feedback_count"] == 0
    print(f"\n[Test Passed] Self-Improving cycle complete. Active Version: {new_state['active_version']} | Acc: {new_state['current_recommendation_acc']*100:.2f}%")

def test_fastapi_endpoints():
    """Verify REST API endpoints."""
    # 1. Health endpoint
    h_resp = client.get("/health")
    assert h_resp.status_code == 200

    # 2. Crop recommendation endpoint
    rec_resp = client.post("/ai/recommend-crop", json={
        "n": 60.0, "p": 55.0, "k": 44.0,
        "temperature": 23.0, "humidity": 82.0,
        "ph": 7.8, "rainfall": 260.0,
        "top_k": 3
    })
    assert rec_resp.status_code == 200
    rec_data = rec_resp.json()
    assert rec_data["success"] is True
    assert len(rec_data["recommendations"]) == 3

    # 3. Self-improving status endpoint
    status_resp = client.get("/ai/self-improving-status")
    assert status_resp.status_code == 200
    status_data = status_resp.json()
    assert "active_version" in status_data
    assert "history" in status_data

    # 4. Leaf scan diagnosis endpoint
    scan_resp = client.post("/ai/scan-leaf", json={
        "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
        "crop_hint": "Tomato"
    })
    assert scan_resp.status_code == 200
    scan_data = scan_resp.json()
    assert scan_data["success"] is True
    assert "disease_name" in scan_data
    assert len(scan_data["precautions"]) > 0

    print("\n[Test Passed] All FastAPI endpoints passed validation.")

def test_chatbot_weather_and_hindi():
    """Verify chatbot weather reasoning, crop precaution lookups, and Hindi language support."""
    # Test 1: English weather & precaution question
    resp_en = client.post("/chat", json={
        "message": "what about my rice field any precautions",
        "crop": "Rice"
    })
    assert resp_en.status_code == 200
    data_en = resp_en.json()
    assert "answer" in data_en
    assert "Rice" in data_en["answer"] or "water" in data_en["answer"].lower() or "drainage" in data_en["answer"].lower()
    assert data_en["confidence"] >= 0.70

    # Test 2: Dynamic weather stress evaluation
    resp_weather = client.post("/chat", json={
        "message": "is today's weather good for rice?",
        "crop": "Rice",
        "current_prediction": {
            "crop": "Rice",
            "crop_health_score": 88.0,
            "health_status": "Healthy",
            "weather": {
                "temperature": 28.0,
                "humidity": 75.0,
                "rainfall": 180.0,
                "wind_speed": 12.0,
                "surface_pressure": 1013.0,
                "location_name": "Kashmir"
            },
            "causes": [],
            "precautions": ["Maintain standing water 3-5cm"],
            "growth_stage": "Tillering",
            "risk_factors": {}
        }
    })
    assert resp_weather.status_code == 200
    data_weather = resp_weather.json()
    assert "28" in data_weather["answer"] or "Favorable" in data_weather["answer"] or "temperature" in data_weather["answer"].lower()
    assert data_weather["confidence"] >= 0.85

    # Test 3: Devanagari Hindi question
    resp_hi = client.post("/chat", json={
        "message": "धान की फसल के लिए क्या सावधानियां हैं?",
        "language": "hi"
    })
    assert resp_hi.status_code == 200
    data_hi = resp_hi.json()
    assert any(c in data_hi["answer"] for c in ["धान", "चावल", "पानी", "तापमान", "सावधानी", "सेंटीमीटर"])
    assert data_hi["confidence"] >= 0.70

    # Test 4: Hinglish weather question
    resp_hinglish = client.post("/chat", json={
        "message": "kya mausam accha hai tamatar ke liye?",
        "crop": "Tomato"
    })
    assert resp_hinglish.status_code == 200
    data_hinglish = resp_hinglish.json()
    assert len(data_hinglish["answer"]) > 20
    assert data_hinglish["confidence"] >= 0.70

    print("\n[Test Passed] Chatbot weather knowledge and Hindi language support fully verified.")

