import 'package:flutter/material.dart';
import '../theme.dart';

class HealthScoreGauge extends StatelessWidget {
  final double score; // 0 to 100
  final double size;

  const HealthScoreGauge({
    Key? key,
    required this.score,
    this.size = 140,
  }) : super(key: key);

  Color _getScoreColor() {
    if (score >= 75.0) return CropGuardTheme.healthyGreen;
    if (score >= 50.0) return CropGuardTheme.warningOrange;
    return CropGuardTheme.dangerRed;
  }

  String _getConditionLabel() {
    if (score >= 75.0) return "Healthy";
    if (score >= 50.0) return "At Risk";
    return "High Risk";
  }

  @override
  Widget build(BuildContext context) {
    final color = _getScoreColor();
    final clampedProgress = (score / 100.0).clamp(0.0, 1.0);

    return SizedBox(
      width: size,
      height: size,
      child: Stack(
        alignment: Alignment.center,
        children: [
          // Background ring
          SizedBox(
            width: size,
            height: size,
            child: CircularProgressIndicator(
              value: 1.0,
              strokeWidth: size * 0.08,
              valueColor: AlwaysStoppedAnimation<Color>(color.withOpacity(0.12)),
            ),
          ),
          // Active progress arc
          SizedBox(
            width: size,
            height: size,
            child: CircularProgressIndicator(
              value: clampedProgress,
              strokeWidth: size * 0.08,
              strokeCap: StrokeCap.round,
              valueColor: AlwaysStoppedAnimation<Color>(color),
            ),
          ),
          // Center Text
          Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                "${score.toInt()}",
                style: TextStyle(
                  fontSize: size * 0.28,
                  fontWeight: FontWeight.w800,
                  color: CropGuardTheme.textPrimary,
                  height: 1.0,
                ),
              ),
              Text(
                "/ 100",
                style: TextStyle(
                  fontSize: size * 0.11,
                  fontWeight: FontWeight.w500,
                  color: CropGuardTheme.textLight,
                ),
              ),
              const SizedBox(height: 2),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Text(
                  _getConditionLabel(),
                  style: TextStyle(
                    fontSize: size * 0.09,
                    fontWeight: FontWeight.w700,
                    color: color,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
