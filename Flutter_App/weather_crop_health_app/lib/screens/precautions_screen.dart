import 'package:flutter/material.dart';
import '../theme.dart';

class PrecautionsScreen extends StatelessWidget {
  final List<String> precautions;
  final String crop;

  const PrecautionsScreen({Key? key, required this.precautions, required this.crop}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(title: Text("$crop Field Action Checklist")),
      body: ListView.builder(
        padding: const EdgeInsets.all(20),
        itemCount: precautions.length,
        itemBuilder: (context, index) {
          final prec = precautions[index];
          return Container(
            margin: const EdgeInsets.only(bottom: 14),
            decoration: CropGuardTheme.cardDecoration,
            padding: const EdgeInsets.all(18),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    color: const Color(0xFFE8F5E9),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  alignment: Alignment.center,
                  child: const Icon(Icons.check_rounded, color: CropGuardTheme.primary, size: 20),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "Action Item ${index + 1}",
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w700,
                          color: CropGuardTheme.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        prec,
                        style: const TextStyle(fontSize: 13, color: CropGuardTheme.textSecondary, height: 1.35),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
