import 'package:flutter/material.dart';
import '../theme.dart';
import '../models/weather_model.dart';
import '../services/api_service.dart';
import '../widgets/weather_card.dart';

class WeatherScreen extends StatefulWidget {
  final WeatherModel? initialWeather;

  const WeatherScreen({Key? key, this.initialWeather}) : super(key: key);

  @override
  State<WeatherScreen> createState() => _WeatherScreenState();
}

class _WeatherScreenState extends State<WeatherScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _searchController = TextEditingController();
  WeatherModel? _weather;
  bool _isLoading = false;

  final List<String> _suggestedCities = [
    "New Delhi", "Pune", "Nashik", "Ludhiana", "Varanasi", "Hyderabad", "Bengaluru"
  ];

  @override
  void initState() {
    super.initState();
    _weather = widget.initialWeather;
    if (_weather == null) {
      _fetchWeatherForCity("New Delhi");
    }
  }

  Future<void> _fetchWeatherForCity(String city) async {
    setState(() => _isLoading = true);
    final w = await _apiService.fetchWeather(city: city);
    if (mounted) {
      setState(() {
        _weather = w;
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(title: const Text("Meteorological Telemetry")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Location Search Input
            TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: "Enter agricultural district or locality...",
                prefixIcon: const Icon(Icons.search, color: CropGuardTheme.primary),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.arrow_forward_rounded, color: CropGuardTheme.primary),
                  onPressed: () {
                    if (_searchController.text.trim().isNotEmpty) {
                      _fetchWeatherForCity(_searchController.text.trim());
                    }
                  },
                ),
              ),
              onSubmitted: (val) {
                if (val.trim().isNotEmpty) _fetchWeatherForCity(val.trim());
              },
            ),
            const SizedBox(height: 12),
            // Quick suggested regions
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: _suggestedCities.map((city) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: ActionChip(
                      label: Text(city),
                      backgroundColor: Colors.white,
                      side: const BorderSide(color: CropGuardTheme.border),
                      labelStyle: const TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary),
                      onPressed: () {
                        _searchController.text = city;
                        _fetchWeatherForCity(city);
                      },
                    ),
                  );
                }).toList(),
              ),
            ),
            const SizedBox(height: 24),

            if (_isLoading)
              const Center(
                child: Padding(
                  padding: EdgeInsets.all(40),
                  child: CircularProgressIndicator(color: CropGuardTheme.primary),
                ),
              )
            else if (_weather != null) ...[
              WeatherCard(
                weather: _weather!,
                onRefresh: () => _fetchWeatherForCity(_weather!.locationName),
              ),
              const SizedBox(height: 20),
              // Telemetry Detailed Grid
              Container(
                decoration: CropGuardTheme.cardDecoration,
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "Detailed Agronomic Sensors",
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w800,
                        color: CropGuardTheme.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 16),
                    _buildDetailRow("Ambient Canopy Temp", "${_weather!.temperature.toStringAsFixed(1)} °C"),
                    const Divider(color: CropGuardTheme.border),
                    _buildDetailRow("Relative Air Humidity", "${_weather!.humidity.toStringAsFixed(1)} %"),
                    const Divider(color: CropGuardTheme.border),
                    _buildDetailRow("Hourly Precipitation", "${_weather!.rainfall.toStringAsFixed(1)} mm"),
                    const Divider(color: CropGuardTheme.border),
                    _buildDetailRow("Wind Velocity (10m)", "${_weather!.windSpeed.toStringAsFixed(1)} km/h"),
                    if (_weather!.surfacePressure != null) ...[
                      const Divider(color: CropGuardTheme.border),
                      _buildDetailRow("Atmospheric Pressure", "${_weather!.surfacePressure!.toStringAsFixed(1)} hPa"),
                    ],
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 14, color: CropGuardTheme.textSecondary)),
          Text(value, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: CropGuardTheme.textPrimary)),
        ],
      ),
    );
  }
}
