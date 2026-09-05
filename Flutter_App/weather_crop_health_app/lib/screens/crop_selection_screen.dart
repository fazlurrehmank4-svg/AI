import 'package:flutter/material.dart';
import '../theme.dart';
import '../models/crop_model.dart';

class CropSelectionScreen extends StatelessWidget {
  final CropModel? selectedCrop;

  const CropSelectionScreen({Key? key, this.selectedCrop}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final crops = CropModel.supportedCrops;

    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(
        title: const Text("Select Cultivated Crop"),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
        itemCount: crops.length,
        itemBuilder: (context, index) {
          final crop = crops[index];
          final isSelected = selectedCrop?.name == crop.name;

          return Container(
            margin: const EdgeInsets.only(bottom: 14),
            decoration: isSelected
                ? CropGuardTheme.activeCardDecoration
                : CropGuardTheme.cardDecoration,
            child: InkWell(
              borderRadius: BorderRadius.circular(18),
              onTap: () => Navigator.pop(context, crop),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  children: [
                    Container(
                      width: 52,
                      height: 52,
                      decoration: BoxDecoration(
                        color: isSelected ? const Color(0xFFE8F5E9) : const Color(0xFFF7FAF7),
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(
                          color: isSelected ? CropGuardTheme.primaryLight : CropGuardTheme.border,
                          width: 1.2,
                        ),
                      ),
                      alignment: Alignment.center,
                      child: Text(crop.emoji, style: const TextStyle(fontSize: 26)),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Text(
                                crop.name,
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w800,
                                  color: CropGuardTheme.textPrimary,
                                ),
                              ),
                              const SizedBox(width: 8),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(
                                  color: CropGuardTheme.primary.withOpacity(0.08),
                                  borderRadius: BorderRadius.circular(6),
                                ),
                                child: Text(
                                  crop.growingSeason,
                                  style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w600, color: CropGuardTheme.primary),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 4),
                          Text(
                            "Optimal: ${crop.tempMin.toInt()}–${crop.tempMax.toInt()}°C • ${crop.humidityMin.toInt()}–${crop.humidityMax.toInt()}% RH",
                            style: const TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            "Rainfall: ${crop.rainfallMin.toInt()}–${crop.rainfallMax.toInt()} mm • ${crop.soilType}",
                            style: const TextStyle(fontSize: 11, color: CropGuardTheme.textLight),
                          ),
                        ],
                      ),
                    ),
                    Icon(
                      isSelected ? Icons.check_circle_rounded : Icons.radio_button_unchecked,
                      color: isSelected ? CropGuardTheme.primary : CropGuardTheme.border,
                      size: 24,
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
