import 'weather_model.dart';

class PredictionModel {
  final String crop;
  final String location;
  final WeatherModel weather;
  final double cropHealthScore;
  final String healthStatus;
  final String riskLevel;
  final String primaryRiskFactor;
  final String agroClimaticRegime;
  final List<String> causes;
  final List<String> precautions;
  final String aiExplanation;
  final DateTime timestamp;

  PredictionModel({
    required this.crop,
    required this.location,
    required this.weather,
    required this.cropHealthScore,
    required this.healthStatus,
    required this.riskLevel,
    required this.primaryRiskFactor,
    required this.agroClimaticRegime,
    required this.causes,
    required this.precautions,
    required this.aiExplanation,
    required this.timestamp,
  });

  factory PredictionModel.fromJson(Map<String, dynamic> json) {
    return PredictionModel(
      crop: json['crop'] as String? ?? 'Wheat',
      location: json['location'] as String? ?? 'Local Farm',
      weather: json['weather'] is Map<String, dynamic>
          ? WeatherModel.fromJson(json['weather'] as Map<String, dynamic>)
          : WeatherModel(
              temperature: 25.0,
              humidity: 60.0,
              rainfall: 0.0,
              windSpeed: 10.0,
              condition: 'Normal',
              locationName: 'Local Farm',
            ),
      cropHealthScore: (json['crop_health_score'] as num?)?.toDouble() ?? 75.0,
      healthStatus: json['health_status'] as String? ?? 'Healthy',
      riskLevel: json['risk_level'] as String? ?? 'Low',
      primaryRiskFactor: json['primary_risk_factor'] as String? ?? 'Optimal Conditions',
      agroClimaticRegime: json['agro_climatic_regime'] as String? ?? 'Favorable Agronomic Regime',
      causes: (json['causes'] as List<dynamic>?)?.map((e) => e.toString()).toList() ?? [],
      precautions: (json['precautions'] as List<dynamic>?)?.map((e) => e.toString()).toList() ?? [],
      aiExplanation: json['ai_explanation'] as String? ?? 'Conditions conform to standard agronomic envelopes.',
      timestamp: json['timestamp'] != null
          ? DateTime.tryParse(json['timestamp'].toString()) ?? DateTime.now()
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'crop': crop,
      'location': location,
      'weather': weather.toJson(),
      'crop_health_score': cropHealthScore,
      'health_status': healthStatus,
      'risk_level': riskLevel,
      'primary_risk_factor': primaryRiskFactor,
      'agro_climatic_regime': agroClimaticRegime,
      'causes': causes,
      'precautions': precautions,
      'ai_explanation': aiExplanation,
      'timestamp': timestamp.toIso8601String(),
    };
  }
}
