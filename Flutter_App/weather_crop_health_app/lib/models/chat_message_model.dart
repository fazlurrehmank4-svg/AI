class ChatMessageModel {
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final double? confidence;
  final String? matchedTopic;
  final String? category;
  final String? reasoningSummary;

  ChatMessageModel({
    required this.text,
    required this.isUser,
    required this.timestamp,
    this.confidence,
    this.matchedTopic,
    this.category,
    this.reasoningSummary,
  });

  factory ChatMessageModel.user(String message) {
    return ChatMessageModel(
      text: message,
      isUser: true,
      timestamp: DateTime.now(),
    );
  }

  factory ChatMessageModel.bot({
    required String message,
    double? confidence,
    String? matchedTopic,
    String? category,
    String? reasoningSummary,
  }) {
    return ChatMessageModel(
      text: message,
      isUser: false,
      timestamp: DateTime.now(),
      confidence: confidence,
      matchedTopic: matchedTopic,
      category: category,
      reasoningSummary: reasoningSummary,
    );
  }
}
