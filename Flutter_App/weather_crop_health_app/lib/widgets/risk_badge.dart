import 'package:flutter/material.dart';
import '../theme.dart';
import '../services/language_service.dart';

class RiskBadge extends StatelessWidget {
  final String status; // 'Healthy', 'At Risk', 'High Risk'
  final String? riskLevel; // 'Low', 'Moderate', 'High'

  const RiskBadge({
    super.key,
    required this.status,
    this.riskLevel,
  });

  Color _getColor() {
    switch (status.toLowerCase()) {
      case 'healthy':
        return CropGuardTheme.healthyGreen;
      case 'at risk':
        return CropGuardTheme.warningOrange;
      case 'high risk':
      case 'severe':
        return CropGuardTheme.dangerRed;
      default:
        return CropGuardTheme.primary;
    }
  }

  IconData _getIcon() {
    switch (status.toLowerCase()) {
      case 'healthy':
        return Icons.check_circle_rounded;
      case 'at risk':
        return Icons.warning_amber_rounded;
      case 'high risk':
      case 'severe':
        return Icons.error_rounded;
      default:
        return Icons.eco_rounded;
    }
  }

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<String>(
      valueListenable: LanguageService(),
      builder: (context, _, __) {
        final color = _getColor();
        final displayStatus = LanguageService().translateStatus(status);

        String? displayRiskLevel;
        if (riskLevel != null) {
          final rLower = riskLevel!.toLowerCase();
          if (rLower.contains("high") || rLower.contains("severe")) {
            displayRiskLevel = LanguageService().t(en: "High Risk", hi: "उच्च जोखिम", ur: "شدید خطرہ");
          } else if (rLower.contains("mod") || rLower.contains("risk")) {
            displayRiskLevel = LanguageService().t(en: "Moderate Risk", hi: "मध्यम जोखिम", ur: "متوسط خطرہ");
          } else {
            displayRiskLevel = LanguageService().t(en: "Low Risk", hi: "कम जोखिम", ur: "کم خطرہ");
          }
        }

        return Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: color.withValues(alpha: 0.12),
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: color.withValues(alpha: 0.35), width: 1.2),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(_getIcon(), size: 16, color: color),
              const SizedBox(width: 6),
              Text(
                displayStatus,
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  color: color,
                ),
              ),
              if (displayRiskLevel != null) ...[
                Text(
                  " ($displayRiskLevel)",
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                    color: color.withValues(alpha: 0.85),
                  ),
                ),
              ],
            ],
          ),
        );
      },
    );
  }
}
