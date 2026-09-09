import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../theme.dart';
import '../models/prediction_model.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../services/language_service.dart';
import '../widgets/risk_badge.dart';
import 'prediction_screen.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  final ApiService _apiService = ApiService();
  List<PredictionModel> _history = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    setState(() => _isLoading = true);
    final user = AuthService().currentUser;
    final list = await _apiService.fetchHistory(
      userId: user?.id ?? "guest-farmer",
      token: AuthService().authToken,
    );

    if (mounted) {
      setState(() {
        _history = list;
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final dateFormat = DateFormat('MMM dd, yyyy • hh:mm a');

    return ValueListenableBuilder<String>(
      valueListenable: LanguageService(),
      builder: (context, currentLang, _) {
        return Scaffold(
          backgroundColor: CropGuardTheme.background,
          appBar: AppBar(
            title: Text(LanguageService().drawerHistory),
            actions: [
              IconButton(icon: const Icon(Icons.refresh_rounded), onPressed: _loadHistory),
            ],
          ),
          body: _isLoading
              ? const Center(child: CircularProgressIndicator(color: CropGuardTheme.primary))
              : _history.isEmpty
                  ? _buildEmptyState()
                  : ListView.builder(
                      padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
                      itemCount: _history.length,
                      itemBuilder: (context, index) {
                        final item = _history[index];
                        final translatedCrop = LanguageService().getCropName(item.crop);
                        final translatedLoc = LanguageService().getLocationName(item.location);

                        return Container(
                          margin: const EdgeInsets.only(bottom: 14),
                          decoration: CropGuardTheme.cardDecoration,
                          child: InkWell(
                            borderRadius: BorderRadius.circular(18),
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (_) => PredictionScreen(prediction: item)),
                              );
                            },
                            child: Padding(
                              padding: const EdgeInsets.all(16),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Row(
                                        children: [
                                          const Icon(Icons.eco_outlined, color: CropGuardTheme.primary, size: 20),
                                          const SizedBox(width: 8),
                                          Text(
                                            translatedCrop,
                                            style: const TextStyle(
                                              fontSize: 16,
                                              fontWeight: FontWeight.w800,
                                              color: CropGuardTheme.textPrimary,
                                            ),
                                          ),
                                        ],
                                      ),
                                      RiskBadge(status: item.healthStatus, riskLevel: item.riskLevel),
                                    ],
                                  ),
                                  const SizedBox(height: 8),
                                  Text(
                                    "$translatedLoc • Score: ${item.cropHealthScore.toInt()}/100",
                                    style: const TextStyle(fontSize: 13, color: CropGuardTheme.textSecondary, fontWeight: FontWeight.w500),
                                    overflow: TextOverflow.ellipsis,
                                    maxLines: 1,
                                  ),
                                  const SizedBox(height: 6),
                                  Text(
                                    dateFormat.format(item.timestamp),
                                    style: const TextStyle(fontSize: 11, color: CropGuardTheme.textLight),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        );
                      },
                    ),
        );
      },
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.history_toggle_off_rounded, size: 64, color: CropGuardTheme.textLight.withValues(alpha: 0.5)),
          const SizedBox(height: 16),
          const Text(
            "No Predictions Recorded Yet",
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: CropGuardTheme.textPrimary),
          ),
          const SizedBox(height: 6),
          const Text(
            "Run your first crop health prediction from the dashboard.",
            style: TextStyle(fontSize: 13, color: CropGuardTheme.textSecondary),
          ),
        ],
      ),
    );
  }
}
