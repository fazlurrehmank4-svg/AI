import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:weather_crop_health_app/widgets/logo_widget.dart';
import 'package:weather_crop_health_app/widgets/health_score_gauge.dart';
import 'package:weather_crop_health_app/widgets/risk_badge.dart';
import 'package:weather_crop_health_app/widgets/weather_card.dart';
import 'package:weather_crop_health_app/models/weather_model.dart';
import 'package:weather_crop_health_app/models/crop_model.dart';

void main() {
  testWidgets('CropGuardLogo renders app title and subtitle', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: CropGuardLogo(size: 80, showText: true),
        ),
      ),
    );

    expect(find.text("CropGuard AI"), findsOneWidget);
    expect(find.text("Weather-Based Crop Health Predictor"), findsOneWidget);
  });

  testWidgets('HealthScoreGauge renders score and condition', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: HealthScoreGauge(score: 85.0),
        ),
      ),
    );

    expect(find.text("85"), findsOneWidget);
    expect(find.text("Healthy"), findsOneWidget);
  });

  testWidgets('RiskBadge renders High Risk warning status', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: RiskBadge(status: "High Risk", riskLevel: "High"),
        ),
      ),
    );

    expect(find.text("High Risk"), findsOneWidget);
    expect(find.text(" (High Risk)"), findsOneWidget);
  });

  testWidgets('WeatherCard displays temperature, humidity, rainfall', (WidgetTester tester) async {
    final weather = WeatherModel(
      temperature: 27.0,
      humidity: 65.0,
      rainfall: 8.5,
      windSpeed: 14.0,
      condition: "Partly Cloudy",
      locationName: "Test Farm Station",
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: WeatherCard(weather: weather),
        ),
      ),
    );

    expect(find.text("Test Farm Station"), findsOneWidget);
    expect(find.text("27"), findsOneWidget);
    expect(find.text("65%"), findsOneWidget);
    expect(find.text("8.5 mm"), findsOneWidget);
  });

  test('CropModel contains all 8 required agricultural crops', () {
    final crops = CropModel.supportedCrops;
    expect(crops.length, 8);
    final names = crops.map((c) => c.name).toList();
    expect(names.contains("Wheat"), isTrue);
    expect(names.contains("Rice"), isTrue);
    expect(names.contains("Tomato"), isTrue);
    expect(names.contains("Maize"), isTrue);
    expect(names.contains("Cotton"), isTrue);
    expect(names.contains("Potato"), isTrue);
    expect(names.contains("Sugarcane"), isTrue);
    expect(names.contains("Chickpea"), isTrue);
  });
}
