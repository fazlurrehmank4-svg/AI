import 'package:flutter/material.dart';
import '../models/weather_model.dart';
import '../theme.dart';

class WeatherCard extends StatelessWidget {
  final WeatherModel weather;
  final VoidCallback? onRefresh;

  const WeatherCard({
    Key? key,
    required this.weather,
    this.onRefresh,
  }) : super(key: key);

  IconData _getWeatherIcon(String cond) {
    final lower = cond.toLowerCase();
    if (lower.contains('rain') || lower.contains('shower')) return Icons.water_drop_rounded;
    if (lower.contains('cloud') || lower.contains('overcast')) return Icons.cloud_rounded;
    if (lower.contains('thunder') || lower.contains('storm')) return Icons.thunderstorm_rounded;
    if (lower.contains('fog')) return Icons.foggy;
    return Icons.wb_sunny_rounded;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: CropGuardTheme.cardDecoration,
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: CropGuardTheme.primary.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(Icons.location_on_rounded, color: CropGuardTheme.primary, size: 20),
                  ),
                  const SizedBox(width: 10),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        weather.locationName,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w700,
                          color: CropGuardTheme.textPrimary,
                        ),
                      ),
                      Text(
                        weather.source ?? "Live Agricultural Telemetry",
                        style: const TextStyle(
                          fontSize: 12,
                          color: CropGuardTheme.textSecondary,
                        ),
                      ),
                    ],
                  ),
                ],
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
                      weather.condition,
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
              _buildMetricItem(Icons.water_drop_outlined, "Humidity", "${weather.humidity.round()}%"),
              _buildMetricItem(Icons.grain_rounded, "Rainfall", "${weather.rainfall.toStringAsFixed(1)} mm"),
              _buildMetricItem(Icons.air_rounded, "Wind Speed", "${weather.windSpeed.round()} km/h"),
            ],
          ),
        ],
      ),
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
            color: CropGuardTheme.textLight,
          ),
        ),
      ],
    );
  }
}
