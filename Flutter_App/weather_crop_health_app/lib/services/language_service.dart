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

  // Location Bottom Sheet Translations
  String get locationPickerTitle => t(
        en: "Choose Your Farm Location",
        hi: "अपनी कृषि भूमि का स्थान चुनें",
        ur: "اپنی کاشتکاری کی جگہ کا انتخاب کریں",
      );

  String get locationPickerSubtitle => t(
        en: "Select your agricultural district or auto-detect via GPS for live weather telemetry.",
        hi: "लाइव मौसम डेटा के लिए अपना कृषि जिला चुनें या GPS द्वारा खोजें।",
        ur: "براہ راست موسمیاتی ڈیٹا کے لیے اپنا زرعی ضلع منتخب کریں یا GPS استعمال کریں۔",
      );

  String get useGpsButton => t(
        en: "Use Current GPS Location",
        hi: "वर्तमान GPS स्थान का उपयोग करें",
        ur: "موجودہ GPS مقام استعمال کریں",
      );

  String get searchDistrictHint => t(
        en: "Type any district (e.g. Nashik, Ludhiana)...",
        hi: "किसी भी जिले का नाम लिखें (जैसे नासिक, लुधियाना)...",
        ur: "کسی بھی ضلع کا نام درج کریں (مثلاً ناشک، لدھیانہ)...",
      );

  String get majorHubsTitle => t(
        en: "Major Agricultural Hubs",
        hi: "प्रमुख कृषि केंद्र",
        ur: "اہم زرعی مراکز",
      );

  String get activeCropLabel => t(
        en: "Active Crop",
        hi: "सक्रिय फसल",
        ur: "فعال فصل",
      );

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

  // --- CROP NAME TRANSLATIONS ---
  static const Map<String, Map<String, String>> _cropMap = {
    "Wheat": {"hi": "गेहूँ", "ur": "گندم"},
    "Rice": {"hi": "धान (चावल)", "ur": "دھان (چاول)"},
    "Maize": {"hi": "मक्का", "ur": "مکئی"},
    "Jute": {"hi": "पटसन (जूट)", "ur": "پٹ سن"},
    "Tomato": {"hi": "टमाटर", "ur": "ٹماٹر"},
    "Potato": {"hi": "आलू", "ur": "آلو"},
    "Pepper": {"hi": "मिर्च (शिमला मिर्च)", "ur": "مرچ (شملہ مرچ)"},
    "Apple": {"hi": "सेब", "ur": "سیب"},
    "Cherry": {"hi": "चेरी", "ur": "چیری"},
    "Peach": {"hi": "आड़ू", "ur": "آڑو"},
    "Grapes": {"hi": "अंगूर", "ur": "انگور"},
    "Strawberry": {"hi": "स्ट्रॉबेरी", "ur": "اسٹرابیری"},
    "Banana": {"hi": "केला", "ur": "کیلا"},
    "Mango": {"hi": "आम", "ur": "آم"},
    "Orange": {"hi": "संतरा", "ur": "سنترا"},
    "Papaya": {"hi": "पपीता", "ur": "پپیتا"},
    "Pomegranate": {"hi": "अनार", "ur": "انار"},
    "Watermelon": {"hi": "तरबूज", "ur": "تربوز"},
    "Muskmelon": {"hi": "खरबूजा", "ur": "خربوزہ"},
    "Coconut": {"hi": "नारियल", "ur": "ناریل"},
    "Coffee": {"hi": "कॉफी", "ur": "کافی"},
    "Chickpea": {"hi": "चना", "ur": "چنا"},
    "Kidneybeans": {"hi": "राजमा", "ur": "راجما"},
    "Pigeonpeas": {"hi": "अरहर (तूर)", "ur": "ارہر (تُور)"},
    "Mothbeans": {"hi": "मोठ", "ur": "موٹھ"},
    "Mungbean": {"hi": "मूंग", "ur": "مونگ"},
    "Blackgram": {"hi": "उड़द", "ur": "اڑد"},
    "Lentil": {"hi": "मसूर", "ur": "مسور"},
    "Cotton": {"hi": "कपास (रुई)", "ur": "کپاس"},
    "Sugarcane": {"hi": "गन्ना", "ur": "گنا"},
  };

  String getCropName(String crop) {
    if (isEnglish) return crop;
    final dict = _cropMap[crop];
    if (dict != null) {
      if (isHindi && dict.containsKey("hi")) return dict["hi"]!;
      if (isUrdu && dict.containsKey("ur")) return dict["ur"]!;
    }
    return crop;
  }

  // --- CATEGORY TRANSLATIONS ---
  static const Map<String, Map<String, String>> _categoryMap = {
    "Cereal Grain": {"hi": "अनाज", "ur": "اناج"},
    "Cereal / Fodder": {"hi": "अनाज एवं चारा", "ur": "اناج اور چارہ"},
    "Fiber Crop": {"hi": "रेशेदार फसल", "ur": "ریشے دار فصل"},
    "Vegetable / Solanaceous": {"hi": "सब्जी", "ur": "سبزی"},
    "Tuber / Vegetable": {"hi": "कंद-मूल सब्जी", "ur": "کُند سبزی"},
    "Temperate Fruit": {"hi": "शीतोष्ण फल", "ur": "معتدل پھل"},
    "Stone Fruit": {"hi": "गुठलीदार फल", "ur": "گٹھلی دار پھل"},
    "Vine Fruit": {"hi": "बेलदार फल", "ur": "بیل دار پھل"},
    "Berry Fruit": {"hi": "बेरी फल", "ur": "بیری پھل"},
    "Tropical Fruit": {"hi": "उष्णकटिबंधीय फल", "ur": "ٹراپیکل پھل"},
    "Citrus Fruit": {"hi": "खट्टे फल (सिट्रस)", "ur": "کھٹے پھل"},
    "Subtropical Fruit": {"hi": "उपोष्णकटिबंधीय फल", "ur": "ذیلی ٹراپیکل پھل"},
    "Cucurbit Fruit": {"hi": "लता फल", "ur": "لتا پھل"},
    "Plantation / Palm": {"hi": "वृक्षारोपण एवं ताड़", "ur": "باغبانی اور تاڑ"},
    "Plantation / Beverage": {"hi": "पेय फसल", "ur": "مشروب کی فصل"},
    "Pulse / Legume": {"hi": "दाल एवं दलहन", "ur": "دال اور دالحن"},
    "Arid Pulse": {"hi": "शुष्क दाल", "ur": "خشک دال"},
    "Short Pulse": {"hi": "अल्पकालिक दाल", "ur": "مختصر مدتی دال"},
    "Cool Season Pulse": {"hi": "शीतकालीन दाल", "ur": "سردیوں کی دال"},
    "Fiber / Cash": {"hi": "नकदी फसल (रेशा)", "ur": "نقد فصل (ریشہ)"},
    "Cash / Commercial": {"hi": "नकदी फसल", "ur": "نقد فصل"},
  };

  String getCropCategory(String category) {
    if (isEnglish) return category;
    final dict = _categoryMap[category];
    if (dict != null) {
      if (isHindi && dict.containsKey("hi")) return dict["hi"]!;
      if (isUrdu && dict.containsKey("ur")) return dict["ur"]!;
    }
    return category;
  }

  // --- GROWING SEASON TRANSLATIONS ---
  static const Map<String, Map<String, String>> _seasonMap = {
    "Rabi (Winter)": {"hi": "रबी (शीतकालीन)", "ur": "ربیع (سردیاں)"},
    "Kharif (Monsoon)": {"hi": "खरीफ (मानसून)", "ur": "خریف (مون سون)"},
    "Kharif / Spring": {"hi": "खरीफ / वसंत", "ur": "خریف / بہار"},
    "Kharif": {"hi": "खरीफ", "ur": "خریف"},
    "Year-round": {"hi": "बारहमासी", "ur": "تمام سال"},
    "Rabi": {"hi": "रबी", "ur": "ربیع"},
    "Summer / Kharif": {"hi": "ग्रीष्म / खरीफ", "ur": "گرمیاں / خریف"},
    "Perennial": {"hi": "बारहमासी (सदाबहार)", "ur": "بارہماسی"},
    "Spring-Summer": {"hi": "वसंत-ग्रीष्म", "ur": "بہار-گرمیاں"},
    "Winter / Spring": {"hi": "शीतकालीन / वसंत", "ur": "سردیاں / بہار"},
    "Annual/Perennial": {"hi": "वार्षिक / बारहमासी", "ur": "سالانہ / بارہماسی"},
    "Zaid (Summer)": {"hi": "जायद (ग्रीष्मकालीन)", "ur": "زائد (گرمیاں)"},
    "Rabi / Kharif": {"hi": "रबी / खरीफ", "ur": "ربیع / خریف"},
    "Kharif / Summer": {"hi": "खरीफ / ग्रीष्म", "ur": "خریف / گرمیاں"},
    "Annual": {"hi": "वार्षिक", "ur": "سالانہ"},
  };

  String getCropSeason(String season) {
    if (isEnglish) return season;
    final dict = _seasonMap[season];
    if (dict != null) {
      if (isHindi && dict.containsKey("hi")) return dict["hi"]!;
      if (isUrdu && dict.containsKey("ur")) return dict["ur"]!;
    }
    return season;
  }

  // --- LOCATION & CITY TRANSLATIONS ---
  static const Map<String, Map<String, String>> _locationMap = {
    "New Delhi": {"hi": "नई दिल्ली", "ur": "نئی دہلی"},
    "Delhi": {"hi": "दिल्ली", "ur": "دہلی"},
    "Pune": {"hi": "पुणे", "ur": "پونے"},
    "Nashik": {"hi": "नासिक", "ur": "ناشک"},
    "Ludhiana": {"hi": "लुधियाना", "ur": "لدھیانہ"},
    "Nagpur": {"hi": "नागपुर", "ur": "ناگپور"},
    "Bathinda": {"hi": "बठिंडा", "ur": "بھٹنڈہ"},
    "Guntur": {"hi": "गुंटूर", "ur": "گنٹور"},
    "Shimla": {"hi": "शिमला", "ur": "شملہ"},
    "Varanasi": {"hi": "वाराणसी", "ur": "وارانسی"},
    "Hyderabad": {"hi": "हैदराबाद", "ur": "حیدرآباد"},
    "Bengaluru": {"hi": "बेंगलुरु", "ur": "بنگلورو"},
    "Mumbai": {"hi": "मुंबई", "ur": "ممبئی"},
    "Kolkata": {"hi": "कोलकाता", "ur": "کولکاتہ"},
    "Chennai": {"hi": "चेन्नई", "ur": "چنئی"},
    "Lucknow": {"hi": "लखनऊ", "ur": "لکھنؤ"},
    "Jaipur": {"hi": "जयपुर", "ur": "جے پور"},
    "Indore": {"hi": "इंदौर", "ur": "اندور"},
    "Ahmedabad": {"hi": "अहमदाबाद", "ur": "احمد آباد"},
    "Chandigarh": {"hi": "चंडीगढ़", "ur": "چندی گڑھ"},
    "Amritsar": {"hi": "अमृतसर", "ur": "امرتسر"},
    "Patna": {"hi": "पटना", "ur": "پٹنہ"},
    "Bhopal": {"hi": "भोपाल", "ur": "بھوپال"},
  };

  String getLocationName(String city) {
    if (isEnglish) return city;
    // Check direct match or substring match
    for (var entry in _locationMap.entries) {
      if (city.toLowerCase().contains(entry.key.toLowerCase())) {
        final dict = entry.value;
        if (isHindi && dict.containsKey("hi")) return dict["hi"]!;
        if (isUrdu && dict.containsKey("ur")) return dict["ur"]!;
      }
    }
    return city;
  }
}
