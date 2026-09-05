class WeatherModel {
  final double temperature;
  final double humidity;
  final double rainfall;
  final double windSpeed;
  final double? surfacePressure;
  final String condition;
  final String locationName;
  final String? source;

  WeatherModel({
    required this.temperature,
    required this.humidity,
    required this.rainfall,
    required this.windSpeed,
    this.surfacePressure,
    required this.condition,
    required this.locationName,
    this.source,
  });

  factory WeatherModel.fromJson(Map<String, dynamic> json) {
    return WeatherModel(
      temperature: (json['temperature'] as num?)?.toDouble() ?? 25.0,
      humidity: (json['humidity'] as num?)?.toDouble() ?? 60.0,
      rainfall: (json['rainfall'] as num?)?.toDouble() ?? 0.0,
      windSpeed: (json['wind_speed'] as num?)?.toDouble() ?? 10.0,
      surfacePressure: (json['surface_pressure'] as num?)?.toDouble(),
      condition: json['condition'] as String? ?? 'Normal',
      locationName: json['location_name'] as String? ?? 'Local Farm',
      source: json['source'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'temperature': temperature,
      'humidity': humidity,
      'rainfall': rainfall,
      'wind_speed': windSpeed,
      'surface_pressure': surfacePressure,
      'condition': condition,
      'location_name': locationName,
      'source': source,
    };
  }
}
