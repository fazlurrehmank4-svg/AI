import 'package:flutter/material.dart';
import '../theme.dart';
import '../models/prediction_model.dart';
import '../widgets/health_score_gauge.dart';
import '../widgets/risk_badge.dart';
import 'causes_screen.dart';
import 'precautions_screen.dart';
import 'explanation_screen.dart';
import 'chatbot_screen.dart';

class PredictionScreen extends StatelessWidget {
  final PredictionModel prediction;

  const PredictionScreen({Key? key, required this.prediction}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(
        title: Text("${prediction.crop} Health Analysis"),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header Score & Status Card
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(22),
              child: Column(
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              prediction.crop,
                              style: const TextStyle(
                                fontSize: 22,
                                fontWeight: FontWeight.w800,
                                color: CropGuardTheme.textPrimary,
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                            Text(
                              prediction.location,
                              style: const TextStyle(fontSize: 13, color: CropGuardTheme.textSecondary),
                              overflow: TextOverflow.ellipsis,
                              maxLines: 1,
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 8),
                      RiskBadge(status: prediction.healthStatus, riskLevel: prediction.riskLevel),
                    ],
                  ),
                  const SizedBox(height: 24),
                  HealthScoreGauge(score: prediction.cropHealthScore, size: 130),
                  const SizedBox(height: 16),
                  Text(
                    prediction.primaryRiskFactor,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                      color: CropGuardTheme.textSecondary,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: const Color(0xFFE8F5E9),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      prediction.agroClimaticRegime,
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w700,
                        color: CropGuardTheme.primary,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 18),

            // Weather Metrics Snapshot
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildMetric("Temp", "${prediction.weather.temperature.round()}°C"),
                  _buildMetric("Humidity", "${prediction.weather.humidity.round()}%"),
                  _buildMetric("Rain", "${prediction.weather.rainfall.toStringAsFixed(1)}mm"),
                  _buildMetric("Wind", "${prediction.weather.windSpeed.round()}km/h"),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // "Why this prediction?" AI Explanation Button / Section
            GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => ExplanationScreen(prediction: prediction)),
                );
              },
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFFE8F5E9), Color(0xFFC8E6C9)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: CropGuardTheme.primaryLight, width: 1.2),
                ),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(8),
                      decoration: const BoxDecoration(
                        color: CropGuardTheme.primary,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.psychology_rounded, color: Colors.white, size: 20),
                    ),
                    const SizedBox(width: 14),
                    const Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            "Why this prediction?",
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.w800,
                              color: CropGuardTheme.primaryDark,
                            ),
                          ),
                          SizedBox(height: 2),
                          Text(
                            "View Backward Chaining AI Reasoning & Rule Trace",
                            style: TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary),
                          ),
                        ],
                      ),
                    ),
                    const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: CropGuardTheme.primary),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Possible Causes Section
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  "Possible Causes",
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                ),
                TextButton(
                  onPressed: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => CausesScreen(causes: prediction.causes, crop: prediction.crop)),
                  ),
                  child: const Text("View All"),
                ),
              ],
            ),
            const SizedBox(height: 8),
            ...prediction.causes.take(3).map((cause) => _buildBulletCard(Icons.info_outline, cause, CropGuardTheme.warningOrange)),
            const SizedBox(height: 16),

            // Precautions Section
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  "Recommended Precautions",
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                ),
                TextButton(
                  onPressed: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => PrecautionsScreen(precautions: prediction.precautions, crop: prediction.crop)),
                  ),
                  child: const Text("View All"),
                ),
              ],
            ),
            const SizedBox(height: 8),
            ...prediction.precautions.take(3).map((prec) => _buildBulletCard(Icons.check_circle_outline, prec, CropGuardTheme.primary)),
            const SizedBox(height: 24),

            // Ask Chatbot with this Context
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.chat_outlined),
                label: Text("Ask CropGuard AI About ${prediction.crop}"),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => ChatbotScreen(
                        activeCrop: prediction.crop,
                        currentPrediction: prediction,
                      ),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }

  Widget _buildMetric(String label, String value) {
    return Column(
      children: [
        Text(value, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 15, color: CropGuardTheme.textPrimary)),
        const SizedBox(height: 2),
        Text(label, style: const TextStyle(fontSize: 11, color: CropGuardTheme.textLight)),
      ],
    );
  }

  Widget _buildBulletCard(IconData icon, String text, Color accentColor) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: CropGuardTheme.cardDecoration,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 18, color: accentColor),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(fontSize: 13, color: CropGuardTheme.textPrimary, height: 1.35),
            ),
          ),
        ],
      ),
    );
  }
}
