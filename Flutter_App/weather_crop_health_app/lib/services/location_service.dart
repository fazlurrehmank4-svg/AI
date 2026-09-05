import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class LocationResult {
  final double latitude;
  final double longitude;
  final String locationName;

  LocationResult({
    required this.latitude,
    required this.longitude,
    required this.locationName,
  });
}

class LocationService {
  static final LocationService _instance = LocationService._internal();
  factory LocationService() => _instance;
  LocationService._internal();

  static const String _defaultLocationKey = "farmer_default_location";

  /// Gets the farmer's stored default location name (or fallback)
  Future<String?> getSavedDefaultLocation() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final loc = prefs.getString(_defaultLocationKey) ?? prefs.getString("farm_loc");
      if (loc != null && loc.trim().isNotEmpty) {
        return loc.trim();
      }
      return null;
    } catch (_) {
      return null;
    }
  }

  /// Sets the farmer's default location name in local storage
  Future<void> setSavedDefaultLocation(String locationName) async {
    final clean = locationName.trim();
    if (clean.isEmpty) return;
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_defaultLocationKey, clean);
      await prefs.setString("farm_loc", clean);
    } catch (_) {}
  }

  /// Request GPS permissions and obtain current coordinates and reverse-geocoded place name
  Future<LocationResult?> getCurrentLocation() async {
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        debugPrint("[LocationService] Location service disabled.");
        return null;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          debugPrint("[LocationService] Location permission denied.");
          return null;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        debugPrint("[LocationService] Location permission permanently denied.");
        return null;
      }

      Position position = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.medium,
          timeLimit: Duration(seconds: 8),
        ),
      );

      String placeName = await reverseGeocode(position.latitude, position.longitude);

      // Save as farmer's default location
      await setSavedDefaultLocation(placeName);

      return LocationResult(
        latitude: position.latitude,
        longitude: position.longitude,
        locationName: placeName,
      );
    } catch (e) {
      debugPrint("[LocationService] Exception getting location: $e");
      return null;
    }
  }

  /// Reverse geocodes coordinates to a human-readable city or locality name
  Future<String> reverseGeocode(double lat, double lon) async {
    try {
      final url = Uri.parse(
        "https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=$lat&longitude=$lon&localityLanguage=en",
      );
      final response = await http.get(url).timeout(const Duration(seconds: 5));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final city = data["city"] ?? data["locality"] ?? data["principalSubdivision"];
        final country = data["countryName"] ?? "";
        if (city != null && city.toString().isNotEmpty) {
          return country.isNotEmpty ? "$city, $country" : city.toString();
        }
      }
    } catch (e) {
      debugPrint("[LocationService] Reverse geocode lookup fallback: $e");
    }

    return "Farm (${lat.toStringAsFixed(2)}, ${lon.toStringAsFixed(2)})";
  }
}
