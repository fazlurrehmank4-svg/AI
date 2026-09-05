class DailyForecastAlert {
  final String date;
  final String dayName;
  final double tempMax;
  final double tempMin;
  final double rainfall;
  final double windSpeed;
  final String condition;
  final int weatherCode;
  final String riskLevel;
  final bool hasHarm;
  final String harmSummary;
  final List<String> precautions;

  DailyForecastAlert({
    required this.date,
    required this.dayName,
    required this.tempMax,
    required this.tempMin,
    required this.rainfall,
    required this.windSpeed,
    required this.condition,
    required this.weatherCode,
    required this.riskLevel,
    required this.hasHarm,
    required this.harmSummary,
    required this.precautions,
  });

  factory DailyForecastAlert.fromJson(Map<String, dynamic> json) {
    return DailyForecastAlert(
      date: json['date'] as String? ?? '',
      dayName: json['day_name'] as String? ?? 'Day',
      tempMax: (json['temp_max'] as num?)?.toDouble() ?? 28.0,
      tempMin: (json['temp_min'] as num?)?.toDouble() ?? 20.0,
      rainfall: (json['rainfall'] as num?)?.toDouble() ?? 0.0,
      windSpeed: (json['wind_speed'] as num?)?.toDouble() ?? 10.0,
      condition: json['condition'] as String? ?? 'Normal',
      weatherCode: json['weather_code'] as int? ?? 0,
      riskLevel: json['risk_level'] as String? ?? 'Low',
      hasHarm: json['has_harm'] as bool? ?? false,
      harmSummary: json['harm_summary'] as String? ?? 'Favorable conditions.',
      precautions: (json['precautions'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
    );
  }
}

class ForecastAlertModel {
  final String crop;
  final String location;
  final String overallThreatLevel;
  final String summary;
  final List<DailyForecastAlert> alerts;

  ForecastAlertModel({
    required this.crop,
    required this.location,
    required this.overallThreatLevel,
    required this.summary,
    required this.alerts,
  });

  factory ForecastAlertModel.fromJson(Map<String, dynamic> json) {
    return ForecastAlertModel(
      crop: json['crop'] as String? ?? 'Crop',
      location: json['location'] as String? ?? 'Farm',
      overallThreatLevel: json['overall_threat_level'] as String? ?? 'Low',
      summary: json['summary'] as String? ?? '',
      alerts: (json['alerts'] as List<dynamic>?)
              ?.map((e) => DailyForecastAlert.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}
