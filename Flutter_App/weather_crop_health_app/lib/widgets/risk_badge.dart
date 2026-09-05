import 'package:flutter/material.dart';
import '../theme.dart';

class RiskBadge extends StatelessWidget {
  final String status; // 'Healthy', 'At Risk', 'High Risk'
  final String? riskLevel; // 'Low', 'Moderate', 'High'

  const RiskBadge({
    Key? key,
    required this.status,
    this.riskLevel,
  }) : super(key: key);

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
    final color = _getColor();
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.12),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withOpacity(0.35), width: 1.2),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(_getIcon(), size: 16, color: color),
          const SizedBox(width: 6),
          Text(
            status,
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w700,
              color: color,
            ),
          ),
          if (riskLevel != null) ...[
            Text(
              " ($riskLevel Risk)",
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w500,
                color: color.withOpacity(0.85),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
