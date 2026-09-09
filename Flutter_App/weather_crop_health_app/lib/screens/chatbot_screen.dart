import 'package:flutter/material.dart';
import '../theme.dart';
import '../models/chat_message_model.dart';
import '../models/prediction_model.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../widgets/logo_widget.dart';

class ChatbotScreen extends StatefulWidget {
  final String? activeCrop;
  final PredictionModel? currentPrediction;

  const ChatbotScreen({
    super.key,
    this.activeCrop,
    this.currentPrediction,
  });

  @override
  State<ChatbotScreen> createState() => _ChatbotScreenState();
}

class _ChatbotScreenState extends State<ChatbotScreen> {
  static const List<String> _englishQuestions = [
    "What about my rice field any precautions?",
    "Why is my crop at risk?",
    "What is the best temperature for wheat?",
    "What causes fungal disease?",
    "Why are my leaves turning yellow?",
    "When to spray pesticide or fungicide?",
    "How to use fertilizer properly?",
    "What precautions for tomato crop?",
  ];

  static const List<String> _hindiQuestions = [
    "धान की फसल के लिए क्या सावधानियां हैं?",
    "धान में कौन सी बीमारी लगती है?",
    "फसल को रोग का खतरा क्यों है?",
    "गेहूं की खेती के लिए सही तापमान क्या है?",
    "फफूंद रोग (Fungal disease) किस कारण होता है?",
    "पत्तियां पीली क्यों हो रही हैं?",
    "टमाटर की फसल में क्या सावधानी बरतें?",
    "कीटनाशक का छिड़काव कब करना चाहिए?",
    "खाद और उर्वरक का सही उपयोग कैसे करें?",
  ];

  static const List<String> _urduQuestions = [
    "دھان کی فصل کے لیے کیا احتیاطی تدابیر ہیں؟",
    "چاول میں کون سی بیماریاں لگتی ہیں؟",
    "فصل کو بیماری یا خطرہ کیوں ہوتا ہے؟",
    "گندم کی کاشت کے لیے بہترین درجہ حرارت کیا ہے؟",
    "پھپھوندی (Fungal disease) کی کیا وجوہات ہیں؟",
    "پتے پیلے کیوں پڑ رہے ہیں؟",
    "ٹماٹر کے پتے مڑ رہے ہیں کیا کریں؟",
    "کیڑے مار اور فنگس کش دوا کا اسپرے کب کریں؟",
    "کھاد اور یوریا کا صحیح استعمال کیسے کریں؟",
  ];

  final ApiService _apiService = ApiService();
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<ChatMessageModel> _messages = [];
  bool _isTyping = false;
  String _selectedLanguage = "auto";

  @override
  void initState() {
    super.initState();
    _initWelcomeMessage();
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  bool _isUrduText(String text) {
    return RegExp(r'[\u0600-\u06FF]').hasMatch(text);
  }

  void _initWelcomeMessage() {
    _messages.clear();
    final isHindi = _selectedLanguage == "hi";
    final isUrdu = _selectedLanguage == "ur";
    String welcome;
    if (isUrdu) {
      welcome = "خوش آمدید! میں **CropGuard AI معاون** ہوں، آپ کا مقامی زرعی اور موسمیاتی مشیر۔\n\n"
          "میں مکمل طور پر **مقامی زرعی NLP اور علمی بنیاد** پر کام کرتا ہوں (بغیر کسی بیرونی LLM یا API کے)۔\n\n"
          "آپ مجھ سے فصل کی موسمی مطابقت، بیماریوں، کھاد کے شیڈول، احتیاطی تدابیر یا نیچے دیے گئے موضوعات پر پوچھ سکتے ہیں۔";
      if (widget.currentPrediction != null) {
        final pred = widget.currentPrediction!;
        welcome += "\n\n🌱 *فصل:* **${pred.crop}** مقام **${pred.location}** (حالت: ${pred.healthStatus})۔";
      }
    } else if (isHindi) {
      welcome = "नमस्ते! मैं **CropGuard AI सहायक** हूँ, आपका स्थानीय कृषि और मौसम विशेषज्ञ।\n\n"
          "मैं पूरी तरह से **स्थानीय कृषि NLP इंजन** पर काम करता हूँ (शून्य बाहरी API या LLM)।\n\n"
          "आप मुझसे फसल की मौसम अनुकूलता, सावधानियां, रोग निवारण, खाद या नीचे दिए गए सुझावों के बारे में पूछ सकते हैं।";
      if (widget.currentPrediction != null) {
        final pred = widget.currentPrediction!;
        welcome += "\n\n🌱 *सक्रिय फसल:* **${pred.crop}** स्थान **${pred.location}** (स्थिति: ${pred.healthStatus})।";
      }
    } else {
      welcome = "Namaste! I am the **CropGuard AI Assistant**, your local agricultural & weather intelligence advisor.\n\n"
          "I run entirely on **our project's local NLP & reasoning engine** (zero external LLMs or third-party APIs).\n\n"
          "Ask me about crop requirements, weather risks, fungal prevention, fertilizers, precautions, or tap a suggested topic below.";
      if (widget.currentPrediction != null) {
        final pred = widget.currentPrediction!;
        welcome += "\n\n🌱 *Active Context:* **${pred.crop}** at **${pred.location}** (Status: ${pred.healthStatus}).";
      }
    }

    _messages.add(
      ChatMessageModel.bot(
        message: welcome,
        confidence: 1.0,
        matchedTopic: "greeting_welcome",
      ),
    );
  }

  void _changeLanguage(String lang) {
    if (_selectedLanguage == lang) return;
    setState(() {
      _selectedLanguage = lang;
      _initWelcomeMessage();
    });
  }

  Future<void> _sendMessage(String text) async {
    final query = text.trim();
    if (query.isEmpty) return;

    _textController.clear();
    setState(() {
      _messages.add(ChatMessageModel.user(query));
      _isTyping = true;
    });
    _scrollToBottom();

    final botReply = await _apiService.sendChatMessage(
      message: query,
      crop: widget.activeCrop ?? widget.currentPrediction?.crop,
      currentPrediction: widget.currentPrediction,
      userId: AuthService().currentUser?.id,
      language: _selectedLanguage,
    );

    if (mounted) {
      setState(() {
        _isTyping = false;
        _messages.add(botReply);
      });
      _scrollToBottom();
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final isHindi = _selectedLanguage == "hi";
    final isUrdu = _selectedLanguage == "ur";
    final List<String> suggestedQuestions = isUrdu
        ? _urduQuestions
        : (isHindi ? _hindiQuestions : _englishQuestions);

    String langLabel;
    if (_selectedLanguage == "ur") {
      langLabel = "اردو";
    } else if (_selectedLanguage == "hi") {
      langLabel = "हिंदी";
    } else if (_selectedLanguage == "en") {
      langLabel = "EN";
    } else {
      langLabel = "Auto";
    }

    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(
        titleSpacing: 0,
        title: Row(
          children: [
            const CropGuardLogo(size: 28, showText: false),
            const SizedBox(width: 8),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    "CropGuard AI Assistant",
                    style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                    overflow: TextOverflow.ellipsis,
                  ),
                  Text(
                    "Local Domain NLP • Zero LLMs",
                    style: TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.w600,
                      color: CropGuardTheme.primary.withValues(alpha: 0.85),
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
          ],
        ),
        actions: [
          // Language Switcher Badge / Menu
          Padding(
            padding: const EdgeInsets.only(right: 8),
            child: PopupMenuButton<String>(
              icon: Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: CropGuardTheme.primary.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: CropGuardTheme.primary.withValues(alpha: 0.3)),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.language_rounded, size: 15, color: CropGuardTheme.primaryDark),
                    const SizedBox(width: 4),
                    Text(
                      langLabel,
                      style: const TextStyle(fontSize: 11.5, fontWeight: FontWeight.bold, color: CropGuardTheme.primaryDark),
                    ),
                  ],
                ),
              ),
              onSelected: _changeLanguage,
              itemBuilder: (context) => const [
                PopupMenuItem(
                  value: "auto",
                  child: Text("Auto-detect"),
                ),
                PopupMenuItem(
                  value: "en",
                  child: Text("English"),
                ),
                PopupMenuItem(
                  value: "hi",
                  child: Text("हिंदी"),
                ),
                PopupMenuItem(
                  value: "ur",
                  child: Text("اردو"),
                ),
              ],
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          // Active Prediction Context Banner (Responsive on mobile)
          if (widget.currentPrediction != null)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              color: const Color(0xFFE8F5E9),
              child: Row(
                children: [
                  const Icon(Icons.eco_rounded, color: CropGuardTheme.primary, size: 18),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      "Context: ${widget.currentPrediction!.crop} (${widget.currentPrediction!.healthStatus}) • ${widget.currentPrediction!.weather.temperature.toInt()}°C, ${widget.currentPrediction!.weather.humidity.toInt()}% RH",
                      style: const TextStyle(fontSize: 11.5, fontWeight: FontWeight.w600, color: CropGuardTheme.primaryDark),
                      overflow: TextOverflow.ellipsis,
                      maxLines: 2,
                    ),
                  ),
                ],
              ),
            ),

          // Messages List
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                if (index < 0 || index >= _messages.length) return const SizedBox.shrink();
                final msg = _messages[index];
                return _buildMessageBubble(msg);
              },
            ),
          ),

          // Typing Indicator
          if (_isTyping)
            Padding(
              padding: const EdgeInsets.only(left: 16, right: 16, bottom: 6),
              child: Row(
                children: [
                  const SizedBox(
                    width: 14,
                    height: 14,
                    child: CircularProgressIndicator(strokeWidth: 2, color: CropGuardTheme.primary),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      isUrdu
                          ? "CropGuard AI تجزیہ کر رہا ہے..."
                          : (isHindi
                              ? "CropGuard AI विश्लेषण कर रहा है..."
                              : "CropGuard AI is reasoning over local rules..."),
                      style: TextStyle(fontSize: 11.5, color: CropGuardTheme.textSecondary.withValues(alpha: 0.85)),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
            ),

          // Suggested Question Chips
          Container(
            height: 38,
            margin: const EdgeInsets.only(bottom: 6),
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 12),
              itemCount: suggestedQuestions.length,
              itemBuilder: (context, index) {
                if (index < 0 || index >= suggestedQuestions.length) return const SizedBox.shrink();
                final q = suggestedQuestions[index];
                return Padding(
                  padding: const EdgeInsets.only(right: 6),
                  child: ActionChip(
                    label: Text(q),
                    padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 0),
                    backgroundColor: Colors.white,
                    side: const BorderSide(color: CropGuardTheme.border, width: 1.1),
                    labelStyle: const TextStyle(fontSize: 11.5, color: CropGuardTheme.primaryDark, fontWeight: FontWeight.w600),
                    onPressed: () => _sendMessage(q),
                  ),
                );
              },
            ),
          ),

          // Input Bar (Mobile Responsive & Keyboard Safe)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: const BoxDecoration(
              color: Colors.white,
              border: Border(top: BorderSide(color: CropGuardTheme.border)),
            ),
            child: SafeArea(
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _textController,
                      textDirection: isUrdu ? TextDirection.rtl : TextDirection.ltr,
                      style: const TextStyle(fontSize: 13.5),
                      decoration: InputDecoration(
                        hintText: isUrdu
                            ? "زرعی یا موسمیاتی سوال پوچھیں..."
                            : (isHindi
                                ? "कृषि या मौसम संबंधी प्रश्न पूछें..."
                                : "Ask an agricultural or weather question..."),
                        hintStyle: const TextStyle(fontSize: 12.5),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                      ),
                      onSubmitted: _sendMessage,
                    ),
                  ),
                  const SizedBox(width: 8),
                  CircleAvatar(
                    radius: 20,
                    backgroundColor: CropGuardTheme.primary,
                    child: IconButton(
                      padding: EdgeInsets.zero,
                      icon: const Icon(Icons.send_rounded, color: Colors.white, size: 18),
                      onPressed: () => _sendMessage(_textController.text),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(ChatMessageModel message) {
    final isUser = message.isUser;
    final isUrdu = _isUrduText(message.text);
    final isHindi = _selectedLanguage == "hi" || RegExp(r'[\u0900-\u097F]').hasMatch(message.text);
    final screenWidth = MediaQuery.of(context).size.width;
    final maxBubbleWidth = screenWidth < 600 ? screenWidth * 0.88 : 550.0;

    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 10),
        constraints: BoxConstraints(maxWidth: maxBubbleWidth),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        decoration: BoxDecoration(
          color: isUser ? CropGuardTheme.primary : Colors.white,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(isUser ? 16 : 4),
            bottomRight: Radius.circular(isUser ? 4 : 16),
          ),
          border: isUser ? null : Border.all(color: CropGuardTheme.border, width: 1.1),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.04),
              blurRadius: 6,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: isUser ? CrossAxisAlignment.end : (isUrdu ? CrossAxisAlignment.end : CrossAxisAlignment.start),
          children: [
            SelectableText(
              message.text,
              textDirection: isUrdu ? TextDirection.rtl : TextDirection.ltr,
              style: TextStyle(
                fontSize: 13.5,
                color: isUser ? Colors.white : CropGuardTheme.textPrimary,
                height: 1.45,
                fontWeight: isUser ? FontWeight.w500 : FontWeight.normal,
              ),
            ),
            if (!isUser && message.confidence != null && message.confidence! > 0) ...[
              const SizedBox(height: 6),
              Row(
                mainAxisSize: MainAxisSize.min,
                textDirection: isUrdu ? TextDirection.rtl : TextDirection.ltr,
                children: [
                  Icon(Icons.verified_outlined, size: 12, color: CropGuardTheme.primary.withValues(alpha: 0.8)),
                  const SizedBox(width: 4),
                  Text(
                    isUrdu
                        ? "مقامی تصدیق: ${(message.confidence! * 100).toInt()}%"
                        : (isHindi
                            ? "सटीकता: ${(message.confidence! * 100).toInt()}%"
                            : "Match Confidence: ${(message.confidence! * 100).toInt()}%"),
                    style: TextStyle(
                      fontSize: 10,
                      color: CropGuardTheme.textSecondary.withValues(alpha: 0.85),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }
}
