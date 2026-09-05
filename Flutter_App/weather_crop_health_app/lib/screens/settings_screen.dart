import 'package:flutter/material.dart';
import '../theme.dart';
import '../services/api_service.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final ApiService _apiService = ApiService();
  late TextEditingController _urlController;

  @override
  void initState() {
    super.initState();
    _urlController = TextEditingController(text: _apiService.baseUrl);
  }

  void _saveUrl(String url) async {
    await _apiService.setBaseUrl(url);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Backend URL set to: $url")),
      );
      setState(() {});
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(title: const Text("Application Settings")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Backend Connectivity Card
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    children: [
                      Icon(Icons.dns_rounded, color: CropGuardTheme.primary, size: 22),
                      SizedBox(width: 10),
                      Text(
                        "FastAPI Backend Endpoint",
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    "Configure the active server endpoint for ML inference and local chatbot retrieval.",
                    style: TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _urlController,
                    decoration: InputDecoration(
                      labelText: "Backend Base URL",
                      suffixIcon: IconButton(
                        icon: const Icon(Icons.check, color: CropGuardTheme.primary),
                        onPressed: () => _saveUrl(_urlController.text),
                      ),
                    ),
                  ),
                  const SizedBox(height: 14),
                  const Text("Quick Presets:", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: CropGuardTheme.textSecondary)),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      ActionChip(
                        label: const Text("Android Emulator (10.0.2.2)"),
                        backgroundColor: Colors.white,
                        side: const BorderSide(color: CropGuardTheme.border),
                        onPressed: () {
                          _urlController.text = "http://10.0.2.2:8000";
                          _saveUrl("http://10.0.2.2:8000");
                        },
                      ),
                      ActionChip(
                        label: const Text("Local Desktop (127.0.0.1)"),
                        backgroundColor: Colors.white,
                        side: const BorderSide(color: CropGuardTheme.border),
                        onPressed: () {
                          _urlController.text = "http://127.0.0.1:8000";
                          _saveUrl("http://127.0.0.1:8000");
                        },
                      ),
                      ActionChip(
                        label: const Text("Cloud Production (Render)"),
                        backgroundColor: Colors.white,
                        side: const BorderSide(color: CropGuardTheme.border),
                        onPressed: () {
                          _urlController.text = "https://cropguard-ai.onrender.com";
                          _saveUrl("https://cropguard-ai.onrender.com");
                        },
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Telemetry Provider Settings
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.cloud_sync_rounded, color: CropGuardTheme.primary, size: 22),
                      SizedBox(width: 10),
                      Text(
                        "Weather Telemetry Source",
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                      ),
                    ],
                  ),
                  SizedBox(height: 8),
                  Text(
                    "Primary: Open-Meteo WMO-calibrated real-time API (Zero API-key required).\nFallback: OpenWeatherMap (Configured via backend .env).",
                    style: TextStyle(fontSize: 13, color: CropGuardTheme.textSecondary, height: 1.4),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Local AI Engine Information
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.psychology_rounded, color: CropGuardTheme.primary, size: 22),
                      SizedBox(width: 10),
                      Text(
                        "Local Chatbot NLP Privacy",
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                      ),
                    ],
                  ),
                  SizedBox(height: 8),
                  Text(
                    "100% On-Premise Execution: Zero external calls to OpenAI, Gemini, Claude, or DeepSeek. All responses generated from local Kaggle knowledge bases and Backward Chaining inference.",
                    style: TextStyle(fontSize: 13, color: CropGuardTheme.textSecondary, height: 1.4),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
