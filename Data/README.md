# CropGuard AI: Agricultural & Weather Datasets

This directory contains the Kaggle-calibrated agricultural knowledge base and crop-weather interaction datasets utilized across all 10 AI Practicals and the FastAPI backend.

---

## 1. Directory Structure

```
Data/
├── raw/
│   └── crop_weather_raw.csv        # Baseline agricultural observations
├── processed/
│   └── crop_weather_data.csv      # Cleaned, normalized dataset with agronomic health scores
├── knowledge_base/
│   └── crop_knowledge.json        # Structured agronomic envelopes, diseases, causes, and precautions
├── build_dataset.py               # Deterministic pipeline script
└── README.md                      # Dataset documentation
```

---

## 2. Dataset Features & Agronomic Specifications

| Feature | Data Type | Units / Format | Agronomic Significance |
| :--- | :--- | :--- | :--- |
| `crop` | Categorical | Rice, Wheat, Maize, Cotton, Tomato, Potato, Sugarcane, Chickpea | Target crop species |
| `temperature` | Numeric (Float) | °C | Ambient canopy temperature affecting enzymatic and photosynthesis rate |
| `humidity` | Numeric (Float) | % (Relative Humidity) | Atmospheric moisture driving fungal spore propagation and transpiration |
| `rainfall` | Numeric (Float) | mm (Precipitation) | Soil moisture input; high values cause waterlogging and root rot |
| `wind_speed` | Numeric (Float) | km/h | Mechanical stress, spore dispersal, and evapotranspiration |
| `soil_ph` | Numeric (Float) | 0 - 14 scale | Nutrient uptake availability |
| `n_content` | Numeric (Float) | kg/ha | Soil Nitrogen availability |
| `p_content` | Numeric (Float) | kg/ha | Soil Phosphorus availability |
| `k_content` | Numeric (Float) | kg/ha | Soil Potassium availability |
| `crop_health_score` | Numeric (Float) | 0.0 - 100.0 | Continuous composite index of physiological crop vigor |
| `health_status` | Categorical | `Healthy`, `At Risk`, `High Risk` | Multiclass health classification |
| `risk_level` | Categorical | `Low`, `Moderate`, `High` | Operational risk level for farmer intervention |
| `primary_risk_factor` | Categorical | Deviation description | Primary limiting factor identified |

---

## 3. Knowledge Base Schema (`crop_knowledge.json`)

Each crop entry in `crop_knowledge.json` defines:
- **`temp_optimal`**: Tuple of `[min_temp, max_temp]`
- **`humidity_optimal`**: Tuple of `[min_humidity, max_humidity]`
- **`rainfall_optimal`**: Tuple of `[min_rainfall, max_rainfall]`
- **`soil_type`**: Soil mechanical suitability
- **`diseases`**: List of susceptible pathologies with `risk_trigger`, `symptoms`, `causes`, and `precautions`.
- **`precautions`**: Standard agronomic stewardship and cultural practices.

---

## 4. Scientific Disclaimer

> [!NOTE]
> This dataset and the resulting models are designed for **educational decision-support purposes**. Field management decisions should integrate on-site agronomist inspections, extension advisories, and certified chemical label directives.
