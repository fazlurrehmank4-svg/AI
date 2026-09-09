import 'package:flutter/material.dart';

class LanguageService extends ValueNotifier<String> {
  static final LanguageService _instance = LanguageService._internal();
  factory LanguageService() => _instance;
  LanguageService._internal() : super('en');

  String get currentLanguage => value;

  void setLanguage(String lang) {
    if (value != lang) {
      value = lang;
    }
  }

  bool get isHindi => value == 'hi';
  bool get isUrdu => value == 'ur';
  bool get isEnglish => value == 'en';

  // Helper dictionary for common App UI labels
  String translate({required String en, required String hi, required String ur}) {
    if (isUrdu) return ur;
    if (isHindi) return hi;
    return en;
  }
}
