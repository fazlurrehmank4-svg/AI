import 'package:flutter/material.dart';
import '../theme.dart';
import '../models/prediction_model.dart';

class ExplanationScreen extends StatelessWidget {
  final PredictionModel prediction;

  const ExplanationScreen({Key? key, required this.prediction}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(title: const Text("AI Reasoning & Explainability")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Banner
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: const Color(0xFFE8F5E9),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: CropGuardTheme.primaryLight, width: 1.2),
              ),
              child: const Row(
                children: [
                  Icon(Icons.psychology_outlined, color: CropGuardTheme.primary, size: 32),
                  SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Explainable AI (XAI) Architecture",
                          style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: CropGuardTheme.primaryDark),
                        ),
                        SizedBox(height: 3),
                        Text(
                          "Powered by Practical 05: Backward Chaining Inference Engine",
                          style: TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // AI Explanation Card
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Algorithmic Justification Proof",
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    prediction.aiExplanation,
                    style: const TextStyle(fontSize: 14, color: CropGuardTheme.textPrimary, height: 1.45),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Formal Chain Steps
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Multi-Tier Inference Flow",
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                  ),
                  const SizedBox(height: 16),
                  _buildStep(
                    step: "1",
                    title: "Meteorological Discretization",
                    desc: "Mapped continuous sensor readings (Temp: ${prediction.weather.temperature}°C, Humidity: ${prediction.weather.humidity}%) into discrete propositional facts.",
                  ),
                  const Divider(color: CropGuardTheme.border, height: 24),
                  _buildStep(
                    step: "2",
                    title: "Statistical ML Prediction",
                    desc: "Linear Regression computed health score (${prediction.cropHealthScore}/100) while Decision Tree classified state as '${prediction.healthStatus}'.",
                  ),
                  const Divider(color: CropGuardTheme.border, height: 24),
                  _buildStep(
                    step: "3",
                    title: "Backward Chaining Verification",
                    desc: "Goal hypothesis proved by checking satisfaction of biological preconditions against domain expert rules.",
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStep({required String step, required String title, required String desc}) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        CircleAvatar(
          radius: 14,
          backgroundColor: CropGuardTheme.primary,
          child: Text(step, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white)),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: CropGuardTheme.textPrimary)),
              const SizedBox(height: 3),
              Text(desc, style: const TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary, height: 1.3)),
            ],
          ),
        ),
      ],
    );
  }
}
