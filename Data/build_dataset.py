import json
import os
import numpy as np
import pandas as pd

# Define crop agronomic profiles based on FAO and Kaggle Agricultural Data standards
CROP_PROFILES = {
    "Rice": {
        "temp_optimal": (22.0, 32.0),
        "humidity_optimal": (70.0, 85.0),
        "rainfall_optimal": (150.0, 300.0),
        "ph_optimal": (5.5, 7.0),
        "water_requirement": "High",
        "soil_type": "Clayey loam, alluvial",
        "growing_season": "Kharif (Monsoon)",
        "diseases": [
            {
                "name": "Bacterial Leaf Blight",
                "risk_trigger": "High humidity (>80%) and warm temp (>28C) with rainfall",
                "symptoms": "Water-soaked lesions on leaves turning yellowish-white with wavy margins.",
                "causes": "High humidity, excessive nitrogen fertilization, and prolonged leaf wetness.",
                "precautions": "Avoid excess nitrogen, ensure field drainage, spray copper-based bactericides if verified.",
            },
            {
                "name": "Rice Blast (Pyricularia oryzae)",
                "risk_trigger": "High humidity (>85%), overcast days, temp 20-26C",
                "symptoms": "Spindle-shaped spots with gray/white centers and brownish margins.",
                "causes": "Excessive wetness on foliage, moderate temperatures, and crowded planting.",
                "precautions": "Maintain spacing, avoid excessive vegetative wetness, apply recommended bio-fungicides.",
            },
        ],
        "precautions": [
            "Maintain controlled standing water (2-5 cm); drain excess flood water during storm surges.",
            "Avoid excessive chemical nitrogen application during cloudy and humid periods.",
            "Scout weekly for stem borer and blast lesions during panicle initiation.",
        ],
    },
    "Wheat": {
        "temp_optimal": (15.0, 25.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (50.0, 100.0),
        "ph_optimal": (6.0, 7.5),
        "water_requirement": "Moderate",
        "soil_type": "Well-drained loamy soil",
        "growing_season": "Rabi (Winter)",
        "diseases": [
            {
                "name": "Yellow / Stripe Rust",
                "risk_trigger": "Cool temperature (10-20C) combined with high relative humidity (>75%)",
                "symptoms": "Yellow pustules arranged in linear stripes on leaf blades.",
                "causes": "Prolonged cool moist weather and wind-borne spores.",
                "precautions": "Plant resistant cultivars, monitor early morning dew periods, apply triazole fungicides if risk escalates.",
            },
            {
                "name": "Terminal Heat Stress",
                "risk_trigger": "Temperature exceeding 30C during grain filling stage",
                "symptoms": "Premature leaf senescence, shriveled grains, and forced maturity.",
                "causes": "Late sowing and sudden temperature spikes.",
                "precautions": "Ensure light irrigation to reduce canopy temperature; apply potassium nitrate spray.",
            },
        ],
        "precautions": [
            "Do not over-irrigate during flowering to prevent root lodging and rust susceptibility.",
            "Ensure balanced fertilization with adequate phosphorus and potassium.",
            "Monitor soil moisture at crown root initiation and flowering stages.",
        ],
    },
    "Maize": {
        "temp_optimal": (20.0, 30.0),
        "humidity_optimal": (55.0, 75.0),
        "rainfall_optimal": (60.0, 120.0),
        "ph_optimal": (5.8, 7.2),
        "water_requirement": "Moderate",
        "soil_type": "Deep, well-drained fertile loam",
        "growing_season": "Kharif / Spring",
        "diseases": [
            {
                "name": "Maydis Leaf Blight",
                "risk_trigger": "Warm (20-30C) and humid weather (>80% humidity)",
                "symptoms": "Elongated diamond-shaped necrotic lesions between leaf veins.",
                "causes": "High humidity, warm temperatures, and infected plant residue.",
                "precautions": "Rotate crops, remove crop debris, avoid dense plant spacing.",
            },
            {
                "name": "Fall Armyworm Damage Risk",
                "risk_trigger": "Warm dry spells interrupted by moderate humidity",
                "symptoms": "Pinholes, window-pane feeding in whorl, copious frass.",
                "causes": "Favorable warm temperatures accelerating larval development cycles.",
                "precautions": "Install pheromone traps; apply neem formulations at early whorl stage.",
            },
        ],
        "precautions": [
            "Ensure proper drainage; maize roots cannot tolerate waterlogging beyond 24-48 hours.",
            "Apply top-dressed nitrogen in split doses at knee-high and tasseling stages.",
            "Mulch between rows to preserve moisture during dry spells.",
        ],
    },
    "Cotton": {
        "temp_optimal": (21.0, 32.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (50.0, 110.0),
        "ph_optimal": (6.0, 8.0),
        "water_requirement": "Moderate",
        "soil_type": "Deep black soil (Regur), alluvial",
        "growing_season": "Kharif",
        "diseases": [
            {
                "name": "Bacterial Blight / Angular Leaf Spot",
                "risk_trigger": "High humidity (>80%) and temperature (28-34C)",
                "symptoms": "Angular water-soaked spots bounded by leaf veinlets.",
                "causes": "Wind-driven rain, high humidity, and warm weather.",
                "precautions": "Seed treatment with bactericide; avoid overhead sprinkler irrigation.",
            },
            {
                "name": "Boll Rot Complex",
                "risk_trigger": "Prolonged rainfall, overcast weather, and relative humidity >85%",
                "symptoms": "Discolored, softening bolls failing to open properly.",
                "causes": "Secondary fungal entry following insect punctures in wet weather.",
                "precautions": "Prune lower leaves if foliage is extremely dense; improve field aeration.",
            },
        ],
        "precautions": [
            "Avoid standing water; cotton is sensitive to root asphyxiation in waterlogged soils.",
            "Monitor whitefly and bollworm populations during square formation.",
            "Apply micronutrients (boron and zinc) during flowering and boll retention.",
        ],
    },
    "Tomato": {
        "temp_optimal": (18.0, 28.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (40.0, 90.0),
        "ph_optimal": (6.0, 7.0),
        "water_requirement": "Moderate-High",
        "soil_type": "Well-drained sandy loam rich in organic matter",
        "growing_season": "Year-round / Rabi / Kharif",
        "diseases": [
            {
                "name": "Early Blight (Alternaria solani)",
                "risk_trigger": "Warm temperatures (24-29C) and alternating wet/dry conditions",
                "symptoms": "Concentric rings ('target board' pattern) on older lower leaves.",
                "causes": "Foliar wetness from dew or rain followed by warm sunshine.",
                "precautions": "Stake plants, mulch to prevent soil splashing, remove lower diseased leaves.",
            },
            {
                "name": "Late Blight (Phytophthora infestans)",
                "risk_trigger": "Cool, cloudy weather (15-22C) with high relative humidity (>85%)",
                "symptoms": "Water-soaked irregular lesions with white mold on leaf undersides.",
                "causes": "Continuous leaf wetness and cool humid microclimates.",
                "precautions": "Apply preventive copper/mancozeb sprays before continuous rain spells; avoid overhead watering.",
            },
        ],
        "precautions": [
            "Use drip irrigation to keep foliage dry and minimize fungal spore germination.",
            "Stake and prune indeterminate varieties to optimize airflow and sunlight penetration.",
            "Ensure calcium availability to avoid blossom end rot under variable moisture conditions.",
        ],
    },
    "Potato": {
        "temp_optimal": (16.0, 24.0),
        "humidity_optimal": (60.0, 80.0),
        "rainfall_optimal": (50.0, 100.0),
        "ph_optimal": (5.0, 6.5),
        "water_requirement": "Moderate",
        "soil_type": "Loose, friable sandy loam",
        "growing_season": "Rabi (Winter)",
        "diseases": [
            {
                "name": "Potato Late Blight",
                "risk_trigger": "Temp 10-21C with RH >90% for 2+ consecutive days",
                "symptoms": "Rapid blighting of leaves and stems with purplish-brown decay.",
                "causes": "Cool, foggy weather and persistent wet canopy conditions.",
                "precautions": "Earthing up to shield tubers; timely preventive protective sprays.",
            },
            {
                "name": "Common Scab",
                "risk_trigger": "Dry, warm soil conditions during tuber initiation (pH > 6.8)",
                "symptoms": "Corky lesions and pitted scabs on tuber surfaces.",
                "causes": "Low soil moisture at tuberization combined with alkaline soil.",
                "precautions": "Maintain consistent soil moisture for 4-6 weeks after tuber initiation.",
            },
        ],
        "precautions": [
            "Perform proper earthing up to prevent tuber greening and late blight spore wash-down.",
            "Avoid water stagnation which rapidly induces bacterial soft rot in tubers.",
            "Stop irrigation 10-14 days prior to harvesting to promote tuber skin curing.",
        ],
    },
    "Sugarcane": {
        "temp_optimal": (24.0, 35.0),
        "humidity_optimal": (65.0, 85.0),
        "rainfall_optimal": (100.0, 200.0),
        "ph_optimal": (6.0, 7.8),
        "water_requirement": "Very High",
        "soil_type": "Deep rich loamy soil",
        "growing_season": "Annual (10-14 months)",
        "diseases": [
            {
                "name": "Red Rot (Colletotrichum falcatum)",
                "risk_trigger": "High humidity (>85%), waterlogging, and temp 25-32C",
                "symptoms": "Discoloration of crown leaves, internal red discoloration with white patches across stalks.",
                "causes": "Waterlogging, infected seed setts, and stagnant humid fields.",
                "precautions": "Use certified disease-free setts, ensure field drainage, avoid ratoon cropping infected fields.",
            }
        ],
        "precautions": [
            "Provide trash mulching to conserve moisture in early formative stages.",
            "Ensure drainage channels are clear before peak monsoon to avert red rot escalation.",
            "Perform propping or earthing up to prevent crop lodging during high wind events.",
        ],
    },
    "Chickpea": {
        "temp_optimal": (15.0, 25.0),
        "humidity_optimal": (40.0, 60.0),
        "rainfall_optimal": (30.0, 70.0),
        "ph_optimal": (6.0, 8.0),
        "water_requirement": "Low-Moderate",
        "soil_type": "Well-drained black cotton or sandy loam",
        "growing_season": "Rabi (Post-Monsoon/Winter)",
        "diseases": [
            {
                "name": "Ascochyta Blight",
                "risk_trigger": "Overcast cool weather (15-20C) with high humidity (>75%)",
                "symptoms": "Circular spots with concentric dark pycnidia rings on leaves and pods.",
                "causes": "Prolonged rainfall, heavy fog, and cool temperatures.",
                "precautions": "Select tolerant varieties; apply seed treatment; avoid dense canopies.",
            },
            {
                "name": "Fusarium Wilt",
                "risk_trigger": "High soil temperatures (>25C) and moisture stress",
                "symptoms": "Drooping petioles, internal vascular browning, sudden drying.",
                "causes": "Soil-borne pathogen activated by root stress and warm soils.",
                "precautions": "Practice 3-year crop rotation; avoid sowing in excessively warm early October soil.",
            },
        ],
        "precautions": [
            "Extremely sensitive to waterlogging; never allow water to stand in the field.",
            "Avoid excess irrigation which causes vegetative overgrowth at the expense of pod setting.",
            "Monitor pod borer (Helicoverpa armigera) at flowering and early pod stage.",
        ],
    },
}

def calculate_agronomic_health(crop_name, temp, humidity, rainfall, wind_speed=12.0):
    """
    Computes an objective, scientifically bounded Crop Health Score (0-100)
    and risk category based on agronomic bounds.
    """
    profile = CROP_PROFILES.get(crop_name, CROP_PROFILES["Wheat"])
    t_min, t_max = profile["temp_optimal"]
    h_min, h_max = profile["humidity_optimal"]
    r_min, r_max = profile["rainfall_optimal"]

    # Penalties for deviations
    temp_penalty = 0.0
    if temp < t_min:
        temp_penalty = min(40.0, (t_min - temp) * 3.5)
    elif temp > t_max:
        temp_penalty = min(45.0, (temp - t_max) * 4.0)

    hum_penalty = 0.0
    if humidity < h_min:
        hum_penalty = min(30.0, (h_min - humidity) * 1.2)
    elif humidity > h_max:
        hum_penalty = min(35.0, (humidity - h_max) * 1.5)

    rain_penalty = 0.0
    if rainfall < r_min:
        rain_penalty = min(35.0, ((r_min - rainfall) / max(1.0, r_min)) * 35.0)
    elif rainfall > r_max:
        rain_penalty = min(40.0, ((rainfall - r_max) / max(1.0, r_max)) * 40.0)

    wind_penalty = 0.0
    if wind_speed > 35.0:
        wind_penalty = min(25.0, (wind_speed - 35.0) * 1.5)

    total_penalty = temp_penalty + hum_penalty + rain_penalty + wind_penalty
    # Base health score starts at 100
    score = max(5.0, min(98.0, 100.0 - total_penalty))

    if score >= 75.0:
        status = "Healthy"
        risk_level = "Low"
    elif score >= 50.0:
        status = "At Risk"
        risk_level = "Moderate"
    else:
        status = "High Risk"
        risk_level = "High"

    # Identify primary risk factor
    factors = [
        ("Temperature Deviation", temp_penalty),
        ("Humidity Deviation", hum_penalty),
        ("Rainfall Deviation", rain_penalty),
        ("Wind Force", wind_penalty),
    ]
    factors.sort(key=lambda x: x[1], reverse=True)
    primary_risk = factors[0][0] if factors[0][1] > 5.0 else "Optimal Conditions"

    return round(score, 1), status, risk_level, primary_risk

def generate_datasets():
    os.makedirs("Data/raw", exist_ok=True)
    os.makedirs("Data/processed", exist_ok=True)
    os.makedirs("Data/knowledge_base", exist_ok=True)

    # 1. Save structured knowledge base JSON
    kb_file = "Data/knowledge_base/crop_knowledge.json"
    with open(kb_file, "w") as f:
        json.dump(CROP_PROFILES, f, indent=2)
    print(f"Generated {kb_file}")

    # 2. Generate comprehensive Kaggle-standard synthetic/calibrated dataset (2,400 samples across 8 crops)
    np.random.seed(42)
    records = []
    crops = list(CROP_PROFILES.keys())

    for crop in crops:
        profile = CROP_PROFILES[crop]
        t_min, t_max = profile["temp_optimal"]
        h_min, h_max = profile["humidity_optimal"]
        r_min, r_max = profile["rainfall_optimal"]
        ph_min, ph_max = profile["ph_optimal"]

        for _ in range(300):
            # Mix optimal, moderate stress, and high stress regimes
            regime = np.random.choice(["optimal", "moderate_stress", "high_stress"], p=[0.45, 0.35, 0.20])

            if regime == "optimal":
                temp = np.random.uniform(t_min, t_max)
                humidity = np.random.uniform(h_min, h_max)
                rainfall = np.random.uniform(r_min, r_max)
                wind = np.random.uniform(5.0, 20.0)
            elif regime == "moderate_stress":
                # slightly out of bound
                delta_t = np.random.choice([-1, 1]) * np.random.uniform(3.0, 8.0)
                temp = np.clip(np.random.uniform(t_min, t_max) + delta_t, 5.0, 48.0)
                delta_h = np.random.choice([-1, 1]) * np.random.uniform(10.0, 25.0)
                humidity = np.clip(np.random.uniform(h_min, h_max) + delta_h, 15.0, 98.0)
                delta_r = np.random.choice([-1, 1]) * np.random.uniform(0.3, 0.7) * r_min
                rainfall = max(0.0, np.random.uniform(r_min, r_max) + delta_r)
                wind = np.random.uniform(10.0, 32.0)
            else: # high stress
                delta_t = np.random.choice([-1, 1]) * np.random.uniform(9.0, 16.0)
                temp = np.clip(np.random.uniform(t_min, t_max) + delta_t, 2.0, 52.0)
                humidity = np.random.choice([np.random.uniform(10.0, 25.0), np.random.uniform(88.0, 99.0)])
                rainfall = np.random.choice([np.random.uniform(0.0, 10.0), np.random.uniform(r_max * 1.5, r_max * 2.5)])
                wind = np.random.uniform(25.0, 60.0)

            ph = np.random.uniform(ph_min - 0.5, ph_max + 0.5)
            n_val = np.random.uniform(20.0, 140.0)
            p_val = np.random.uniform(10.0, 90.0)
            k_val = np.random.uniform(15.0, 120.0)

            score, status, risk_level, primary_risk = calculate_agronomic_health(crop, temp, humidity, rainfall, wind)

            records.append({
                "crop": crop,
                "temperature": round(temp, 2),
                "humidity": round(humidity, 2),
                "rainfall": round(rainfall, 2),
                "wind_speed": round(wind, 2),
                "soil_ph": round(ph, 2),
                "n_content": round(n_val, 1),
                "p_content": round(p_val, 1),
                "k_content": round(k_val, 1),
                "crop_health_score": score,
                "health_status": status,
                "risk_level": risk_level,
                "primary_risk_factor": primary_risk,
            })

    df = pd.DataFrame(records)
    # Save raw and processed
    raw_path = "Data/raw/crop_weather_raw.csv"
    processed_path = "Data/processed/crop_weather_data.csv"
    df.to_csv(raw_path, index=False)
    df.to_csv(processed_path, index=False)
    print(f"Saved {raw_path} and {processed_path} with {len(df)} records across {len(crops)} crops.")

if __name__ == "__main__":
    generate_datasets()
