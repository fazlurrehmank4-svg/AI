import 'package:flutter/material.dart';
import '../theme.dart';
import '../models/forecast_alert_model.dart';

class ForecastAlertCard extends StatefulWidget {
  final ForecastAlertModel forecastAlert;
  final VoidCallback? onRefresh;

  const ForecastAlertCard({
    Key? key,
    required this.forecastAlert,
    this.onRefresh,
  }) : super(key: key);

  @override
  State<ForecastAlertCard> createState() => _ForecastAlertCardState();
}

class _ForecastAlertCardState extends State<ForecastAlertCard> {
  int _selectedDayIndex = 0;

  Color _getRiskColor(String risk) {
    switch (risk.toLowerCase()) {
      case 'high':
      case 'critical':
        return CropGuardTheme.dangerRed;
      case 'moderate':
        return CropGuardTheme.warningOrange;
      case 'low':
      default:
        return CropGuardTheme.healthyGreen;
    }
  }

  IconData _getWeatherIcon(String condition) {
    final c = condition.toLowerCase();
    if (c.contains('rain') || c.contains('drizzle')) return Icons.water_drop_rounded;
    if (c.contains('thunder') || c.contains('storm')) return Icons.flash_on_rounded;
    if (c.contains('cloud')) return Icons.cloud_rounded;
    if (c.contains('fog')) return Icons.blur_on_rounded;
    return Icons.wb_sunny_rounded;
  }

  @override
  Widget build(BuildContext context) {
    final model = widget.forecastAlert;
    final overallColor = _getRiskColor(model.overallThreatLevel);
    final hasThreat = model.overallThreatLevel.toLowerCase() != 'low';
    final alerts = model.alerts;

    if (alerts.isEmpty) return const SizedBox.shrink();
    if (_selectedDayIndex >= alerts.length) _selectedDayIndex = 0;
    final activeDay = alerts[_selectedDayIndex];

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: hasThreat ? overallColor.withValues(alpha: 0.35) : CropGuardTheme.border,
          width: hasThreat ? 1.5 : 1.0,
        ),
        boxShadow: [
          BoxShadow(
            color: hasThreat ? overallColor.withValues(alpha: 0.08) : Colors.black.withValues(alpha: 0.04),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      padding: const EdgeInsets.all(18),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header Row
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: overallColor.withValues(alpha: 0.12),
                      shape: BoxShape.circle,
                    ),
                    child: Icon(
                      hasThreat ? Icons.warning_amber_rounded : Icons.shield_outlined,
                      color: overallColor,
                      size: 20,
                    ),
                  ),
                  const SizedBox(width: 10),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        "3-Day Crop Hazard Outlook",
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w800,
                          color: CropGuardTheme.textPrimary,
                        ),
                      ),
                      Text(
                        "${model.crop} • ${model.location}",
                        style: const TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary),
                      ),
                    ],
                  ),
                ],
              ),
              // Overall Threat Tag
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                decoration: BoxDecoration(
                  color: overallColor.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: overallColor.withValues(alpha: 0.3)),
                ),
                child: Text(
                  "${model.overallThreatLevel.toUpperCase()} RISK",
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w800,
                    color: overallColor,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),

          // 3-Day Selector Tabs
          Row(
            children: List.generate(alerts.length, (idx) {
              final day = alerts[idx];
              final isSelected = idx == _selectedDayIndex;
              final dayRiskColor = _getRiskColor(day.riskLevel);

              return Expanded(
                child: Padding(
                  padding: EdgeInsets.only(right: idx < alerts.length - 1 ? 8.0 : 0),
                  child: InkWell(
                    onTap: () => setState(() => _selectedDayIndex = idx),
                    borderRadius: BorderRadius.circular(14),
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 200),
                      padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? CropGuardTheme.primary.withValues(alpha: 0.08)
                            : Colors.grey.shade50,
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(
                          color: isSelected ? CropGuardTheme.primary : CropGuardTheme.border,
                          width: isSelected ? 1.5 : 1.0,
                        ),
                      ),
                      child: Column(
                        children: [
                          Text(
                            day.dayName,
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                              color: isSelected ? CropGuardTheme.primaryDark : CropGuardTheme.textPrimary,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Icon(
                            _getWeatherIcon(day.condition),
                            size: 18,
                            color: isSelected ? CropGuardTheme.primary : CropGuardTheme.textSecondary,
                          ),
                          const SizedBox(height: 4),
                          Text(
                            "${day.tempMax.toInt()}° / ${day.tempMin.toInt()}°",
                            style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: CropGuardTheme.textPrimary),
                          ),
                          if (day.rainfall > 0) ...[
                            const SizedBox(height: 2),
                            Text(
                              "${day.rainfall.toStringAsFixed(1)}mm",
                              style: const TextStyle(fontSize: 10, color: Colors.blue, fontWeight: FontWeight.w600),
                            ),
                          ],
                          const SizedBox(height: 4),
                          Container(
                            width: 8,
                            height: 8,
                            decoration: BoxDecoration(
                              color: dayRiskColor,
                              shape: BoxShape.circle,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              );
            }),
          ),
          const SizedBox(height: 16),

          // Selected Day Hazard Card
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: _getRiskColor(activeDay.riskLevel).withValues(alpha: 0.06),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(
                color: _getRiskColor(activeDay.riskLevel).withValues(alpha: 0.25),
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(
                      activeDay.hasHarm ? Icons.report_problem_rounded : Icons.check_circle_rounded,
                      size: 16,
                      color: _getRiskColor(activeDay.riskLevel),
                    ),
                    const SizedBox(width: 6),
                    Text(
                      "${activeDay.dayName} Threat Assessment (${activeDay.condition}):",
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w800,
                        color: _getRiskColor(activeDay.riskLevel),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 6),
                Text(
                  activeDay.harmSummary,
                  style: const TextStyle(
                    fontSize: 12.5,
                    height: 1.4,
                    fontWeight: FontWeight.w500,
                    color: CropGuardTheme.textPrimary,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 14),

          // Actionable Precautions Checklist
          Row(
            children: const [
              Icon(Icons.checklist_rounded, size: 16, color: CropGuardTheme.primary),
              SizedBox(width: 6),
              Text(
                "Required Farmer Precautions:",
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w800,
                  color: CropGuardTheme.textPrimary,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Column(
            children: activeDay.precautions.map((p) {
              return Padding(
                padding: const EdgeInsets.only(bottom: 6),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.arrow_right_rounded, size: 18, color: CropGuardTheme.primary),
                    const SizedBox(width: 4),
                    Expanded(
                      child: Text(
                        p,
                        style: const TextStyle(
                          fontSize: 12,
                          height: 1.35,
                          color: CropGuardTheme.textSecondary,
                        ),
                      ),
                    ),
                  ],
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }
}
