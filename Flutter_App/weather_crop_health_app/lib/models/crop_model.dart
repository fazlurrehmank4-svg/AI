class CropModel {
  final String name;
  final String category;
  final String growingSeason;
  final double tempMin;
  final double tempMax;
  final double humidityMin;
  final double humidityMax;
  final double rainfallMin;
  final double rainfallMax;
  final String soilType;
  final String waterRequirement;
  final String emoji;

  const CropModel({
    required this.name,
    required this.category,
    required this.growingSeason,
    required this.tempMin,
    required this.tempMax,
    required this.humidityMin,
    required this.humidityMax,
    required this.rainfallMin,
    required this.rainfallMax,
    required this.soilType,
    required this.waterRequirement,
    required this.emoji,
  });

  static const List<CropModel> supportedCrops = [
    CropModel(
      name: "Wheat",
      category: "Cereal Grain",
      growingSeason: "Rabi (Winter)",
      tempMin: 15.0,
      tempMax: 25.0,
      humidityMin: 50.0,
      humidityMax: 70.0,
      rainfallMin: 50.0,
      rainfallMax: 100.0,
      soilType: "Well-drained loam",
      waterRequirement: "Moderate",
      emoji: "🌾",
    ),
    CropModel(
      name: "Rice",
      category: "Cereal Grain",
      growingSeason: "Kharif (Monsoon)",
      tempMin: 22.0,
      tempMax: 32.0,
      humidityMin: 70.0,
      humidityMax: 85.0,
      rainfallMin: 150.0,
      rainfallMax: 300.0,
      soilType: "Clayey alluvial",
      waterRequirement: "High",
      emoji: "🍚",
    ),
    CropModel(
      name: "Tomato",
      category: "Vegetable / Cash",
      growingSeason: "Year-round",
      tempMin: 18.0,
      tempMax: 28.0,
      humidityMin: 50.0,
      humidityMax: 70.0,
      rainfallMin: 40.0,
      rainfallMax: 90.0,
      soilType: "Sandy loam",
      waterRequirement: "Moderate",
      emoji: "🍅",
    ),
    CropModel(
      name: "Maize",
      category: "Cereal / Fodder",
      growingSeason: "Kharif / Spring",
      tempMin: 20.0,
      tempMax: 30.0,
      humidityMin: 55.0,
      humidityMax: 75.0,
      rainfallMin: 60.0,
      rainfallMax: 120.0,
      soilType: "Fertile loam",
      waterRequirement: "Moderate",
      emoji: "🌽",
    ),
    CropModel(
      name: "Cotton",
      category: "Fiber / Cash",
      growingSeason: "Kharif",
      tempMin: 21.0,
      tempMax: 32.0,
      humidityMin: 50.0,
      humidityMax: 70.0,
      rainfallMin: 50.0,
      rainfallMax: 110.0,
      soilType: "Deep black soil",
      waterRequirement: "Moderate",
      emoji: "🌱",
    ),
    CropModel(
      name: "Potato",
      category: "Tuber / Vegetable",
      growingSeason: "Rabi",
      tempMin: 16.0,
      tempMax: 24.0,
      humidityMin: 60.0,
      humidityMax: 80.0,
      rainfallMin: 50.0,
      rainfallMax: 100.0,
      soilType: "Loose friable loam",
      waterRequirement: "Moderate",
      emoji: "🥔",
    ),
    CropModel(
      name: "Sugarcane",
      category: "Cash / Commercial",
      growingSeason: "Annual",
      tempMin: 24.0,
      tempMax: 35.0,
      humidityMin: 65.0,
      humidityMax: 85.0,
      rainfallMin: 100.0,
      rainfallMax: 200.0,
      soilType: "Rich heavy loam",
      waterRequirement: "Very High",
      emoji: "🎋",
    ),
    CropModel(
      name: "Chickpea",
      category: "Pulse / Legume",
      growingSeason: "Rabi",
      tempMin: 15.0,
      tempMax: 25.0,
      humidityMin: 40.0,
      humidityMax: 60.0,
      rainfallMin: 30.0,
      rainfallMax: 70.0,
      soilType: "Black or sandy loam",
      waterRequirement: "Low-Moderate",
      emoji: "🥜",
    ),
  ];
}
