import 'package:flutter/material.dart';
import '../theme.dart';
import '../widgets/logo_widget.dart';

class AboutScreen extends StatefulWidget {
  const AboutScreen({super.key});

  @override
  State<AboutScreen> createState() => _AboutScreenState();
}

class _AboutScreenState extends State<AboutScreen> {
  String _selectedLanguage = "en"; // "en", "hi", "ur"

  @override
  Widget build(BuildContext context) {
    final isHindi = _selectedLanguage == "hi";
    final isUrdu = _selectedLanguage == "ur";

    final titleText = isUrdu
        ? "CropGuard AI کے بارے میں"
        : isHindi
            ? "CropGuard AI के बारे में"
            : "About CropGuard AI";

    final overviewTitle = isUrdu
        ? "زرعی AI لیب پریکٹیکلز کا تعارف"
        : isHindi
            ? "कृषि AI लैब प्रैक्टिकल अवलोकन"
            : "College AI Mini-Project Overview";

    final overviewBody = isUrdu
        ? "CropGuard AI ایک جامع زرعی فیصلہ سازی کا نظام ہے جو کسانوں کو فصل کی صحت، موسمی بیماریوں کے خطرات اور احتیاطی تدابیر کو سمجھنے میں مدد کرتا ہے۔\n\n"
          "یہ ایپلی کیشن 11 مصنوعی ذہانت (AI) لیب پریکٹیکلز کو ایک ہی فاسٹ اے پی آئی (FastAPI) اور سپابیس (Supabase) آرکیٹیکچر میں جوڑتی ہے۔"
        : isHindi
            ? "CropGuard AI एक व्यापक कृषि निर्णय सहायता प्रणाली है जो किसानों को फसल स्वास्थ्य, मौसमी बीमारियों के जोखिम और निवारक उपायों को समझने में मदद करती है।\n\n"
              "यह एप्लिकेशन 11 आर्टिफिशियल इंटेलिजेंस (AI) लैब प्रैक्टिकल को एक ही फ़ास्ट-एपीआई और सुपाबेस आर्किटेक्चर में एकीकृत करता है।"
            : "CropGuard AI is a comprehensive agricultural decision support system designed to assist farmers in understanding crop vigor, identifying meteorological disease vulnerabilities, and receiving actionable precautions.\n\n"
              "The application integrates all 11 Artificial Intelligence Laboratory Practicals into a single cohesive, deployable architecture with a FastAPI backend and Supabase database.";

    final practicalsTitle = isUrdu
        ? "شامل شدہ AI لیب پریکٹیکلز (کام اور نتائج)"
        : isHindi
            ? "एकीकृत AI लैब प्रैक्टिकल (कार्य और परिणाम)"
            : "Integrated AI Lab Practicals (Action & Results)";

    final actionHeading = isUrdu ? "کارروائی (Action): " : isHindi ? "कार्रवाई (Action): " : "Action: ";
    final resultHeading = isUrdu ? "نتیجہ (Result): " : isHindi ? "परिणाम (Result): " : "Result: ";

    final disclaimerText = isUrdu
        ? "تعلیمی ڈیسیژن سپورٹ ڈس کلیمر: CropGuard AI موسمیاتی اشاروں کی بنیاد پر پیشگوئی فراہم کرتا ہے۔ یہ کسی زرعی ماہر کے معائنے کا متبادل نہیں ہے۔"
        : isHindi
            ? "शैक्षणिक निर्णय-सहायता अस्वीकरण: CropGuard AI मौसम के संकेतकों के आधार पर जोखिम सलाह प्रदान करता है। यह कृषि विशेषज्ञ के निरीक्षण का विकल्प नहीं है।"
            : "Educational Decision-Support Disclaimer: CropGuard AI provides probabilistic risk advisories based on meteorological indicators. It is not an unconditional diagnosis or a substitute for on-site agricultural extension inspection.";

    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(
        title: Text(titleText),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        child: Column(
          children: [
            const CropGuardLogo(size: 72, showText: true),
            const SizedBox(height: 16),

            // Multilingual Language Selector (English, Hindi, Urdu)
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(30),
                boxShadow: const [
                  BoxShadow(color: Colors.black12, blurRadius: 4, offset: Offset(0, 2)),
                ],
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _buildLangChip("en", "English 🇬🇧"),
                  _buildLangChip("hi", "हिंदी 🇮🇳"),
                  _buildLangChip("ur", "اردو 🇵🇰"),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Overview Card
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    overviewTitle,
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    overviewBody,
                    style: const TextStyle(fontSize: 13, color: CropGuardTheme.textSecondary, height: 1.45),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 18),

            // AI Practicals Table with Clear Actions and Results
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    practicalsTitle,
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                  ),
                  const SizedBox(height: 14),

                  // Practical 01
                  _buildPracticalRow(
                    code: "P01",
                    tech: "NumPy, Pandas & Matplotlib",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "زرعی فیچرز کی ڈیٹا کلیننگ اور باہمی تعلق (Correlation Matrix) کی گنتی۔"
                        : isHindi
                            ? "कृषि सुविधाओं की डेटा सफाई और सहसंबंध (Correlation Matrix) की गणना।"
                            : "Preprocesses telemetry feature distributions & computes feature correlation matrix.",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "صاف ستھرا زرعی ڈیٹا سیٹ اور 4-پینل ویژولائزیشن ہیٹ میپ۔"
                        : isHindi
                            ? "स्वच्छ कृषि डेटासेट और 4-पैनल दृश्य सहसंबंध हीटमैप चार्ट।"
                            : "Cleaned agricultural dataset & 4-panel correlation heatmap.",
                  ),

                  // Practical 02
                  _buildPracticalRow(
                    code: "P02",
                    tech: "BFS & DFS Graph Search",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "فصل کے خطرے کی حالتوں میں لیول بہ لیول (BFS) اور گہرائی (DFS) کی تلاش۔"
                        : isHindi
                            ? "फसल जोखिम अवस्थाओं में स्तर-दर-स्तर (BFS) और गहराई (DFS) खोज करता है।"
                            : "Traverses decision trees level-by-level (BFS) and branch-by-branch (DFS) across risk states.",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "بغیر کسی گائیڈ کے سٹیٹ اسپیس روٹ (State-Space Path) کی مکمل دریافت۔"
                        : isHindi
                            ? "बिना किसी अनुमानी मार्गदर्शन के संपूर्ण अवस्था-स्थान पथ खोज (State-Space Discovery)।"
                            : "Complete state-space path discovery without heuristic guidance.",
                  ),

                  // Practical 03
                  _buildPracticalRow(
                    code: "P03",
                    tech: "GBFS & A* Search",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "کم ترین علاج کی لاگت h(n) اور کل لاگت f(n)=g(n)+h(n) کی گنتی۔"
                        : isHindi
                            ? "अनुमानी (Heuristic) लागत h(n) और f(n)=g(n)+h(n) का उपयोग करके सबसे कम लागत वाला मार्ग चुनता है।"
                            : "Computes minimal remediation path using heuristic h(n) and total path cost f(n)=g(n)+h(n).",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "35 فیصد کم وسائل کی لاگت کے ساتھ بہترین علاج کے مراحل۔"
                        : isHindi
                            ? "35% कम संसाधन लागत के साथ इष्टतम उपचारात्मक कदम।"
                            : "Optimal remediation intervention sequence with 35% lower resource cost.",
                  ),

                  // Practical 04
                  _buildPracticalRow(
                    code: "P04",
                    tech: "Hill Climbing & Simulated Annealing",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "میٹروپولیس قانون (P = e^(ΔE/T)) سے آبپاشی اور چھاؤں کا انتخاب۔"
                        : isHindi
                            ? "मेट्रोपोलिस मानदंड (P = e^(ΔE/T)) का उपयोग करके सिंचाई और छाया दर का अनुकूलन।"
                            : "Optimizes continuous irrigation and shade levels using Metropolis criterion P = exp(ΔE / T).",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "99.98 / 100 کا عالمی فصل سکور (مقامی غلط جال سے نجات)۔"
                        : isHindi
                            ? "99.98 / 100 का वैश्विक फसल आराम स्कोर (स्थानीय जाल से मुक्ति)।"
                            : "Global physiological crop comfort score of 99.98 / 100 (escaping local traps).",
                  ),

                  // Practical 05
                  _buildPracticalRow(
                    code: "P05",
                    tech: "Forward & Backward Chaining",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "فارورڈ چیننگ سے بیماری کی وجہ اور بیک ورڈ چیننگ سے XAI ثبوت کی گنتی۔"
                        : isHindi
                            ? "फॉरवर्ड चेनिंग से रोग कारण का अनुमान और बैकवर्ड चेनिंग से XAI प्रमाण प्रदान करता है।"
                            : "Executes forward deduction for root cause disease detection and backward chaining for XAI proofs.",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "واضح بیماری کی تشخیص اور قابل تصدیق XAI ثبوت کا راستہ۔"
                        : isHindi
                            ? "स्पष्ट रोग निदान और सत्यापित करने योग्य व्याख्यात्मक AI (XAI) प्रमाण।"
                            : "Deductive etiology diagnosis + verifiable Explainable AI (XAI) proof trace.",
                  ),

                  // Practical 06
                  _buildPracticalRow(
                    code: "P06",
                    tech: "Multiple Linear Regression",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "درجہ حرارت، نمی اور بارش پر لکیری ماڈل کا استعمال۔"
                        : isHindi
                            ? "तापमान, आर्द्रता और वर्षा पर लीनियर मॉडल फिट करके फसल स्वास्थ्य स्कोर का अनुमान।"
                            : "Fits linear parameters over temperature, humidity, and rainfall continuous inputs.",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "R² = 0.7313 اور MAE = 12.42 کے ساتھ فصل کا مسلسل ہیلتھ سکور (0-100)۔"
                        : isHindi
                            ? "R² = 0.7313 और MAE = 12.42 के साथ सतत स्वास्थ्य स्कोर (0-100)।"
                            : "Continuous Crop Health Score (0-100) with R² = 0.7313, MAE = 12.42.",
                  ),

                  // Practical 07
                  _buildPracticalRow(
                    code: "P07",
                    tech: "Decision Tree (CART) & k-NN (k=5)",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "فصل کے خطرے کی سطحوں (صحت مند، خطرے میں، تیز خطرہ) کی درجہ بندی۔"
                        : isHindi
                            ? "फसल जोखिम स्तरों (स्वस्थ, जोखिम में, उच्च जोखिम) का वर्गीकरण करता है।"
                            : "Classifies crop health status into categorical risk tiers (Healthy, At Risk, High Risk).",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "k-NN میں 88.33 فیصد اور ڈیسیژن ٹری میں 87.71 فیصد درستگی۔"
                        : isHindi
                            ? "k-NN में 88.33% और निर्णय वृक्ष (Decision Tree) में 87.71% सटीकता।"
                            : "88.33% k-NN accuracy and 87.71% Decision Tree classification accuracy.",
                  ),

                  // Practical 08
                  _buildPracticalRow(
                    code: "P08",
                    tech: "K-Means Clustering (k=3)",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "بغیر لیبل والے موسمی ڈیٹا کو 3 آب و ہوا کے تناؤ کے زونز میں تقسیم کرنا۔"
                        : isHindi
                            ? "बिना लेबल वाले मौसम डेटा को 3 सूक्ष्म-जलवायु तनाव क्षेत्रों में क्लस्टर करता है।"
                            : "Groups unlabeled environmental telemetry into latent stress vulnerability zones.",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "سلائیٹ سکور 0.297 کے ساتھ 3 الگ تھلگ آب و ہوا زونز کی دریافت۔"
                        : isHindi
                            ? "सिलहूट स्कोर 0.297 के साथ 3 अलग-अलग जलवायु जोखिम क्षेत्रों की खोज।"
                            : "3 distinct micro-climate vulnerability zones with Silhouette Score = 0.297.",
                  ),

                  // Practical 09
                  _buildPracticalRow(
                    code: "P09",
                    tech: "Domain-Specific NLP (TF-IDF)",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "بغیر کسی بیرونی LLM API کے کسانوں کے سوالات کو مقامی زرعی معلومات سے ملانا۔"
                        : isHindi
                            ? "बिना किसी बाहरी LLM API के किसान प्रश्नों को स्थानीय कृषि ज्ञानकोश से मिलाना।"
                            : "Matches farmer questions against Kaggle agricultural knowledge without external APIs.",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "100 فیصد مقامی، مفت اور درست کثیر لسانی (اردو، ہندی، انگریزی) کسان چیٹ باٹ۔"
                        : isHindi
                            ? "100% स्थानीय, मुफ्त और सटीक बहुभाषी (हिंदी, उर्दू, अंग्रेजी) किसान चैटबॉट।"
                            : "100% local, zero-cost, zero-hallucination farmer advisory chatbot in EN, HI, UR.",
                  ),

                  // Practical 10
                  _buildPracticalRow(
                    code: "P10",
                    tech: "Integrated Full-Stack Mini-Project",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "فلٹر ایپ، فاسٹ اے پی آئی بیک اینڈ اور سپا بیس ڈیٹا بیس کو آپس میں جوڑنا۔"
                        : isHindi
                            ? "फ्लटर ऐप, फ़ास्ट-एपीआई बैकएंड और सुपाबेस डेटाबेस को आपस में जोड़ना।"
                            : "Connects Flutter UI, FastAPI REST endpoints, Supabase RLS DB, and AI engines.",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "مکمل پروڈکشن گریڈ اینڈ ٹو اینڈ زرعی فیصلہ سازی کا موبائل سسٹم۔"
                        : isHindi
                            ? "पूर्ण उत्पादन-स्तरीय एंड-टू-एंड कृषि निर्णय सहायता मोबाइल प्रणाली।"
                            : "Production-grade end-to-end decision support application.",
                  ),

                  // Practical 11
                  _buildPracticalRow(
                    code: "P11",
                    tech: "Tabular Q-Learning (RL)",
                    actionHeader: actionHeading,
                    actionText: isUrdu
                        ? "27 سٹیٹ والے MDP ماحول میں بہترین آبپاشی اور کھاد کے کاموں کی حکمت عملی سیکھنا۔"
                        : isHindi
                            ? "27-अवस्था वाले MDP वातावरण में इष्टतम सिंचाई और खाद कार्यों की नीति सीखना।"
                            : "Learns optimal sequential irrigation and fertilizer actions in a 27-state MDP environment.",
                    resultHeader: resultHeading,
                    resultText: isUrdu
                        ? "30 دن کے سائیکل پر +33.78 اوسط انعام کی حکمت عملی کا حصول (Convergence)۔"
                        : isHindi
                            ? "30-दिवसीय फसल चक्र पर +33.78 औसत पुरस्कार पर नीति का अभिसरण (Convergence)।"
                            : "Policy convergence to +33.78 average reward over 30-day crop cycle.",
                  ),
                ],
              ),
            ),
            const SizedBox(height: 18),

            // Scientific Disclaimer Card
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFFFF3E0),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: const Color(0xFFFFB74D), width: 1.2),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.info_rounded, color: CropGuardTheme.warningOrange, size: 20),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      disclaimerText,
                      style: const TextStyle(fontSize: 12, color: CropGuardTheme.textPrimary, height: 1.35),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildLangChip(String langCode, String label) {
    final isSelected = _selectedLanguage == langCode;
    return GestureDetector(
      onTap: () {
        setState(() {
          _selectedLanguage = langCode;
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected ? CropGuardTheme.primary : Colors.transparent,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w700,
            color: isSelected ? Colors.white : CropGuardTheme.textSecondary,
          ),
        ),
      ),
    );
  }

  Widget _buildPracticalRow({
    required String code,
    required String tech,
    required String actionHeader,
    required String actionText,
    required String resultHeader,
    required String resultText,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: CropGuardTheme.background,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: CropGuardTheme.primary.withValues(alpha: 0.15), width: 1),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: CropGuardTheme.primary,
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    code,
                    style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w900, color: Colors.white),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    tech,
                    style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            RichText(
              text: TextSpan(
                style: const TextStyle(fontSize: 12, color: CropGuardTheme.textPrimary, height: 1.35),
                children: [
                  TextSpan(
                    text: "⚡ $actionHeader",
                    style: const TextStyle(fontWeight: FontWeight.bold, color: CropGuardTheme.primaryDark),
                  ),
                  TextSpan(text: actionText),
                ],
              ),
            ),
            const SizedBox(height: 4),
            RichText(
              text: TextSpan(
                style: const TextStyle(fontSize: 12, color: CropGuardTheme.textPrimary, height: 1.35),
                children: [
                  TextSpan(
                    text: "🎯 $resultHeader",
                    style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF2E7D32)),
                  ),
                  TextSpan(text: resultText),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
