import 'package:flutter/material.dart';
import '../theme.dart';

class CausesScreen extends StatelessWidget {
  final List<String> causes;
  final String crop;

  const CausesScreen({Key? key, required this.causes, required this.crop}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(title: Text("$crop Risk Etiology & Causes")),
      body: ListView.builder(
        padding: const EdgeInsets.all(20),
        itemCount: causes.length,
        itemBuilder: (context, index) {
          final cause = causes[index];
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
                    color: const Color(0xFFFFF3E0),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  alignment: Alignment.center,
                  child: Text(
                    "${index + 1}",
                    style: const TextStyle(
                      fontWeight: FontWeight.w800,
                      color: CropGuardTheme.warningOrange,
                    ),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "Agronomic Factor ${index + 1}",
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w700,
                          color: CropGuardTheme.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        cause,
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
