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

  String t({required String en, required String hi, required String ur}) {
    if (isUrdu) return ur;
    if (isHindi) return hi;
    return en;
  }

  // Dashboard UI Translations
  String welcome(String name) => t(
        en: "Welcome, $name 👋",
        hi: "स्वागत है, $name 👋",
        ur: "خوش آمدید، $name 👋",
      );

  String get selectCropTitle => t(
        en: "Select Active Crop",
        hi: "सक्रिय फसल का चयन करें",
        ur: "فعال فصل کا انتخاب کریں",
      );

  String get liveWeatherTitle => t(
        en: "Live Weather Telemetry",
        hi: "लाइव मौसम डेटा",
        ur: "براہ راست موسمیاتی ڈیٹا",
      );

  String get cropHealthDiagnosisTitle => t(
        en: "Crop Health Diagnosis",
        hi: "फसल स्वास्थ्य निदान",
        ur: "فصل کی صحت کی تشخیص",
      );

  String get causesAndPrecautionsTitle => t(
        en: "Key Causes & Remediation",
        hi: "प्रमुख कारण और निवारक उपाय",
        ur: "اہم وجوہات اور احتیاطی تدابیر",
      );

  String get askCropGuardButton => t(
        en: "Ask CropGuard AI",
        hi: "CropGuard से पूछें",
        ur: "CropGuard سے پوچھیں",
      );

  // Drawer Translations
  String get drawerDashboard => t(en: "Dashboard Overview", hi: "डैशबोर्ड अवलोकन", ur: "ڈیش بورڈ کا جائزہ");
  String get drawerWeather => t(en: "Live Meteorological Telemetry", hi: "लाइव मौसम विवरण", ur: "براہ راست موسمیاتی معلومات");
  String get drawerDiagnosis => t(en: "Crop Diagnosis & Risk Analysis", hi: "फसल निदान और जोखिम विश्लेषण", ur: "فصل کی تشخیص اور خطرے کا تجزیہ");
  String get drawerChatbot => t(en: "Local AI Farmer Chatbot", hi: "स्थानीय AI किसान चैटबॉट", ur: "مقامی AI کسان چیٹ باٹ");
  String get drawerHistory => t(en: "Prediction & Diagnostic Logs", hi: "पूर्वाभ्यास और निदान इतिहास", ur: "پیشگوئی اور تشخیص کا ریکارڈ");
  String get drawerProfile => t(en: "Farmer Profile", hi: "किसान प्रोफ़ाइल", ur: "کسان پروفائل");
  String get drawerSettings => t(en: "Settings & Preferences", hi: "सेटिंग्स और प्राथमिकताएं", ur: "سیٹنگز اور ترجیحات");
  String get drawerAbout => t(en: "About Project & AI Practicals", hi: "परियोजना और AI लैब प्रैक्टिकल", ur: "پراجیکٹ اور AI لیب پریکٹیکلز");

  // Health Status Translation
  String translateStatus(String status) {
    final lower = status.toLowerCase();
    if (lower.contains("healthy") || lower.contains("optimal")) {
      return t(en: "Healthy", hi: "उत्कृष्ट (स्वस्थ)", ur: "صحت مند");
    } else if (lower.contains("high")) {
      return t(en: "High Risk", hi: "उच्च जोखिम", ur: "شدید خطرہ");
    } else {
      return t(en: "At Risk", hi: "मध्यम जोखिम", ur: "خطرے میں");
    }
  }
}
