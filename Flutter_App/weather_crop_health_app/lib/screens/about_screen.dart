import 'package:flutter/material.dart';
import '../theme.dart';
import '../widgets/logo_widget.dart';
import '../services/language_service.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<String>(
      valueListenable: LanguageService(),
      builder: (context, currentLang, _) {
        final isHindi = currentLang == "hi";
        final isUrdu = currentLang == "ur";

        final titleText = isUrdu
            ? "پراجیکٹ اور AI پریکٹیکلز کی تفصیل"
            : isHindi
                ? "परियोजना और AI लैब प्रैक्टिकल विवरण"
                : "About Project & AI Practicals";

        final overviewTitle = isUrdu
            ? "CropGuard AI پراجیکٹ کا مقصد"
            : isHindi
                ? "CropGuard AI परियोजना का उद्देश्य"
                : "CropGuard AI System Architecture";

        final overviewBody = isUrdu
            ? "یہ ایپلی کیشن 11 مصنوعی ذہانت (AI) لیب پریکٹیکلز کو ایک مکمل زرعی فیصلے کے نظام میں جوڑتی ہے۔ ذیل میں ہر پریکٹیکل کا استعمال اور اس کا حاصل شدہ نتیجہ آسان الفاظ میں دیا گیا ہے۔"
            : isHindi
                ? "यह एप्लिकेशन 11 आर्टिफिशियल इंटेलिजेंस (AI) लैब प्रैक्टिकल को एक पूर्ण कृषि निर्णय प्रणाली में एकीकृत करता है। नीचे प्रत्येक प्रैक्टिकल का उपयोग और उसका परिणाम सरल भाषा में दिया गया है।"
                : "CropGuard AI combines all 11 Artificial Intelligence Laboratory Practicals into a single agricultural decision support app. Below is the simple, clear explanation of WHERE and HOW each practical is used in this project.";

        final practicalsTitle = isUrdu
            ? "11 تمام AI پریکٹیکلز کا استعمال اور نتائج"
            : isHindi
                ? "सभी 11 AI प्रैक्टिकल का उपयोग और परिणाम"
                : "Where & How All 11 AI Practicals Are Used";

        final usageHeading = isUrdu ? "کہاں اور کیسے استعمال ہوتا ہے: " : isHindi ? "कहाँ और कैसे उपयोग होता है: " : "Where & How Used: ";
        final resultHeading = isUrdu ? "حاصل شدہ نتیجہ: " : isHindi ? "प्राप्त परिणाम: " : "Result Achieved: ";

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

                // Language Selector (Clean labels without flags)
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
                      _buildLangChip("en", "English", currentLang),
                      _buildLangChip("hi", "हिंदी", currentLang),
                      _buildLangChip("ur", "اردو", currentLang),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                // System Overview Card
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

                // All 11 Practicals Card
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
                      _buildPracticalCard(
                        code: "P01",
                        title: "Data Preprocessing & Correlation",
                        tech: "NumPy, Pandas & Matplotlib",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "موسمیاتی اور فصل سینسر ڈیٹا کی صفائی اور درجہ حرارت، نمی اور بارش کے درمیان تعلّق (Correlation) کا حساب لگانے کے لیے استعمال ہوتا ہے۔"
                            : isHindi
                                ? "मौसम और फसल सेंसर डेटा की सफाई और तापमान, आर्द्रता और वर्षा के बीच संबंध (Correlation) की गणना के लिए उपयोग किया जाता है।"
                                : "Used in the Data Engineering Pipeline to clean raw weather telemetry and calculate correlation matrices between heat, humidity, and rainfall.",
                        resultHeader: resultHeading,
                        resultText: isUrdu
                            ? "صاف ستھرا ڈیٹا بیس اور 4-پینل ویژولائزیشن ہیٹ میپ چارٹ۔"
                            : isHindi
                                ? "स्वच्छ डेटाबेस और 4-पैनल दृश्य सहसंबंध हीटमैप चार्ट।"
                                : "Cleaned agricultural dataset & 4-panel telemetry correlation heatmap chart.",
                      ),

                      // Practical 02
                      _buildPracticalCard(
                        code: "P02",
                        title: "Uninformed Graph Search",
                        tech: "BFS (Breadth-First) & DFS (Depth-First)",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "فصل کے خطرے کی ممکنہ حالتوں کو لیول بہ لیول (BFS) اور گہرائی (DFS) میں بغیر کسی اندازے کے تلاش کرنے کے لیے استعمال ہوتا ہے۔"
                            : isHindi
                                ? "फसल जोखिम की संभावित अवस्थाओं को स्तर-दर-स्तर (BFS) और गहराई (DFS) में बिना किसी अनुमान के खोजने के लिए उपयोग किया जाता है।"
                                : "Used in the Risk State Exploration Engine to traverse agricultural condition trees level-by-level (BFS) and branch-by-branch (DFS).",
                        resultHeader: resultHeading,
                        resultText: isUrdu
                            ? "بغیر کسی گائیڈ کے سٹیٹ اسپیس روٹ (State-Space Path) کی مکمل دریافت۔"
                            : isHindi
                                ? "बिना किसी अनुमानी मार्गदर्शन के संपूर्ण अवस्था-स्थान पथ खोज (State-Space Discovery)।"
                                : "Complete state-space vulnerability path discovery without heuristic guidance.",
                      ),

                      // Practical 03
                      _buildPracticalCard(
                        code: "P03",
                        title: "Informed Heuristic Search",
                        tech: "Greedy Best-First (GBFS) & A* Search",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "آبپاشی، چھاؤں اور ادویات کا کم ترین لاگت والا بہترین امتزاج f(n) = g(n) + h(n) سے تلاش کرنے کے لیے استعمال ہوتا ہے۔"
                            : isHindi
                                ? "सिंचाई, छाया और दवा के सबसे कम लागत वाले संयोजन को f(n) = g(n) + h(n) से खोजने के लिए उपयोग किया जाता है।"
                                : "Used in the Remediation Cost Planner to find the optimal sequence of interventions (watering + shading) with minimal resource cost f(n)=g(n)+h(n).",
                        resultHeader: resultHeading,
                        resultText: isUrdu
                            ? "35 فیصد کم وسائل کی لاگت کے ساتھ علاج کے بہترین مراحل۔"
                            : isHindi
                                ? "35% कम संसाधन लागत के साथ इष्टतम उपचारात्मक कदम।"
                                : "Optimal intervention sequence saving 35% resource expenditure.",
                      ),

                      // Practical 04
                      _buildPracticalCard(
                        code: "P04",
                        title: "Local Search Optimization",
                        tech: "Hill Climbing & Simulated Annealing",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "شدید گرمی میں میٹروپولیس قانون (P = e^(ΔE/T)) کا استعمال کر کے آبپاشی (mm/day) اور چھاؤں (%) کا بہترین توازن بنانے کے لیے استعمال ہوتا ہے۔"
                            : isHindi
                                ? "अत्यधिक गर्मी में मेट्रोपोलिस मानदंड (P = e^(ΔE/T)) का उपयोग करके सिंचाई (mm/day) और छाया (%) का सर्वोत्तम संतुलन बनाने के लिए उपयोग किया जाता है।"
                                : "Used in the Microclimate Optimization Engine using Metropolis cooling criterion P = exp(ΔE / T) to dynamically balance continuous irrigation and shading.",
                        resultHeader: resultHeading,
                        resultText: isUrdu
                            ? "99.98 / 100 کا عالمی فصل سکور (مقامی غلط جال سے نجات)۔"
                            : isHindi
                                ? "99.98 / 100 का वैश्विक फसल आराम स्कोर (स्थानीय जाल से मुक्ति)।"
                                : "Global physiological crop comfort score of 99.98 / 100 (escaping local optima traps).",
                      ),

                      // Practical 05
                      _buildPracticalCard(
                        code: "P05",
                        title: "Expert Reasoning & XAI Proofs",
                        tech: "Forward & Backward Chaining",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "فارورڈ چیننگ سے موسمی ڈیٹا دیکھ کر بیماری کی وجہ معلوم کرنے اور بیک ورڈ چیننگ سے اس کا ثبوت دینے کے لیے استعمال ہوتا ہے۔"
                            : isHindi
                                ? "फॉरवर्ड चेनिंग से मौसम डेटा देखकर बीमारी का कारण बताने और बैकवर्ड चेनिंग से उसका प्रमाण देने के लिए उपयोग किया जाता है।"
                                : "Used in the Expert Reasoning Engine: Forward Chaining deduces disease causes from weather observations, and Backward Chaining generates Explainable AI (XAI) proofs.",
                        resultHeader: resultHeading,
                        resultText: isUrdu
                            ? "واضح بیماری کی تشخیص اور قابل تصدیق XAI ثبوت کا راستہ۔"
                            : isHindi
                                ? "स्पष्ट रोग निदान और सत्यापित करने योग्य व्याख्यात्मक AI (XAI) प्रमाण।"
                                : "Deductive etiology diagnosis + verifiable Explainable AI (XAI) proof trace.",
                      ),

                      // Practical 06
                      _buildPracticalCard(
                        code: "P06",
                        title: "Continuous Health Prediction",
                        tech: "Multiple Linear Regression",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "درجہ حرارت، نمی اور بارش کے اعدادی اعداد و شمار پر گنتی کر کے فصل کا مسلسل صحت کا سکور (0 سے 100) بتانے کے لیے استعمال ہوتا ہے۔"
                            : isHindi
                                ? "तापमान, आर्द्रता और वर्षा के आंकड़ों की गणना करके फसल का निरंतर स्वास्थ्य स्कोर (0 से 100) बताने के लिए उपयोग किया जाता है।"
                                : "Used in the Continuous Prediction Module to fit linear parameters over weather metrics and output a continuous Crop Health Score (0.0 to 100.0).",
                        resultHeader: resultHeading,
                        resultText: isUrdu
                            ? "R² = 0.7313 اور MAE = 12.42 کے ساتھ فصل کا ہیلتھ سکور۔"
                            : isHindi
                                ? "R² = 0.7313 और MAE = 12.42 के साथ निरंतर फसल स्वास्थ्य स्कोर।"
                                : "Continuous Crop Health Score (0-100) with R² = 0.7313, MAE = 12.42.",
                      ),

                      // Practical 07
                      _buildPracticalCard(
                        code: "P07",
                        title: "Supervised Risk Classification",
                        tech: "Decision Tree (CART) & k-NN (k=5)",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "فصل کے خطرے کو تین حصوں (صحت مند، خطرے میں، شدید خطرہ) میں تقسیم کرنے کے لیے استعمال ہوتا ہے۔"
                            : isHindi
                                ? "फसल के जोखिम को तीन श्रेणियों (स्वस्थ, जोखिम में, उच्च जोखिम) में वर्गीकृत करने के लिए उपयोग किया जाता है।"
                                : "Used in the Classification Engine to categorize farms into operational risk status tiers (Healthy, At Risk, High Risk).",
                        resultHeader: resultHeading,
                        resultText: isUrdu
                            ? "k-NN میں 88.33 فیصد اور ڈیسیژن ٹری میں 87.71 فیصد درستگی۔"
                            : isHindi
                                ? "k-NN में 88.33% और निर्णय वृक्ष में 87.71% वर्गीकरण सटीकता।"
                                : "88.33% k-NN accuracy and 87.71% Decision Tree classification accuracy.",
                      ),

                      // Practical 08
                      _buildPracticalCard(
                        code: "P08",
                        title: "Unsupervised Climate Zoning",
                        tech: "K-Means Clustering (k=3)",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "بغیر نام والے موسمی ڈیٹا کو 3 آب و ہوا کے خطرے کے زونز میں گروپ کرنے کے لیے استعمال ہوتا ہے۔"
                            : isHindi
                                ? "बिना नाम वाले मौसम डेटा को 3 जलवायु जोखिम क्षेत्रों में समूहित करने के लिए उपयोग किया जाता है।"
                                : "Used in the Agro-Climatic Zoning Engine to group unlabeled environmental telemetry into 3 micro-climate vulnerability clusters.",
                        resultHeader: resultHeading,
                        resultText: isUrdu
                            ? "سلائیٹ سکور 0.297 کے ساتھ 3 مختلف آب و ہوا زونز۔"
                            : isHindi
                                ? "सिलहूट स्कोर 0.297 के साथ 3 अलग-अलग जलवायु जोखिम क्षेत्र।"
                                : "3 distinct micro-climate vulnerability zones with Silhouette Score = 0.297.",
                      ),

                      // Practical 09
                      _buildPracticalCard(
                        code: "P09",
                        title: "Local Farmer AI Chatbot",
                        tech: "Domain-Specific NLP (TF-IDF)",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "کسانوں کے سوالات کے جوابات مقامی زرعی ڈیٹا سے دینے کے لیے استعمال ہوتا ہے (بغیر کسی بیرونی API کے)۔"
                            : isHindi
                                ? "किसानों के प्रश्नों का उत्तर स्थानीय कृषि डेटा से देने के लिए उपयोग किया जाता है (बिना किसी बाहरी API के)।"
                                : "Used in the Local Farmer Chatbot Screen to match user questions against Kaggle agricultural knowledge using TF-IDF vectorization and cosine similarity.",
                        resultHeader: resultHeading,
                        resultText: isUrdu
                            ? "100 فیصد مقامی، مفت اور درست کثیر لسانی کسان چیٹ باٹ۔"
                            : isHindi
                                ? "100% स्थानीय, मुफ्त और सटीक बहुभाषी (हिंदी, उर्दू, अंग्रेजी) किसान चैटबॉट।"
                                : "100% local, zero-cost, zero-hallucination farmer advisory chatbot in EN, HI, UR.",
                      ),

                      // Practical 10
                      _buildPracticalCard(
                        code: "P10",
                        title: "Full-Stack Application Integration",
                        tech: "Flutter App + FastAPI + Supabase RLS",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "فلٹر موبائل ایپ، فاسٹ اے پی آئی سرور اور سپا بیس ڈیٹا بیس کو آپس میں جوڑ کر مکمل سسٹم بنانے کے لیے استعمال ہوتا ہے۔"
                            : isHindi
                                ? "फ्लटर मोबाइल ऐप, फ़ास्ट-एपीआई सर्वर और सुपाबेस डेटाबेस को आपस में जोड़कर पूर्ण सिस्टम बनाने के लिए उपयोग किया जाता है।"
                                : "Used as the Core System Integrator connecting the Flutter mobile UI, FastAPI REST server, Supabase RLS PostgreSQL database, and AI engines into one app.",
                        resultHeader: resultHeading,
                        resultText: isUrdu
                            ? "مکمل پروڈکشن گریڈ اینڈ ٹو اینڈ زرعی فیصلے کا موبائل سسٹم۔"
                            : isHindi
                                ? "पूर्ण उत्पादन-स्तरीय एंड-टू-एंड कृषि निर्णय सहायता मोबाइल प्रणाली।"
                                : "Production-grade end-to-end decision support application.",
                      ),

                      // Practical 11
                      _buildPracticalCard(
                        code: "P11",
                        title: "Sequential Irrigation RL Agent",
                        tech: "Tabular Q-Learning (RL)",
                        usageHeader: usageHeading,
                        usageText: isUrdu
                            ? "30 دن کے فصل سائیکل میں پانی اور کھاد دینے کے بہترین فیصلوں کی حکمت عملی سیکھنے کے لیے استعمال ہوتا ہے۔"
                            : isHindi
                                ? "30-दिवसीय फसल चक्र में पानी और खाद देने के सर्वोत्तम निर्णयों की नीति सीखने के लिए उपयोग किया जाता है।"
                                : "Used in the Sequential Resource Allocation Engine to learn optimal daily watering and fertilizing actions over a 30-day crop cycle using Q-Learning MDP.",
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

                // Scientific Disclaimer
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
      },
    );
  }

  Widget _buildLangChip(String langCode, String label, String currentLang) {
    final isSelected = currentLang == langCode;
    return GestureDetector(
      onTap: () {
        LanguageService().setLanguage(langCode);
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
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

  Widget _buildPracticalCard({
    required String code,
    required String title,
    required String tech,
    required String usageHeader,
    required String usageText,
    required String resultHeader,
    required String resultText,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: CropGuardTheme.background,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: CropGuardTheme.primary.withValues(alpha: 0.2), width: 1),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
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
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: const TextStyle(fontSize: 13.5, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                      ),
                      Text(
                        tech,
                        style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: CropGuardTheme.primaryDark),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            RichText(
              text: TextSpan(
                style: const TextStyle(fontSize: 12, color: CropGuardTheme.textPrimary, height: 1.4),
                children: [
                  TextSpan(
                    text: "📍 $usageHeader",
                    style: const TextStyle(fontWeight: FontWeight.bold, color: CropGuardTheme.primaryDark),
                  ),
                  TextSpan(text: usageText),
                ],
              ),
            ),
            const SizedBox(height: 6),
            RichText(
              text: TextSpan(
                style: const TextStyle(fontSize: 12, color: CropGuardTheme.textPrimary, height: 1.4),
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
