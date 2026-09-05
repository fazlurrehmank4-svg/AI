import 'package:flutter/material.dart';

class CropGuardTheme {
  // Brand Color Palette - Fresh Agricultural Identity
  static const Color primary = Color(0xFF1B5E20);      // Deep Emerald Green
  static const Color primaryLight = Color(0xFF4CAF50); // Fresh Leaf Green
  static const Color primaryDark = Color(0xFF0E3812);  // Rich Forest Green
  static const Color accent = Color(0xFF81C784);       // Soft Mint Green
  static const Color background = Color(0xFFF7FAF7);   // Ultra-light earthy background
  static const Color surface = Color(0xFFFFFFFF);      // Clean White
  static const Color cardBg = Color(0xFFFFFFFF);
  static const Color textPrimary = Color(0xFF1A2E1C);  // Deep organic dark
  static const Color textSecondary = Color(0xFF5A725D);// Muted botanical slate
  static const Color textLight = Color(0xFF8FA892);
  static const Color border = Color(0xFFE0EBE1);

  // Status Risk Indicator Colors
  static const Color healthyGreen = Color(0xFF2E7D32); // Low Risk
  static const Color warningOrange = Color(0xFFEF6C00); // Moderate Risk
  static const Color dangerRed = Color(0xFFC62828);     // High Risk

  // Card Decoration
  static BoxDecoration cardDecoration = BoxDecoration(
    color: surface,
    borderRadius: BorderRadius.circular(18),
    border: Border.all(color: border, width: 1.2),
    boxShadow: [
      BoxShadow(
        color: const Color(0xFF1B5E20).withOpacity(0.04),
        blurRadius: 16,
        offset: const Offset(0, 6),
      ),
    ],
  );

  // Active Highlight Card
  static BoxDecoration activeCardDecoration = BoxDecoration(
    color: const Color(0xFFF0F7F1),
    borderRadius: BorderRadius.circular(18),
    border: Border.all(color: primaryLight, width: 1.5),
    boxShadow: [
      BoxShadow(
        color: primaryLight.withOpacity(0.08),
        blurRadius: 18,
        offset: const Offset(0, 6),
      ),
    ],
  );

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      scaffoldBackgroundColor: background,
      primaryColor: primary,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primary,
        primary: primary,
        secondary: primaryLight,
        surface: surface,
        background: background,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: surface,
        foregroundColor: textPrimary,
        elevation: 0,
        centerTitle: true,
        iconTheme: IconThemeData(color: primary),
        titleTextStyle: TextStyle(
          color: textPrimary,
          fontSize: 18,
          fontWeight: FontWeight.w700,
          letterSpacing: -0.3,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: Colors.white,
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 15),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
          textStyle: const TextStyle(
            fontSize: 15,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.2,
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: primary,
          side: const BorderSide(color: primary, width: 1.5),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surface,
        contentPadding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: border, width: 1.2),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: border, width: 1.2),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: primary, width: 2.0),
        ),
        labelStyle: const TextStyle(color: textSecondary, fontSize: 14),
        hintStyle: const TextStyle(color: textLight, fontSize: 14),
      ),
    );
  }
}
