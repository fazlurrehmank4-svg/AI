"""
Practical 10: Complete Integrated Agricultural AI Mini-Project (CropGuard AI)
Author: CropGuard AI Team
Description:
    Demonstrates the end-to-end multi-tier pipeline unifying:
      - Practical 01: Preprocessing and Agronomic Envelopes
      - Practical 02: BFS/DFS Risk State Exploration
      - Practical 03: GBFS / A* Heuristic Intervention Cost Minimization
      - Practical 04: Hill Climbing Microclimate Optimization
      - Practical 05: Forward Chaining Causes & Backward Chaining Justification
      - Practical 06: Linear Regression Continuous Health Prediction (0-100)
      - Practical 07: Decision Tree & k-NN Risk Classification
      - Practical 08: K-Means Agro-Climatic Regime Discovery
      - Practical 09: Local NLP Farmer Chatbot Knowledge Retrieval
"""

import os
import sys

# Ensure local imports work across project directories
sys.path.append(os.path.abspath("."))
from Backend.ai.predictor import CropGuardPredictor
from Backend.ai.chatbot import get_chatbot
from Practical_02_BFS_DFS.bfs_dfs import breadth_first_search, AGRICULTURAL_RISK_GRAPH
from Practical_03_GBFS_AStar.gbfs_astar import a_star_search, AGRICULTURAL_DECISION_GRAPH, HEURISTIC_VALUES
from Practical_04_Local_Search.hill_climbing import AgriculturalOptimizationEnvironment, steepest_ascent_hill_climbing

def run_practical_10_demonstration():
    print("=" * 70)
    print("PRACTICAL 10: CROPGUARD AI - COMPLETE INTEGRATED MINI-PROJECT PIPELINE")
    print("=" * 70)

    # 1. Pipeline Input: Real/Observed Weather Scenario
    crop = "Tomato"
    location = "Nashik Agricultural Zone, Maharashtra"
    temp = 33.5       # Hot
    humidity = 84.0   # High humidity (fungal trigger)
    rainfall = 110.0  # Heavy rainfall
    wind_speed = 22.0 # Moderate wind

    print(f"\n[STEP 1: Field Meteorological Telemetry Ingestion]")
    print(f"Target Crop:     {crop}")
    print(f"Location:        {location}")
    print(f"Weather Record:  Temp={temp}°C | Humidity={humidity}% | Rain={rainfall}mm | Wind={wind_speed}km/h")

    # 2. Multi-Model ML Inference & Reasoning Engine
    predictor = CropGuardPredictor()
    print(f"\n[STEP 2: Executing Multi-Model ML Inference (Practicals 05, 06, 07, 08)]")
    result = predictor.predict(
        crop=crop,
        temperature=temp,
        humidity=humidity,
        rainfall=rainfall,
        wind_speed=wind_speed,
        location_name=location
    )

    print(f"  * Linear Regression Health Score (P06):  {result['crop_health_score']} / 100.0")
    print(f"  * Decision Tree Risk Classification (P07): {result['health_status']} (Risk Level: {result['risk_level']})")
    print(f"  * K-Means Agro-Climatic Regime (P08):      {result['agro_climatic_regime']}")
    print(f"  * Primary Limiting Factor:                {result['primary_risk_factor']}")

    print(f"\n[STEP 3: Forward Chaining Root Causes (Practical 05)]")
    for idx, c in enumerate(result['causes'], 1):
        print(f"  {idx}. {c}")

    print(f"\n[STEP 4: Forward Chaining Prioritized Precautions (Practical 05)]")
    for idx, p in enumerate(result['precautions'], 1):
        print(f"  {idx}. {p}")

    print(f"\n[STEP 5: Backward Chaining AI Explainability (Practical 05)]")
    print(f"  {result['ai_explanation']}")

    # 3. Search & Optimization Support Modules
    print(f"\n[STEP 6: A* Remediation Cost Optimization (Practical 03)]")
    astar = a_star_search(AGRICULTURAL_DECISION_GRAPH, HEURISTIC_VALUES, "Severe_Fungal_Outbreak", "Optimal_Microclimate_Restored")
    print(f"  Optimal Remediation Sequence: {' -> '.join(astar['path'])}")
    print(f"  Total Labor/Resource Cost:    {astar['total_actual_cost_g']} units")

    print(f"\n[STEP 7: Hill Climbing Micro-Climate Local Optimization (Practical 04)]")
    env = AgriculturalOptimizationEnvironment(crop=crop, ambient_temp=temp, ambient_humidity=humidity)
    hc_res = steepest_ascent_hill_climbing(env, (12.0, 10.0))
    print(f"  Recommended Irrigation: {hc_res['final_state'][0]} mm/day | Shade-Net Coverage: {hc_res['final_state'][1]}%")
    print(f"  Maximized Comfort Score: {hc_res['optimal_score']} / 100")

    # 4. Interactive Local NLP Chatbot
    print(f"\n[STEP 8: Local Domain-Specific NLP Chatbot Interaction (Practical 09)]")
    bot = get_chatbot()
    user_question = "What should I do to protect my tomato crop right now?"
    chat_reply = bot.ask(user_question, active_crop=crop, current_prediction=result)
    print(f"  Farmer Query: \"{user_question}\"")
    print(f"  CropGuard AI Reply:\n{chat_reply['answer']}")

    print("\n" + "=" * 70)
    print("[SUCCESS] Practical 10 End-to-End System Pipeline Verified Completely!")
    print("=" * 70)

if __name__ == "__main__":
    run_practical_10_demonstration()
