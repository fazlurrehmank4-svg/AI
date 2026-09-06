import json
import os
import numpy as np
import pandas as pd

# Comprehensive crop agronomic profiles based on FAO, ICAR, and Kaggle Agricultural Data standards
CROP_PROFILES = {
    # --- CEREALS & GRAINS ---
    "Rice": {
        "category": "Cereal Grain",
        "temp_optimal": (22.0, 32.0),
        "humidity_optimal": (70.0, 85.0),
        "rainfall_optimal": (150.0, 300.0),
        "ph_optimal": (5.5, 7.0),
        "water_requirement": "High",
        "soil_type": "Clayey loam, alluvial",
        "growing_season": "Kharif (Monsoon)",
        "emoji": "🍚",
        "diseases": [
            {
                "name": "Bacterial Leaf Blight",
                "risk_trigger": "High humidity (>80%) and warm temp (>28C) with rainfall",
                "symptoms": "Water-soaked lesions on leaves turning yellowish-white with wavy margins.",
                "causes": "High humidity, excessive nitrogen fertilization, and prolonged leaf wetness.",
                "precautions": "Avoid excess nitrogen, ensure field drainage, spray copper-based bactericides if verified."
            },
            {
                "name": "Rice Blast (Pyricularia oryzae)",
                "risk_trigger": "High humidity (>85%), overcast days, temp 20-26C",
                "symptoms": "Spindle-shaped spots with gray/white centers and brownish margins.",
                "causes": "Excessive wetness on foliage, moderate temperatures, and crowded planting.",
                "precautions": "Maintain spacing, avoid excessive vegetative wetness, apply recommended bio-fungicides."
            }
        ],
        "precautions": [
            "Maintain controlled standing water (2-5 cm); drain excess flood water during storm surges.",
            "Avoid excessive chemical nitrogen application during cloudy and humid periods.",
            "Scout weekly for stem borer and blast lesions during panicle initiation."
        ]
    },
    "Wheat": {
        "category": "Cereal Grain",
        "temp_optimal": (15.0, 25.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (50.0, 100.0),
        "ph_optimal": (6.0, 7.5),
        "water_requirement": "Moderate",
        "soil_type": "Well-drained loamy soil",
        "growing_season": "Rabi (Winter)",
        "emoji": "🌾",
        "diseases": [
            {
                "name": "Yellow / Stripe Rust",
                "risk_trigger": "Cool temperature (10-20C) combined with high relative humidity (>75%)",
                "symptoms": "Yellow pustules arranged in linear stripes on leaf blades.",
                "causes": "Prolonged cool moist weather and wind-borne spores.",
                "precautions": "Plant resistant cultivars, monitor early morning dew periods, apply triazole fungicides if risk escalates."
            },
            {
                "name": "Terminal Heat Stress",
                "risk_trigger": "Temperature exceeding 30C during grain filling stage",
                "symptoms": "Premature leaf senescence, shriveled grains, and forced maturity.",
                "causes": "Late sowing and sudden temperature spikes.",
                "precautions": "Ensure light irrigation to reduce canopy temperature; apply potassium nitrate spray."
            }
        ],
        "precautions": [
            "Do not over-irrigate during flowering to prevent root lodging and rust susceptibility.",
            "Ensure balanced fertilization with adequate phosphorus and potassium.",
            "Monitor soil moisture at crown root initiation and flowering stages."
        ]
    },
    "Maize": {
        "category": "Cereal / Fodder",
        "temp_optimal": (20.0, 30.0),
        "humidity_optimal": (55.0, 75.0),
        "rainfall_optimal": (60.0, 120.0),
        "ph_optimal": (5.8, 7.2),
        "water_requirement": "Moderate",
        "soil_type": "Deep, well-drained fertile loam",
        "growing_season": "Kharif / Spring",
        "emoji": "🌽",
        "diseases": [
            {
                "name": "Northern Leaf Blight",
                "risk_trigger": "Moderate temp (18-27C) with prolonged wet leaves (>85% RH)",
                "symptoms": "Long, elliptical grayish-green or tan lesions on leaves.",
                "causes": "Fungal spores overwintering in debris, splashed by wind and rain.",
                "precautions": "Use resistant hybrids, practice residue management, apply foliar fungicides."
            },
            {
                "name": "Common Rust",
                "risk_trigger": "Cool to moderate temperatures (16-25C) and high humidity",
                "symptoms": "Cinnamon-brown powdery pustules scattered on upper and lower leaf surfaces.",
                "causes": "Airborne spores carried from southern or warmer regions during wet periods.",
                "precautions": "Plant resistant varieties, scout early vegetative whorls."
            }
        ],
        "precautions": [
            "Ensure proper drainage; maize roots cannot tolerate waterlogging beyond 24-48 hours.",
            "Apply top-dressed nitrogen in split doses at knee-high and tasseling stages.",
            "Mulch between rows to preserve moisture during dry spells."
        ]
    },
    "Jute": {
        "category": "Fiber Crop",
        "temp_optimal": (24.0, 35.0),
        "humidity_optimal": (70.0, 90.0),
        "rainfall_optimal": (120.0, 250.0),
        "ph_optimal": (6.0, 7.5),
        "water_requirement": "High",
        "soil_type": "Alluvial, rich sandy loam",
        "growing_season": "Kharif",
        "emoji": "🌿",
        "diseases": [
            {
                "name": "Stem Rot (Macrophomina phaseolina)",
                "risk_trigger": "Warm (28-34C) and humid wet soil conditions",
                "symptoms": "Brown lesions on stem base, wilting and fiber disintegration.",
                "causes": "Soil-borne pathogen activated by water stagnation and excessive heat.",
                "precautions": "Crop rotation with rice/wheat, seed treatment with Trichoderma, ensure drainage."
            }
        ],
        "precautions": [
            "Maintain timely weeding and thinning at 20-25 days after sowing.",
            "Ensure drainage during heavy monsoon deluges to avoid stem rot."
        ]
    },

    # --- VEGETABLES & TUBERS ---
    "Tomato": {
        "category": "Vegetable / Solanaceous",
        "temp_optimal": (18.0, 28.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (40.0, 90.0),
        "ph_optimal": (6.0, 7.0),
        "water_requirement": "Moderate",
        "soil_type": "Well-drained sandy loam rich in organic matter",
        "growing_season": "Year-round / Rabi / Kharif",
        "emoji": "🍅",
        "diseases": [
            {
                "name": "Early Blight (Alternaria solani)",
                "risk_trigger": "Warm temperatures (24-29C) and alternating wet/dry conditions",
                "symptoms": "Concentric rings ('target board' pattern) on older lower leaves.",
                "causes": "Foliar wetness from dew or rain followed by warm sunshine.",
                "precautions": "Stake plants, mulch to prevent soil splashing, remove lower diseased leaves."
            },
            {
                "name": "Late Blight (Phytophthora infestans)",
                "risk_trigger": "Cool, cloudy weather (15-22C) with high relative humidity (>85%)",
                "symptoms": "Water-soaked irregular lesions with white mold on leaf undersides.",
                "causes": "Continuous leaf wetness and cool humid microclimates.",
                "precautions": "Apply preventive copper/mancozeb sprays before continuous rain spells; avoid overhead watering."
            },
            {
                "name": "Bacterial Spot (Xanthomonas)",
                "risk_trigger": "High humidity and temperatures around 24-30C",
                "symptoms": "Small, dark, water-soaked circular spots with yellow halos.",
                "causes": "Bacterial pathogen spread by wind-driven rain and infected seeds.",
                "precautions": "Use certified seed, apply copper-bactericide sprays, avoid sprinkler irrigation."
            }
        ],
        "precautions": [
            "Use drip irrigation to keep foliage dry and minimize fungal spore germination.",
            "Stake and prune indeterminate varieties to optimize airflow and sunlight penetration.",
            "Ensure calcium availability to avoid blossom end rot under variable moisture conditions."
        ]
    },
    "Potato": {
        "category": "Tuber / Solanaceous",
        "temp_optimal": (16.0, 24.0),
        "humidity_optimal": (60.0, 80.0),
        "rainfall_optimal": (50.0, 100.0),
        "ph_optimal": (5.0, 6.5),
        "water_requirement": "Moderate",
        "soil_type": "Loose, friable sandy loam",
        "growing_season": "Rabi (Winter)",
        "emoji": "🥔",
        "diseases": [
            {
                "name": "Potato Late Blight",
                "risk_trigger": "Temp 10-21C with RH >90% for 2+ consecutive days",
                "symptoms": "Rapid blighting of leaves and stems with purplish-brown decay.",
                "causes": "Cool, foggy weather and persistent wet canopy conditions.",
                "precautions": "Earthing up to shield tubers; timely preventive protective sprays."
            },
            {
                "name": "Early Blight",
                "risk_trigger": "Warm (22-30C) and humid weather with dew",
                "symptoms": "Dark brown circular spots with concentric target-rings.",
                "causes": "Pathogen overwintering in debris; plant stress accelerates onset.",
                "precautions": "Maintain adequate vine nutrition, rotate crops away from solanaceous species."
            }
        ],
        "precautions": [
            "Perform proper earthing up to prevent tuber greening and late blight spore wash-down.",
            "Avoid water stagnation which rapidly induces bacterial soft rot in tubers.",
            "Stop irrigation 10-14 days prior to harvesting to promote tuber skin curing."
        ]
    },
    "Pepper": {
        "category": "Vegetable / Solanaceous",
        "temp_optimal": (20.0, 30.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (40.0, 80.0),
        "ph_optimal": (6.0, 6.8),
        "water_requirement": "Moderate",
        "soil_type": "Well-drained loam or sandy loam",
        "growing_season": "Summer / Kharif / Rabi",
        "emoji": "🫑",
        "diseases": [
            {
                "name": "Bacterial Spot (Xanthomonas)",
                "risk_trigger": "Warm temperatures (24-30C) accompanied by frequent rains or heavy dew",
                "symptoms": "Small yellowish-green spots turning brown and necrotic with yellow halos.",
                "causes": "Splattering water droplets carrying bacterial inoculum to stomata.",
                "precautions": "Avoid overhead watering; spray preventive fixed copper formulations."
            }
        ],
        "precautions": [
            "Avoid waterlogging as capsicums are prone to Phytophthora root rot.",
            "Maintain moderate soil moisture during flowering to prevent flower drop."
        ]
    },

    # --- FRUITS & ORCHARDS ---
    "Apple": {
        "category": "Temperate Fruit",
        "temp_optimal": (12.0, 24.0),
        "humidity_optimal": (55.0, 75.0),
        "rainfall_optimal": (70.0, 130.0),
        "ph_optimal": (6.0, 7.0),
        "water_requirement": "Moderate",
        "soil_type": "Well-drained loamy, rich in organic humus",
        "growing_season": "Perennial (Spring-Autumn)",
        "emoji": "🍎",
        "diseases": [
            {
                "name": "Apple Scab (Venturia inaequalis)",
                "risk_trigger": "Cool (15-22C) and prolonged leaf wetness (>9 hours)",
                "symptoms": "Olive-green to velvety dark brown lesions on leaves and fruit skin.",
                "causes": "Airborne ascospores released during spring rainfall events.",
                "precautions": "Rake and destroy fallen leaves; apply protective fungicidal sprays at green tip stage."
            },
            {
                "name": "Black Rot (Botryosphaeria obtusa)",
                "risk_trigger": "Warm (20-28C) rainy periods",
                "symptoms": "Frog-eye spots on leaves, mummified black fruit rots.",
                "causes": "Fungal infection entering via wounds, dead twigs, or insect stings.",
                "precautions": "Prune dead wood during winter dormancy; sanitize cankered limbs."
            },
            {
                "name": "Cedar Apple Rust",
                "risk_trigger": "Wet spring weather near eastern red cedar hosts",
                "symptoms": "Bright orange-yellow spots on upper leaf surfaces.",
                "causes": "Gymnosporangium rust fungus requiring alternating juniper/cedar hosts.",
                "precautions": "Remove nearby wild cedar trees; apply myclobutanil fungicides before petal fall."
            }
        ],
        "precautions": [
            "Ensure regular canopy pruning for sunlight penetration and rapid drying after rain.",
            "Thin fruit load in early summer to maintain tree vigor and prevent biennial bearing."
        ]
    },
    "Cherry": {
        "category": "Stone Fruit",
        "temp_optimal": (14.0, 24.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (60.0, 100.0),
        "ph_optimal": (6.0, 7.2),
        "water_requirement": "Moderate",
        "soil_type": "Deep well-drained gravelly or sandy loam",
        "growing_season": "Perennial (Spring-Early Summer)",
        "emoji": "🍒",
        "diseases": [
            {
                "name": "Powdery Mildew (Podosphaera)",
                "risk_trigger": "Warm days (20-28C) and cool humid nights",
                "symptoms": "White powdery fungal coating on young shoots, leaves, and fruit.",
                "causes": "Fungal mycelium thriving in shaded canopies and fluctuating humidity.",
                "precautions": "Prune for air circulation; apply sulfur or potassium bicarbonate sprays."
            }
        ],
        "precautions": [
            "Avoid excessive summer irrigation to prevent sweet cherry skin cracking.",
            "Apply winter dormant oil sprays to manage scale and overwintering spores."
        ]
    },
    "Peach": {
        "category": "Stone Fruit",
        "temp_optimal": (18.0, 28.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (60.0, 110.0),
        "ph_optimal": (6.0, 7.0),
        "water_requirement": "Moderate",
        "soil_type": "Deep, well-drained sandy loam",
        "growing_season": "Perennial (Spring-Summer)",
        "emoji": "🍑",
        "diseases": [
            {
                "name": "Bacterial Spot (Xanthomonas arboricola)",
                "risk_trigger": "Frequent spring showers and wind (temp 20-30C)",
                "symptoms": "Water-soaked polygonal spots on leaves, shotgun hole shedding, cracked fruit.",
                "causes": "Windblown rain dispersing overwintering bacteria from twigs.",
                "precautions": "Plant windbreaks, apply copper during dormant and bud-swell stages."
            }
        ],
        "precautions": [
            "Ensure open-center (vase) pruning to maximize interior air flow.",
            "Avoid wetting tree canopies with overhead sprinklers."
        ]
    },
    "Grapes": {
        "category": "Vine Fruit",
        "temp_optimal": (20.0, 32.0),
        "humidity_optimal": (45.0, 65.0),
        "rainfall_optimal": (50.0, 90.0),
        "ph_optimal": (6.0, 7.5),
        "water_requirement": "Moderate-Low",
        "soil_type": "Gravelly or sandy loam with good drainage",
        "growing_season": "Perennial",
        "emoji": "🍇",
        "diseases": [
            {
                "name": "Black Rot (Guignardia bidwellii)",
                "risk_trigger": "Warm (22-29C) and humid weather with rainfall",
                "symptoms": "Small circular reddish-brown leaf spots; shriveled, mummified black berries.",
                "causes": "Rain splash spreading spores from mummified berries left on vines.",
                "precautions": "Remove old mummies during winter pruning; spray mancozeb/triazoles early."
            },
            {
                "name": "Esca (Black Measles)",
                "risk_trigger": "Thermal stress in mature vineyards",
                "symptoms": "Tiger-stripe leaf chlorosis and dark spotting on berries.",
                "causes": "Fungal complex infecting pruning wounds in woody trunks.",
                "precautions": "Sanitize pruning shears, treat trunk wounds with protective paste."
            },
            {
                "name": "Leaf Blight (Isariopsis clavispora)",
                "risk_trigger": "High humidity and continuous canopy shade",
                "symptoms": "Irregular dark brown patches on mature foliage.",
                "causes": "Dense unpruned canopy and stagnant air.",
                "precautions": "Leaf-pulling around grape clusters to enhance air circulation."
            }
        ],
        "precautions": [
            "Maintain trellis canopy management for optimal airflow.",
            "Regulate deficit irrigation during veraison to enhance sugar accumulation."
        ]
    },
    "Strawberry": {
        "category": "Berry Fruit",
        "temp_optimal": (16.0, 26.0),
        "humidity_optimal": (55.0, 75.0),
        "rainfall_optimal": (45.0, 85.0),
        "ph_optimal": (5.5, 6.5),
        "water_requirement": "Moderate",
        "soil_type": "Rich, well-drained sandy loam with high organic compost",
        "growing_season": "Winter / Spring",
        "emoji": "🍓",
        "diseases": [
            {
                "name": "Leaf Scorch (Diplocarpon earlianum)",
                "risk_trigger": "Frequent rain and temperatures between 18-25C",
                "symptoms": "Small purplish spots on upper leaf surfaces that coalesce and dry.",
                "causes": "Fungal spores splashed by rain or overhead watering.",
                "precautions": "Mulch with clean straw or plastic; use drip lines; destroy old diseased leaves."
            }
        ],
        "precautions": [
            "Use plastic mulching to elevate berries above moist soil.",
            "Maintain adequate spacing to facilitate morning leaf drying."
        ]
    },
    "Banana": {
        "category": "Tropical Fruit",
        "temp_optimal": (24.0, 34.0),
        "humidity_optimal": (70.0, 90.0),
        "rainfall_optimal": (100.0, 200.0),
        "ph_optimal": (5.5, 7.0),
        "water_requirement": "Very High",
        "soil_type": "Deep rich alluvial or volcanic loam",
        "growing_season": "Perennial (11-14 months)",
        "emoji": "🍌",
        "diseases": [
            {
                "name": "Sigatoka Leaf Spot",
                "risk_trigger": "Warm temp (>25C) with high humidity (>80%) and rain",
                "symptoms": "Yellow streaks turning into dark brown spindle lesions with gray centers.",
                "causes": "Wind-borne ascospores in tropical humid conditions.",
                "precautions": "Deleaf heavily infected leaves; apply protective mineral oil and triazoles."
            }
        ],
        "precautions": [
            "Provide strong staking or propping for heavy fruiting bunches.",
            "Maintain generous mulch cover to shield shallow feeder roots from sun bake."
        ]
    },
    "Mango": {
        "category": "Tropical Fruit",
        "temp_optimal": (24.0, 35.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (50.0, 100.0),
        "ph_optimal": (5.5, 7.5),
        "water_requirement": "Moderate",
        "soil_type": "Deep well-drained alluvial or red loamy soil",
        "growing_season": "Perennial",
        "emoji": "🥭",
        "diseases": [
            {
                "name": "Anthracnose (Colletotrichum gloeosporioides)",
                "risk_trigger": "Unseasonal rains or heavy morning fogs during panicle bloom",
                "symptoms": "Black sunken spots on blossoms, young foliage, and maturing fruits.",
                "causes": "Conidia washing down from branch canopies during rain events.",
                "precautions": "Spray copper/carbendazim before flowering; prune overlapping interior branches."
            }
        ],
        "precautions": [
            "Withhold irrigation 2 months prior to flowering to induce flower bud differentiation.",
            "Scout for mango hopper insects during panicle emergence."
        ]
    },
    "Orange": {
        "category": "Citrus Fruit",
        "temp_optimal": (18.0, 32.0),
        "humidity_optimal": (55.0, 75.0),
        "rainfall_optimal": (60.0, 120.0),
        "ph_optimal": (5.5, 7.0),
        "water_requirement": "Moderate",
        "soil_type": "Well-drained light loamy soil",
        "growing_season": "Perennial",
        "emoji": "🍊",
        "diseases": [
            {
                "name": "Citrus Canker",
                "risk_trigger": "Warm weather (25-35C) with driving rain",
                "symptoms": "Raised corky lesions on leaves and fruit with yellow halos.",
                "causes": "Bacterium entering stomata and leafminer insect wounds.",
                "precautions": "Apply protective copper sprays; control leafminers; sanitize tools."
            }
        ],
        "precautions": [
            "Ensure excellent subsoil drainage; citrus roots are highly vulnerable to gummosis.",
            "Apply micronutrient zinc and iron sprays during spring flush."
        ]
    },
    "Papaya": {
        "category": "Tropical Fruit",
        "temp_optimal": (22.0, 34.0),
        "humidity_optimal": (60.0, 80.0),
        "rainfall_optimal": (80.0, 160.0),
        "ph_optimal": (6.0, 7.0),
        "water_requirement": "Moderate-High",
        "soil_type": "Rich, well-drained sandy loam with good depth",
        "growing_season": "Annual/Perennial (9-12 months)",
        "emoji": "🍈",
        "diseases": [
            {
                "name": "Papaya Ringspot Virus",
                "risk_trigger": "Warm dry periods accelerating aphid vector movement",
                "symptoms": "Yellow mosaic mottling, shoe-string leaves, concentric rings on fruit.",
                "causes": "Transmitted by aphids from infected cucurbit/papaya weed hosts.",
                "precautions": "Eradicate infected trees immediately; control aphid populations with neem sprays."
            }
        ],
        "precautions": [
            "Plant on raised mounds; papaya is exceptionally intolerant of even 24 hours of flooding.",
            "Avoid planting adjacent to cucurbitaceous crops."
        ]
    },
    "Pomegranate": {
        "category": "Subtropical Fruit",
        "temp_optimal": (20.0, 36.0),
        "humidity_optimal": (40.0, 60.0),
        "rainfall_optimal": (40.0, 80.0),
        "ph_optimal": (6.5, 7.8),
        "water_requirement": "Low-Moderate",
        "soil_type": "Deep loamy or slightly calcareous soil",
        "growing_season": "Perennial",
        "emoji": "🍎",
        "diseases": [
            {
                "name": "Bacterial Blight / Oily Spot (Xanthomonas)",
                "risk_trigger": "Cloudy humid weather (>75% RH) and temperatures between 25-35C",
                "symptoms": "Dark brown water-soaked angular spots on leaves; L-shaped cracked rind lesions.",
                "causes": "Wind-driven rain, contaminated secateurs, and high humidity.",
                "precautions": "Strict orchard sanitation; spray streptocycline + copper oxychloride."
            }
        ],
        "precautions": [
            "Maintain consistent drip irrigation to avoid fruit cracking during dry-to-wet transitions.",
            "Bag fruits on tree to guard against pomegranate fruit borer."
        ]
    },
    "Watermelon": {
        "category": "Cucurbit Fruit",
        "temp_optimal": (24.0, 35.0),
        "humidity_optimal": (45.0, 65.0),
        "rainfall_optimal": (40.0, 70.0),
        "ph_optimal": (6.0, 7.0),
        "water_requirement": "Moderate",
        "soil_type": "Warm, well-drained sandy loam rich in organic matter",
        "growing_season": "Zaid (Summer)",
        "emoji": "🍉",
        "diseases": [
            {
                "name": "Fusarium Wilt",
                "risk_trigger": "Warm soils (>27C) with periodic moisture stress",
                "symptoms": "Unilateral vine wilting, vascular browning in stem base.",
                "causes": "Soil-borne pathogen penetrating root tips.",
                "precautions": "Rotate with non-cucurbit crops for 4+ years; plant grafted rootstocks."
            }
        ],
        "precautions": [
            "Stop irrigation 7-10 days before harvest to maximize sugar brix content.",
            "Use plastic mulching to accelerate spring root development."
        ]
    },
    "Muskmelon": {
        "category": "Cucurbit Fruit",
        "temp_optimal": (24.0, 35.0),
        "humidity_optimal": (45.0, 65.0),
        "rainfall_optimal": (40.0, 60.0),
        "ph_optimal": (6.0, 7.2),
        "water_requirement": "Moderate",
        "soil_type": "Sandy loam, alluvial riverbeds",
        "growing_season": "Zaid (Summer)",
        "emoji": "🍈",
        "diseases": [
            {
                "name": "Downy Mildew",
                "risk_trigger": "High humidity, night dew, and warm day temps",
                "symptoms": "Angular yellow patches on upper leaf surface, purplish mold beneath.",
                "causes": "Airborne sporangia germinating in free moisture on leaves.",
                "precautions": "Drip irrigate early morning; spray cymoxanil/mancozeb at first sign."
            }
        ],
        "precautions": [
            "Provide dry soil bed underneath developing melons to prevent ground rot.",
            "Ensure full sun exposure for high sweetness."
        ]
    },
    "Coconut": {
        "category": "Plantation / Palm",
        "temp_optimal": (25.0, 35.0),
        "humidity_optimal": (65.0, 85.0),
        "rainfall_optimal": (100.0, 220.0),
        "ph_optimal": (5.2, 8.0),
        "water_requirement": "High",
        "soil_type": "Coastal sandy loam, alluvial, red loam",
        "growing_season": "Perennial (Continuous)",
        "emoji": "🥥",
        "diseases": [
            {
                "name": "Bud Rot (Phytophthora palmivora)",
                "risk_trigger": "Heavy continuous monsoon rains and high humidity",
                "symptoms": "Withering of central spear leaf, foul-smelling soft rot of terminal bud.",
                "causes": "Fungal spores washing into crown during torrential monsoons.",
                "precautions": "Clean crown debris; place fungicide sachets/bordeaux paste at heart."
            }
        ],
        "precautions": [
            "Apply potassium and magnesium chloride regularly in coastal and inland basins.",
            "Ensure basin mulching with coconut fronds during dry summer months."
        ]
    },
    "Coffee": {
        "category": "Plantation / Beverage",
        "temp_optimal": (18.0, 28.0),
        "humidity_optimal": (65.0, 85.0),
        "rainfall_optimal": (120.0, 220.0),
        "ph_optimal": (5.5, 6.5),
        "water_requirement": "Moderate-High",
        "soil_type": "Deep, fertile volcanic or forest loam rich in organic matter",
        "growing_season": "Perennial",
        "emoji": "☕",
        "diseases": [
            {
                "name": "Coffee Leaf Rust (Hemileia vastatrix)",
                "risk_trigger": "Wet leaves, rain splashes, and temperatures between 21-25C",
                "symptoms": "Orange-yellow powdery spots on leaf undersides causing heavy defoliation.",
                "causes": "Wind and rain-borne urediniospores in shaded microclimates.",
                "precautions": "Manage shade canopy density; apply protective copper spray before monsoon."
            }
        ],
        "precautions": [
            "Maintain two-tier shade trees to regulate temperature fluctuations.",
            "Scout for coffee berry borer during fruit maturation."
        ]
    },

    # --- PULSES & LEGUMES ---
    "Chickpea": {
        "category": "Pulse / Legume",
        "temp_optimal": (15.0, 25.0),
        "humidity_optimal": (40.0, 60.0),
        "rainfall_optimal": (30.0, 70.0),
        "ph_optimal": (6.0, 8.0),
        "water_requirement": "Low-Moderate",
        "soil_type": "Well-drained black cotton or sandy loam",
        "growing_season": "Rabi (Post-Monsoon/Winter)",
        "emoji": "🥜",
        "diseases": [
            {
                "name": "Ascochyta Blight",
                "risk_trigger": "Overcast cool weather (15-20C) with high humidity (>75%)",
                "symptoms": "Circular spots with concentric dark pycnidia rings on leaves and pods.",
                "causes": "Prolonged rainfall, heavy fog, and cool temperatures.",
                "precautions": "Select tolerant varieties; apply seed treatment; avoid dense canopies."
            },
            {
                "name": "Fusarium Wilt",
                "risk_trigger": "High soil temperatures (>25C) and moisture stress",
                "symptoms": "Drooping petioles, internal vascular browning, sudden drying.",
                "causes": "Soil-borne pathogen activated by root stress and warm soils.",
                "precautions": "Practice 3-year crop rotation; avoid sowing in excessively warm early October soil."
            }
        ],
        "precautions": [
            "Extremely sensitive to waterlogging; never allow water to stand in the field.",
            "Avoid excess irrigation which causes vegetative overgrowth at the expense of pod setting.",
            "Monitor pod borer (Helicoverpa armigera) at flowering and early pod stage."
        ]
    },
    "Kidneybeans": {
        "category": "Pulse / Legume",
        "temp_optimal": (15.0, 25.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (60.0, 110.0),
        "ph_optimal": (5.5, 6.5),
        "water_requirement": "Moderate",
        "soil_type": "Deep, fertile loam with high organic matter",
        "growing_season": "Rabi / Kharif (Hills)",
        "emoji": "🫘",
        "diseases": [
            {
                "name": "Anthracnose (Colletotrichum lindemuthianum)",
                "risk_trigger": "Cool to moderate temperatures (17-24C) with frequent rainfall",
                "symptoms": "Brick-red to black sunken lesions on leaf veins and pods.",
                "causes": "Seed-borne fungal pathogen spread by driving rain.",
                "precautions": "Use certified pathogen-free seed; avoid cultivating wet fields."
            }
        ],
        "precautions": [
            "Ensure adequate nitrogen fixation or supply basal starter nitrogen.",
            "Maintain moderate moisture during pod elongation."
        ]
    },
    "Pigeonpeas": {
        "category": "Pulse / Legume",
        "temp_optimal": (20.0, 32.0),
        "humidity_optimal": (45.0, 70.0),
        "rainfall_optimal": (60.0, 110.0),
        "ph_optimal": (6.5, 7.8),
        "water_requirement": "Low-Moderate",
        "soil_type": "Deep well-drained loam or vertisol",
        "growing_season": "Kharif (Long duration)",
        "emoji": "🌱",
        "diseases": [
            {
                "name": "Sterility Mosaic Disease (SMD)",
                "risk_trigger": "Dry spells promoting eriophyid mite vectors",
                "symptoms": "Bushy appearance, leaf mottling, complete lack of flowers/pods.",
                "causes": "Transmitted by Aceria cajani mites.",
                "precautions": "Plant resistant cultivars (Asha); apply acaricides early if mite populations rise."
            }
        ],
        "precautions": [
            "Deep root system tolerates drought; ensure drainage during monsoon peaks.",
            "Intercrop with sorghum or pearl millet for pest management."
        ]
    },
    "Mothbeans": {
        "category": "Arid Pulse",
        "temp_optimal": (25.0, 38.0),
        "humidity_optimal": (35.0, 55.0),
        "rainfall_optimal": (20.0, 60.0),
        "ph_optimal": (6.5, 8.0),
        "water_requirement": "Very Low",
        "soil_type": "Sandy loam, arid desert soils",
        "growing_season": "Kharif",
        "emoji": "🫘",
        "diseases": [
            {
                "name": "Yellow Mosaic Virus",
                "risk_trigger": "Warm dry periods with whitefly vector activity",
                "symptoms": "Bright yellow patches on foliage, reduced pod development.",
                "causes": "Geminivirus spread by Bemisia tabaci whiteflies.",
                "precautions": "Control whiteflies with sticky traps and bio-insecticides."
            }
        ],
        "precautions": [
            "Highly drought-tolerant; avoid any water stagnation.",
            "Excellent soil cover crop to prevent wind erosion."
        ]
    },
    "Mungbean": {
        "category": "Short Pulse",
        "temp_optimal": (24.0, 35.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (40.0, 80.0),
        "ph_optimal": (6.2, 7.5),
        "water_requirement": "Low-Moderate",
        "soil_type": "Well-drained loam or alluvial",
        "growing_season": "Kharif / Summer",
        "emoji": "🌱",
        "diseases": [
            {
                "name": "Powdery Mildew (Erysiphe polygoni)",
                "risk_trigger": "Cool mornings, warm dry days, and high humidity",
                "symptoms": "White flour-like patches spreading over leaves, stems, and pods.",
                "causes": "Airborne conidia thriving in dense canopies.",
                "precautions": "Spray wettable sulfur; harvest synchronously."
            }
        ],
        "precautions": [
            "Fast 60-70 day crop; provide light irrigation at flowering and pod filling.",
            "Maintain timely harvest to prevent pod shattering."
        ]
    },
    "Blackgram": {
        "category": "Pulse / Legume",
        "temp_optimal": (24.0, 35.0),
        "humidity_optimal": (50.0, 75.0),
        "rainfall_optimal": (50.0, 90.0),
        "ph_optimal": (6.5, 7.5),
        "water_requirement": "Moderate",
        "soil_type": "Deep black soils, loamy soils",
        "growing_season": "Kharif / Rabi",
        "emoji": "🫘",
        "diseases": [
            {
                "name": "Cercospora Leaf Spot",
                "risk_trigger": "Warm humid conditions (25-30C) with rain showers",
                "symptoms": "Circular spots with brown centers and reddish borders.",
                "causes": "Fungal spores spread by rain splashes and wind.",
                "precautions": "Spray carbendazim/mancozeb; rotate crops."
            }
        ],
        "precautions": [
            "Ensure inoculation with Rhizobium culture prior to sowing.",
            "Avoid severe water stress during flowering."
        ]
    },
    "Lentil": {
        "category": "Cool Season Pulse",
        "temp_optimal": (15.0, 25.0),
        "humidity_optimal": (45.0, 65.0),
        "rainfall_optimal": (30.0, 70.0),
        "ph_optimal": (6.0, 7.5),
        "water_requirement": "Low",
        "soil_type": "Light loamy to alluvial clay",
        "growing_season": "Rabi (Winter)",
        "emoji": "🥣",
        "diseases": [
            {
                "name": "Lentil Rust (Uromyces viciae-fabae)",
                "risk_trigger": "High humidity (>80%) and temperatures around 18-22C",
                "symptoms": "Small brown pustules on leaf undersides, premature leaf drop.",
                "causes": "Airborne urediniospores during moist cloudy periods.",
                "precautions": "Early sowing to escape peak rust; spray propiconazole if detected."
            }
        ],
        "precautions": [
            "Plant as relay crop after rice harvest in residual moisture.",
            "Guard against waterlogging."
        ]
    },

    # --- COMMERCIAL & FIBER ---
    "Cotton": {
        "category": "Fiber / Cash",
        "temp_optimal": (21.0, 32.0),
        "humidity_optimal": (50.0, 70.0),
        "rainfall_optimal": (50.0, 110.0),
        "ph_optimal": (6.0, 8.0),
        "water_requirement": "Moderate",
        "soil_type": "Deep black soil (Regur), alluvial",
        "growing_season": "Kharif",
        "emoji": "🌱",
        "diseases": [
            {
                "name": "Bacterial Blight / Angular Leaf Spot",
                "risk_trigger": "High humidity (>80%) and temperature (28-34C)",
                "symptoms": "Angular water-soaked spots bounded by leaf veinlets.",
                "causes": "Wind-driven rain, high humidity, and warm weather.",
                "precautions": "Seed treatment with bactericide; avoid overhead sprinkler irrigation."
            },
            {
                "name": "Boll Rot Complex",
                "risk_trigger": "Prolonged rainfall, overcast weather, and relative humidity >85%",
                "symptoms": "Discolored, softening bolls failing to open properly.",
                "causes": "Secondary fungal entry following insect punctures in wet weather.",
                "precautions": "Prune lower leaves if foliage is extremely dense; improve field aeration."
            }
        ],
        "precautions": [
            "Avoid standing water; cotton is sensitive to root asphyxiation in waterlogged soils.",
            "Monitor whitefly and bollworm populations during square formation.",
            "Apply micronutrients (boron and zinc) during flowering and boll retention."
        ]
    },
    "Sugarcane": {
        "category": "Cash / Commercial",
        "temp_optimal": (24.0, 35.0),
        "humidity_optimal": (65.0, 85.0),
        "rainfall_optimal": (100.0, 200.0),
        "ph_optimal": (6.0, 7.8),
        "water_requirement": "Very High",
        "soil_type": "Deep rich loamy soil",
        "growing_season": "Annual (10-14 months)",
        "emoji": "🎋",
        "diseases": [
            {
                "name": "Red Rot (Colletotrichum falcatum)",
                "risk_trigger": "High humidity (>85%), waterlogging, and temp 25-32C",
                "symptoms": "Discoloration of crown leaves, internal red discoloration with white patches across stalks.",
                "causes": "Waterlogging, infected seed setts, and stagnant humid fields.",
                "precautions": "Use certified disease-free setts, ensure field drainage, avoid ratoon cropping infected fields."
            }
        ],
        "precautions": [
            "Provide trash mulching to conserve moisture in early formative stages.",
            "Ensure drainage channels are clear before peak monsoon to avert red rot escalation.",
            "Perform propping or earthing up to prevent crop lodging during high wind events."
        ]
    }
}

def calculate_agronomic_health(crop_name, temp, humidity, rainfall, wind_speed=12.0):
    """
    Computes an objective, scientifically bounded Crop Health Score (0-100)
    and risk category based on agronomic bounds.
    """
    profile = CROP_PROFILES.get(crop_name, CROP_PROFILES.get("Wheat"))
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
    print(f"[DatasetBuilder] Generated {kb_file} with {len(CROP_PROFILES)} crop profiles.")

    # 2. Generate comprehensive calibrated dataset (300 samples per crop across all 28 crops = 8,400 samples)
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
            regime = np.random.choice(["optimal", "moderate_stress", "high_stress"], p=[0.45, 0.35, 0.20])

            if regime == "optimal":
                temp = np.random.uniform(t_min, t_max)
                humidity = np.random.uniform(h_min, h_max)
                rainfall = np.random.uniform(r_min, r_max)
                wind = np.random.uniform(5.0, 20.0)
            elif regime == "moderate_stress":
                delta_t = np.random.choice([-1, 1]) * np.random.uniform(3.0, 8.0)
                temp = np.clip(np.random.uniform(t_min, t_max) + delta_t, 5.0, 48.0)
                delta_h = np.random.choice([-1, 1]) * np.random.uniform(10.0, 25.0)
                humidity = np.clip(np.random.uniform(h_min, h_max) + delta_h, 15.0, 98.0)
                delta_r = np.random.choice([-1, 1]) * np.random.uniform(0.3, 0.7) * r_min
                rainfall = max(0.0, np.random.uniform(r_min, r_max) + delta_r)
                wind = np.random.uniform(10.0, 32.0)
            else:
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
    raw_path = "Data/raw/crop_weather_raw.csv"
    processed_path = "Data/processed/crop_weather_data.csv"
    df.to_csv(raw_path, index=False)
    df.to_csv(processed_path, index=False)
    print(f"[DatasetBuilder] Saved {raw_path} and {processed_path} with {len(df)} records across {len(crops)} crops.")

if __name__ == "__main__":
    generate_datasets()
