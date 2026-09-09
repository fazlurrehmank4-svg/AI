import 'package:flutter/material.dart';
import '../theme.dart';
import '../models/crop_model.dart';
import '../services/language_service.dart';

class CropSelectionScreen extends StatelessWidget {
  final CropModel? selectedCrop;

  const CropSelectionScreen({super.key, this.selectedCrop});

  @override
  Widget build(BuildContext context) {
    final crops = CropModel.supportedCrops;

    return ValueListenableBuilder<String>(
      valueListenable: LanguageService(),
      builder: (context, currentLang, _) {
        final optimalLabel = LanguageService().t(en: "Optimal", hi: "अनुकूलतम", ur: "بہترین");
        final rainfallLabel = LanguageService().t(en: "Rainfall", hi: "वर्षा", ur: "بارش");

        return Scaffold(
          backgroundColor: CropGuardTheme.background,
          appBar: AppBar(
            title: Text(LanguageService().selectCropTitle),
          ),
          body: ListView.builder(
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
            itemCount: crops.length,
            itemBuilder: (context, index) {
              final crop = crops[index];
              final isSelected = selectedCrop?.name == crop.name;
              final translatedName = LanguageService().getCropName(crop.name);
              final translatedSeason = LanguageService().getCropSeason(crop.growingSeason);
              final translatedCategory = LanguageService().getCropCategory(crop.category);

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
                                  Flexible(
                                    child: Text(
                                      translatedName,
                                      style: const TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.w800,
                                        color: CropGuardTheme.textPrimary,
                                      ),
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                    decoration: BoxDecoration(
                                      color: CropGuardTheme.primary.withValues(alpha: 0.08),
                                      borderRadius: BorderRadius.circular(6),
                                    ),
                                    child: Text(
                                      translatedSeason,
                                      style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w600, color: CropGuardTheme.primary),
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 4),
                              Text(
                                "$optimalLabel: ${crop.tempMin.toInt()}–${crop.tempMax.toInt()}°C • ${crop.humidityMin.toInt()}–${crop.humidityMax.toInt()}% RH",
                                style: const TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary),
                              ),
                              const SizedBox(height: 2),
                              Text(
                                "$rainfallLabel: ${crop.rainfallMin.toInt()}–${crop.rainfallMax.toInt()} mm • $translatedCategory",
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
      },
    );
  }
}
