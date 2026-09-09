import 'package:flutter/material.dart';
import '../models/weather_model.dart';
import '../theme.dart';
import '../services/language_service.dart';

class WeatherCard extends StatelessWidget {
  final WeatherModel weather;
  final VoidCallback? onRefresh;

  const WeatherCard({
    super.key,
    required this.weather,
    this.onRefresh,
  });

  IconData _getWeatherIcon(String cond) {
    final lower = cond.toLowerCase();
    if (lower.contains('rain') || lower.contains('shower')) return Icons.water_drop_rounded;
    if (lower.contains('cloud') || lower.contains('overcast')) return Icons.cloud_rounded;
    if (lower.contains('thunder') || lower.contains('storm')) return Icons.thunderstorm_rounded;
    if (lower.contains('fog')) return Icons.foggy;
    return Icons.wb_sunny_rounded;
  }

  String _translateCondition(String cond) {
    final lower = cond.toLowerCase();
    if (lower.contains('cloud')) {
      return LanguageService().t(en: cond, hi: "आंशिक रूप से बादल", ur: "جزوی طور پر ابر آلود");
    } else if (lower.contains('rain')) {
      return LanguageService().t(en: cond, hi: "बारिश", ur: "بارش");
    } else if (lower.contains('sun') || lower.contains('clear')) {
      return LanguageService().t(en: cond, hi: "साफ / धूप", ur: "صاف / دھوپ");
    }
    return cond;
  }

  String _translateSource(String? source) {
    if (source == null) {
      return LanguageService().t(en: "Live Agricultural Telemetry", hi: "लाइव कृषि मौसम डेटा", ur: "براہ راست زرعی موسمیاتی ڈیٹا");
    }
    if (source.toLowerCase().contains("offline") || source.toLowerCase().contains("cached")) {
      return LanguageService().t(en: source, hi: "ऑफलाइन मौसम बेसलाइन", ur: "آف لائن موسمیاتی ڈیٹا");
    }
    return source;
  }

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<String>(
      valueListenable: LanguageService(),
      builder: (context, _, __) {
        final humidityLabel = LanguageService().t(en: "Humidity", hi: "नमी", ur: "نمی");
        final rainfallLabel = LanguageService().t(en: "Rainfall", hi: "वर्षा", ur: "بارش");
        final windLabel = LanguageService().t(en: "Wind Speed", hi: "हवा की गति", ur: "ہوا کی رفتار");

        return Container(
          decoration: CropGuardTheme.cardDecoration,
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: CropGuardTheme.primary.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(Icons.location_on_rounded, color: CropGuardTheme.primary, size: 20),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          weather.locationName,
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w700,
                            color: CropGuardTheme.textPrimary,
                          ),
                          overflow: TextOverflow.ellipsis,
                          maxLines: 1,
                        ),
                        Text(
                          _translateSource(weather.source),
                          style: const TextStyle(
                            fontSize: 12,
                            color: CropGuardTheme.textSecondary,
                          ),
                          overflow: TextOverflow.ellipsis,
                          maxLines: 1,
                        ),
                      ],
                    ),
                  ),
                  if (onRefresh != null)
                    IconButton(
                      icon: const Icon(Icons.refresh_rounded, color: CropGuardTheme.primary),
                      onPressed: onRefresh,
                    ),
                ],
              ),
              const SizedBox(height: 18),
              // Main Temperature & Condition Row
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "${weather.temperature.round()}",
                        style: const TextStyle(
                          fontSize: 44,
                          fontWeight: FontWeight.w800,
                          color: CropGuardTheme.textPrimary,
                          height: 1.0,
                        ),
                      ),
                      const Text(
                        "°C",
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.w600,
                          color: CropGuardTheme.primary,
                        ),
                      ),
                    ],
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: const Color(0xFFE8F5E9),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          _getWeatherIcon(weather.condition),
                          color: CropGuardTheme.primary,
                          size: 20,
                        ),
                        const SizedBox(width: 6),
                        Text(
                          _translateCondition(weather.condition),
                          style: const TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                            color: CropGuardTheme.primaryDark,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 18),
              const Divider(color: CropGuardTheme.border, height: 1),
              const SizedBox(height: 14),
              // Weather metrics grid (Humidity, Rain, Wind)
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildMetricItem(Icons.water_drop_outlined, humidityLabel, "${weather.humidity.round()}%"),
                  _buildMetricItem(Icons.grain_rounded, rainfallLabel, "${weather.rainfall.toStringAsFixed(1)} mm"),
                  _buildMetricItem(Icons.air_rounded, windLabel, "${weather.windSpeed.round()} km/h"),
                ],
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildMetricItem(IconData icon, String label, String value) {
    return Column(
      children: [
        Icon(icon, size: 20, color: CropGuardTheme.textSecondary),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w700,
            color: CropGuardTheme.textPrimary,
          ),
        ),
        Text(
          label,
          style: const TextStyle(
            fontSize: 11,
            color: CropGuardTheme.textSecondary,
          ),
        ),
      ],
    );
  }
}
