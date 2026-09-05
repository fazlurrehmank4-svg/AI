import 'package:flutter/material.dart';
import '../theme.dart';
import '../models/chat_message_model.dart';
import '../models/prediction_model.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';

class ChatbotScreen extends StatefulWidget {
  final String? activeCrop;
  final PredictionModel? currentPrediction;

  const ChatbotScreen({
    Key? key,
    this.activeCrop,
    this.currentPrediction,
  }) : super(key: key);

  @override
  State<ChatbotScreen> createState() => _ChatbotScreenState();
}

class _ChatbotScreenState extends State<ChatbotScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<ChatMessageModel> _messages = [];
  bool _isTyping = false;

  final List<String> _suggestedQuestions = [
    "What should I do?",
    "Why is my crop at risk?",
    "What is the best temperature for wheat?",
    "What causes fungal disease?",
    "What happens if humidity is too high?",
    "Why are my leaves turning yellow?",
  ];

  @override
  void initState() {
    super.initState();
    _initWelcomeMessage();
  }

  void _initWelcomeMessage() {
    String welcome = "Namaste! I am the **CropGuard AI Assistant**, your local agricultural intelligence advisor.\n\n"
        "I run entirely on **our project's local NLP & reasoning engine** (zero external LLMs or third-party APIs).\n\n"
        "Ask me about crop requirements, weather risks, fungal prevention, or tap a suggested topic below.";

    if (widget.currentPrediction != null) {
      welcome += "\n\n🌱 *Active Context:* **${widget.currentPrediction!.crop}** at **${widget.currentPrediction!.location}** (Status: ${widget.currentPrediction!.healthStatus}).";
    }

    _messages.add(
      ChatMessageModel.bot(
        message: welcome,
        confidence: 1.0,
        matchedTopic: "greeting_welcome",
      ),
    );
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
    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(
        title: Column(
          children: [
            const Text("CropGuard AI Assistant"),
            Text(
              "Local Domain NLP • Zero External LLMs",
              style: TextStyle(fontSize: 10, fontWeight: FontWeight.w600, color: CropGuardTheme.primary.withOpacity(0.85)),
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          // Active Prediction Context Banner (if available)
          if (widget.currentPrediction != null)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              color: const Color(0xFFE8F5E9),
              child: Row(
                children: [
                  const Icon(Icons.eco_rounded, color: CropGuardTheme.primary, size: 18),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      "Context: ${widget.currentPrediction!.crop} (${widget.currentPrediction!.healthStatus}) • ${widget.currentPrediction!.weather.temperature.toInt()}°C, ${widget.currentPrediction!.weather.humidity.toInt()}% RH",
                      style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: CropGuardTheme.primaryDark),
                    ),
                  ),
                ],
              ),
            ),

          // Messages List
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                return _buildMessageBubble(msg);
              },
            ),
          ),

          // Typing Indicator
          if (_isTyping)
            Padding(
              padding: const EdgeInsets.only(left: 20, bottom: 8),
              child: Row(
                children: [
                  const SizedBox(
                    width: 14,
                    height: 14,
                    child: CircularProgressIndicator(strokeWidth: 2, color: CropGuardTheme.primary),
                  ),
                  const SizedBox(width: 10),
                  Text(
                    "CropGuard AI is reasoning over local agricultural rules...",
                    style: TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary.withOpacity(0.8)),
                  ),
                ],
              ),
            ),

          // Suggested Question Chips
          Container(
            height: 42,
            margin: const EdgeInsets.only(bottom: 6),
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 12),
              itemCount: _suggestedQuestions.length,
              itemBuilder: (context, index) {
                final q = _suggestedQuestions[index];
                return Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: ActionChip(
                    label: Text(q),
                    backgroundColor: Colors.white,
                    side: const BorderSide(color: CropGuardTheme.border, width: 1.2),
                    labelStyle: const TextStyle(fontSize: 12, color: CropGuardTheme.primaryDark, fontWeight: FontWeight.w500),
                    onPressed: () => _sendMessage(q),
                  ),
                );
              },
            ),
          ),

          // Input Bar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
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
                      decoration: const InputDecoration(
                        hintText: "Ask an agricultural question...",
                        contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                      ),
                      onSubmitted: _sendMessage,
                    ),
                  ),
                  const SizedBox(width: 10),
                  CircleAvatar(
                    backgroundColor: CropGuardTheme.primary,
                    child: IconButton(
                      icon: const Icon(Icons.send_rounded, color: Colors.white, size: 20),
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
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.82),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        decoration: BoxDecoration(
          color: isUser ? CropGuardTheme.primary : Colors.white,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(isUser ? 16 : 4),
            bottomRight: Radius.circular(isUser ? 4 : 16),
          ),
          border: isUser ? null : Border.all(color: CropGuardTheme.border, width: 1.2),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.03),
              blurRadius: 6,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
          children: [
            Text(
              message.text,
              style: TextStyle(
                fontSize: 14,
                color: isUser ? Colors.white : CropGuardTheme.textPrimary,
                height: 1.4,
              ),
            ),
            if (!isUser && message.confidence != null && message.confidence! > 0) ...[
              const SizedBox(height: 8),
              Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.verified_outlined, size: 12, color: CropGuardTheme.primary.withOpacity(0.7)),
                  const SizedBox(width: 4),
                  Text(
                    "Local Match Confidence: ${(message.confidence! * 100).toInt()}%",
                    style: TextStyle(fontSize: 10, color: CropGuardTheme.textSecondary.withOpacity(0.8), fontWeight: FontWeight.w600),
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
