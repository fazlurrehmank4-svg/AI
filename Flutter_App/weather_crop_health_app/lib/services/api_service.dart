import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/weather_model.dart';
import '../models/prediction_model.dart';
import '../models/chat_message_model.dart';
import '../models/forecast_alert_model.dart';

class ApiService {
  static const String defaultEmulatorUrl = "https://ai-fb48.onrender.com";
  static const String defaultLocalhostUrl = "http://127.0.0.1:8000";

  static String get defaultBaseUrl => kIsWeb ? defaultLocalhostUrl : defaultEmulatorUrl;

  String _baseUrl = defaultBaseUrl;

  ApiService() {
    _loadBaseUrl();
  }

  Future<void> _loadBaseUrl() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      _baseUrl = prefs.getString("backend_url") ?? defaultBaseUrl;
    } catch (_) {}
  }

  Future<void> setBaseUrl(String url) async {
    _baseUrl = url.trim();
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("backend_url", _baseUrl);
    } catch (_) {}
  }

  String get baseUrl => _baseUrl;

  /// Fetches real-time weather from backend or directly from Open-Meteo free API
  Future<WeatherModel> fetchWeather({String? city, double? lat, double? lon}) async {
    // 1. Try Backend endpoint first
    try {
      String endpoint = "$_baseUrl/weather";
      if (lat != null && lon != null) {
        endpoint += "?lat=$lat&lon=$lon";
      } else if (city != null && city.trim().isNotEmpty) {
        endpoint += "?city=${Uri.encodeComponent(city.trim())}";
      } else {
        endpoint += "?city=New%20Delhi";
      }

      final response = await http.get(Uri.parse(endpoint)).timeout(const Duration(seconds: 4));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return WeatherModel.fromJson(data);
      }
    } catch (e) {
      print("[ApiService] Backend weather fetch failed, querying Open-Meteo directly: $e");
    }

    // 2. Direct Open-Meteo Free API (Zero key required, 100% free live weather)
    try {
      final directWeather = await _fetchDirectOpenMeteo(city: city, lat: lat, lon: lon);
      if (directWeather != null) {
        return directWeather;
      }
    } catch (e) {
      print("[ApiService] Direct Open-Meteo fetch failed: $e");
    }

    // 3. Fallback baseline if completely offline
    final targetLoc = (city != null && city.trim().isNotEmpty) ? city.trim() : "Local Farm";
    final int hash = targetLoc.codeUnits.fold(0, (prev, elem) => prev + elem);
    final double temp = 22.0 + (hash % 10) + 0.5;

    return WeatherModel(
      temperature: temp,
      humidity: (55 + (hash % 30)).toDouble(),
      rainfall: ((hash % 5) * 1.5),
      windSpeed: (8 + (hash % 12)).toDouble(),
      surfacePressure: 1013.0,
      condition: "Partly Cloudy",
      locationName: targetLoc,
      source: "Offline Baseline Telemetry",
    );
  }

  /// Direct free Open-Meteo fetcher without needing backend or API key
  Future<WeatherModel?> _fetchDirectOpenMeteo({String? city, double? lat, double? lon}) async {
    double? latitude = lat;
    double? longitude = lon;
    String locationName = city ?? "Local Farm";

    // If coordinates are not provided, geocode using Open-Meteo Free Geocoding API
    if (latitude == null || longitude == null) {
      final queryCity = (city != null && city.trim().isNotEmpty) ? city.trim() : "New Delhi";
      final searchTerm = queryCity.contains(",") ? queryCity.split(",")[0].trim() : queryCity;
      
      final geoUrl = "https://geocoding-api.open-meteo.com/v1/search?name=${Uri.encodeComponent(searchTerm)}&count=1&language=en&format=json";
      final geoRes = await http.get(Uri.parse(geoUrl), headers: {"User-Agent": "CropGuardApp/1.0"}).timeout(const Duration(seconds: 6));
      
      if (geoRes.statusCode == 200) {
        final geoData = json.decode(geoRes.body);
        final results = geoData['results'] as List<dynamic>?;
        if (results != null && results.isNotEmpty) {
          latitude = (results[0]['latitude'] as num).toDouble();
          longitude = (results[0]['longitude'] as num).toDouble();
          final name = results[0]['name'] as String? ?? queryCity;
          final country = results[0]['country'] as String?;
          final admin1 = results[0]['admin1'] as String?;
          if (admin1 != null && admin1.isNotEmpty && admin1 != name) {
            locationName = "$name, $admin1";
          } else if (country != null && country.isNotEmpty) {
            locationName = "$name, $country";
          } else {
            locationName = name;
          }
        }
      }
    }

    if (latitude == null || longitude == null) {
      latitude = 28.6139;
      longitude = 77.2090;
      locationName = "New Delhi, India";
    }

    // Query Open-Meteo Current Weather
    final forecastUrl = "https://api.open-meteo.com/v1/forecast?latitude=$latitude&longitude=$longitude&current=temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m,weather_code";
    final forecastRes = await http.get(Uri.parse(forecastUrl), headers: {"User-Agent": "CropGuardApp/1.0"}).timeout(const Duration(seconds: 6));

    if (forecastRes.statusCode == 200) {
      final fData = json.decode(forecastRes.body);
      final current = fData['current'] as Map<String, dynamic>?;
      if (current != null) {
        final code = (current['weather_code'] as num?)?.toInt() ?? 0;
        final condition = _wmoCodeToCondition(code);
        return WeatherModel(
          temperature: (current['temperature_2m'] as num?)?.toDouble() ?? 25.0,
          humidity: (current['relative_humidity_2m'] as num?)?.toDouble() ?? 60.0,
          rainfall: (current['precipitation'] as num?)?.toDouble() ?? 0.0,
          windSpeed: (current['wind_speed_10m'] as num?)?.toDouble() ?? 10.0,
          surfacePressure: (current['surface_pressure'] as num?)?.toDouble() ?? 1013.2,
          condition: condition,
          locationName: locationName,
          source: "Open-Meteo (Free Live Weather)",
        );
      }
    }

    return null;
  }

  static String _wmoCodeToCondition(int code) {
    if (code == 0) return "Clear Sky";
    if (code == 1 || code == 2 || code == 3) return "Partly Cloudy";
    if (code == 45 || code == 48) return "Foggy";
    if (code >= 51 && code <= 55) return "Drizzle";
    if (code >= 61 && code <= 65) return "Rain";
    if (code >= 71 && code <= 75) return "Snow";
    if (code >= 80 && code <= 82) return "Rain Showers";
    if (code >= 95 && code <= 99) return "Thunderstorm";
    return "Overcast";
  }

  /// Sends prediction request to /predict
  Future<PredictionModel> predictCropHealth({
    required String crop,
    required WeatherModel weather,
    double soilPh = 6.5,
    String? userId,
    String? authToken,
  }) async {
    final payload = {
      "crop": crop,
      "weather": weather.toJson(),
      "soil_ph": soilPh,
      "user_id": userId ?? "guest-farmer",
    };

    try {
      final headers = {"Content-Type": "application/json"};
      if (authToken != null) {
        headers["Authorization"] = "Bearer $authToken";
      }

      final response = await http
          .post(
            Uri.parse("$_baseUrl/predict"),
            headers: headers,
            body: json.encode(payload),
          )
          .timeout(const Duration(seconds: 12));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return PredictionModel.fromJson(data);
      }
    } catch (e) {
      print("[ApiService] Predict exception: $e");
    }

    // Local fallback prediction if offline
    return PredictionModel(
      crop: crop,
      location: weather.locationName,
      weather: weather,
      cropHealthScore: 78.5,
      healthStatus: "Healthy",
      riskLevel: "Low",
      primaryRiskFactor: "Optimal Conditions",
      agroClimaticRegime: "Favorable Agronomic Regime",
      causes: [
        "Temperature and moisture levels remain within optimal developmental ranges for $crop.",
        "Soil moisture retention supports balanced root respiration.",
      ],
      precautions: [
        "Maintain routine canopy scouting twice weekly.",
        "Continue scheduled drip irrigation according to evapotranspiration demand.",
      ],
      aiExplanation: "Current ambient temperature and humidity conform with $crop biology.",
      timestamp: DateTime.now(),
    );
  }

  /// Sends message to /chat (Zero external LLMs)
  Future<ChatMessageModel> sendChatMessage({
    required String message,
    String? crop,
    PredictionModel? currentPrediction,
    String? userId,
    String language = "auto",
  }) async {
    final payload = {
      "message": message,
      "crop": crop,
      "current_prediction": currentPrediction?.toJson(),
      "user_id": userId,
      "language": language,
    };

    final candidateUrls = <String>{
      _baseUrl,
      defaultLocalhostUrl,
      "http://10.0.2.2:8000",
      defaultEmulatorUrl,
    };

    for (final base in candidateUrls) {
      try {
        final response = await http
            .post(
              Uri.parse("$base/chat"),
              headers: {"Content-Type": "application/json"},
              body: json.encode(payload),
            )
            .timeout(const Duration(seconds: 5));

        if (response.statusCode == 200) {
          final data = json.decode(utf8.decode(response.bodyBytes));
          return ChatMessageModel.bot(
            message: data['answer'] ?? "No response received.",
            confidence: (data['confidence'] as num?)?.toDouble(),
            matchedTopic: data['matched_topic'] as String?,
            category: data['category'] as String?,
            reasoningSummary: data['reasoning_summary'] as String?,
          );
        }
      } catch (e) {
        print("[ApiService] Chat attempt failed on $base: $e");
      }
    }

    final isHindi = language == "hi";
    final isUrdu = language == "ur";
    // Offline local fallback reply
    String fallbackMsg;
    if (isUrdu) {
      fallbackMsg = "آف لائن موڈ: براہ کرم یقینی بنائیں کہ CropGuard AI بیک اینڈ http://127.0.0.1:8000 پر فعال ہے۔\n\n"
          "معاون موضوعات: دھان اور گندم کی احتیاطی تدابیر، فصل کے لیے درجہ حرارت، ہوا میں نمی، بیماریاں اور بچاؤ۔";
    } else if (isHindi) {
      fallbackMsg = "ऑफ़लाइन मोड: कृपया सुनिश्चित करें कि CropGuard AI बैकएंड http://127.0.0.1:8000 पर चालू है।\n\n"
          "समर्थित विषय: धान और गेहूं की सावधानियां, फसल तापमान, हवा में नमी, रोग और उपाय।";
    } else {
      fallbackMsg = "I am running in offline mode. Please ensure the CropGuard AI backend is running on http://127.0.0.1:8000.\n\n"
          "Supported topics: rice/wheat precautions, temperature limits, humidity hazards, disease remedies.";
    }

    return ChatMessageModel.bot(
      message: fallbackMsg,
      confidence: 0.50,
      matchedTopic: "offline_fallback",
    );
  }

  /// Retrieves user prediction history from /history
  Future<List<PredictionModel>> fetchHistory({required String userId, String? token}) async {
    try {
      final headers = <String, String>{};
      if (token != null) {
        headers["Authorization"] = "Bearer $token";
      }

      final response = await http
          .get(
            Uri.parse("$_baseUrl/history?user_id=${Uri.encodeComponent(userId)}"),
            headers: headers,
          )
          .timeout(const Duration(seconds: 8));

      if (response.statusCode == 200) {
        final List<dynamic> list = json.decode(response.body);
        return list.map((item) => PredictionModel.fromJson(item)).toList();
      }
    } catch (e) {
      print("[ApiService] History fetch exception: $e");
    }

    return [];
  }

  /// Fetches 3-day weather forecast hazard alerts & precautions for active crop
  Future<ForecastAlertModel?> fetch3DayCropAlert({
    required String crop,
    String? city,
    double? lat,
    double? lon,
  }) async {
    try {
      String endpoint = "$_baseUrl/predict/forecast-alerts?crop=${Uri.encodeComponent(crop)}";
      if (lat != null && lon != null) {
        endpoint += "&lat=$lat&lon=$lon";
      } else if (city != null && city.isNotEmpty) {
        endpoint += "&city=${Uri.encodeComponent(city)}";
      }

      final response = await http.get(Uri.parse(endpoint)).timeout(const Duration(seconds: 4));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return ForecastAlertModel.fromJson(data);
      }
    } catch (e) {
      print("[ApiService] Backend 3-day forecast failed, using direct Open-Meteo: $e");
    }

    // Direct Open-Meteo Free 3-Day Forecast
    try {
      final directForecast = await _fetchDirectOpenMeteoForecast(crop: crop, city: city, lat: lat, lon: lon);
      if (directForecast != null) {
        return directForecast;
      }
    } catch (e) {
      print("[ApiService] Direct Open-Meteo 3-day forecast failed: $e");
    }

    return ForecastAlertModel(
      crop: crop,
      location: city ?? "Local Agricultural Zone",
      overallThreatLevel: "Low",
      summary: "3-Day Forecast: Favorable parameters expected for $crop.",
      alerts: [
        DailyForecastAlert(
          date: "Day 1",
          dayName: "Today",
          tempMax: 29.5,
          tempMin: 22.0,
          rainfall: 2.0,
          windSpeed: 11.0,
          condition: "Partly Cloudy",
          weatherCode: 1,
          riskLevel: "Low",
          hasHarm: false,
          harmSummary: "Normal biological range for $crop.",
          precautions: ["Maintain routine irrigation and field scouting."],
        ),
        DailyForecastAlert(
          date: "Day 2",
          dayName: "Tomorrow",
          tempMax: 31.0,
          tempMin: 23.5,
          rainfall: 0.0,
          windSpeed: 9.0,
          condition: "Sunny",
          weatherCode: 0,
          riskLevel: "Low",
          hasHarm: false,
          harmSummary: "Clear canopy sunshine; suitable for photosynthesis.",
          precautions: ["Check soil moisture in top 10cm before midday."],
        ),
        DailyForecastAlert(
          date: "Day 3",
          dayName: "In 2 Days",
          tempMax: 30.0,
          tempMin: 23.0,
          rainfall: 4.0,
          windSpeed: 12.0,
          condition: "Scattered Clouds",
          weatherCode: 2,
          riskLevel: "Low",
          hasHarm: false,
          harmSummary: "Stable temperature and humidity.",
          precautions: ["Adhere to scheduled nutrient schedule."],
        ),
      ],
    );
  }

  /// Direct free Open-Meteo 3-day forecast fetcher
  Future<ForecastAlertModel?> _fetchDirectOpenMeteoForecast({
    required String crop,
    String? city,
    double? lat,
    double? lon,
  }) async {
    double? latitude = lat;
    double? longitude = lon;
    String locationName = city ?? "Local Farm";

    if (latitude == null || longitude == null) {
      final queryCity = (city != null && city.trim().isNotEmpty) ? city.trim() : "New Delhi";
      final searchTerm = queryCity.contains(",") ? queryCity.split(",")[0].trim() : queryCity;
      
      final geoUrl = "https://geocoding-api.open-meteo.com/v1/search?name=${Uri.encodeComponent(searchTerm)}&count=1&language=en&format=json";
      final geoRes = await http.get(Uri.parse(geoUrl), headers: {"User-Agent": "CropGuardApp/1.0"}).timeout(const Duration(seconds: 6));
      
      if (geoRes.statusCode == 200) {
        final geoData = json.decode(geoRes.body);
        final results = geoData['results'] as List<dynamic>?;
        if (results != null && results.isNotEmpty) {
          latitude = (results[0]['latitude'] as num).toDouble();
          longitude = (results[0]['longitude'] as num).toDouble();
          final name = results[0]['name'] as String? ?? queryCity;
          locationName = name;
        }
      }
    }

    if (latitude == null || longitude == null) {
      latitude = 28.6139;
      longitude = 77.2090;
    }

    final url = "https://api.open-meteo.com/v1/forecast?latitude=$latitude&longitude=$longitude&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max&forecast_days=3&timezone=auto";
    final res = await http.get(Uri.parse(url), headers: {"User-Agent": "CropGuardApp/1.0"}).timeout(const Duration(seconds: 6));

    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      final daily = data['daily'] as Map<String, dynamic>?;
      if (daily != null) {
        final times = daily['time'] as List<dynamic>? ?? [];
        final codes = daily['weather_code'] as List<dynamic>? ?? [];
        final maxTemps = daily['temperature_2m_max'] as List<dynamic>? ?? [];
        final minTemps = daily['temperature_2m_min'] as List<dynamic>? ?? [];
        final rains = daily['precipitation_sum'] as List<dynamic>? ?? [];
        final winds = daily['wind_speed_10m_max'] as List<dynamic>? ?? [];

        final dayLabels = ["Today", "Tomorrow", "In 2 Days"];
        final List<DailyForecastAlert> alerts = [];
        bool anyHarm = false;

        for (int i = 0; i < times.length && i < 3; i++) {
          final tMax = (maxTemps[i] as num?)?.toDouble() ?? 30.0;
          final tMin = (minTemps[i] as num?)?.toDouble() ?? 22.0;
          final rain = (rains[i] as num?)?.toDouble() ?? 0.0;
          final wind = (winds[i] as num?)?.toDouble() ?? 10.0;
          final wCode = (codes[i] as num?)?.toInt() ?? 0;
          final cond = _wmoCodeToCondition(wCode);

          final harms = <String>[];
          final precautions = <String>[];

          if (tMax > 34.0) {
            harms.add("Extreme heat ($tMax°C) risks thermal stress for $crop.");
            precautions.add("Provide light shade netting and irrigate during cooler morning/evening.");
          }
          if (rain > 15.0) {
            harms.add("Heavy rainfall ($rain mm) creates root saturation risk.");
            precautions.add("Clear farm drainage channels to prevent waterlogging.");
          }
          if (wind > 28.0) {
            harms.add("High wind speed ($wind km/h) risks mechanical lodging.");
            precautions.add("Stake vulnerable plants and avoid foliar chemical sprays.");
          }

          final dayHarm = harms.isNotEmpty;
          if (dayHarm) anyHarm = true;

          alerts.add(DailyForecastAlert(
            date: times[i].toString(),
            dayName: i < dayLabels.length ? dayLabels[i] : times[i].toString(),
            tempMax: tMax,
            tempMin: tMin,
            rainfall: rain,
            windSpeed: wind,
            condition: cond,
            weatherCode: wCode,
            riskLevel: dayHarm ? "High" : "Low",
            hasHarm: dayHarm,
            harmSummary: dayHarm ? harms.join(" ") : "Favorable microclimate for $crop vegetative cycle.",
            precautions: precautions.isNotEmpty ? precautions : ["Maintain regular scouting and optimal irrigation schedule."],
          ));
        }

        return ForecastAlertModel(
          crop: crop,
          location: locationName,
          overallThreatLevel: anyHarm ? "Moderate" : "Low",
          summary: anyHarm ? "Weather anomalies predicted in the next 3 days for $crop." : "3-Day microclimate forecast is stable for $crop cultivation.",
          alerts: alerts,
        );
      }
    }

    return null;
  }
}
