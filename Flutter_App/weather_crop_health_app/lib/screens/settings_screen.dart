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
  bool _isTesting = false;
  Map<String, dynamic>? _testResult;

  @override
  void initState() {
    super.initState();
    _urlController = TextEditingController(text: _apiService.baseUrl);
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  void _saveUrl(String url) async {
    await _apiService.setBaseUrl(url);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Backend URL set to: $url"),
          backgroundColor: CropGuardTheme.primary,
        ),
      );
      setState(() {});
    }
  }

  Future<void> _runConnectionDiagnostic([String? customUrl]) async {
    setState(() {
      _isTesting = true;
      _testResult = null;
    });

    final target = customUrl ?? _urlController.text.trim();
    final result = await _apiService.testConnection(target.isNotEmpty ? target : null);

    if (mounted) {
      setState(() {
        _isTesting = false;
        _testResult = result;
        if (result["success"] == true && result["url"] != null) {
          _urlController.text = result["url"] as String;
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(title: const Text("Application Settings")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Backend Connectivity Card
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(18),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    children: [
                      Icon(Icons.dns_rounded, color: CropGuardTheme.primary, size: 22),
                      SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          "FastAPI Backend Endpoint",
                          style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    "Configure the active server endpoint for ML inference and local multilingual AI reasoning.",
                    style: TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _urlController,
                    decoration: InputDecoration(
                      labelText: "Backend Base URL",
                      hintText: "http://192.168.0.146:8000",
                      suffixIcon: IconButton(
                        icon: const Icon(Icons.check_circle_rounded, color: CropGuardTheme.primary),
                        onPressed: () => _saveUrl(_urlController.text),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Auto-Detect & Diagnostic Button
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: CropGuardTheme.primary,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      icon: _isTesting
                          ? const SizedBox(
                              width: 16,
                              height: 16,
                              child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                            )
                          : const Icon(Icons.network_check_rounded, size: 18),
                      label: Text(_isTesting ? "Testing Connection..." : "Auto-Detect & Test Server"),
                      onPressed: _isTesting ? null : () => _runConnectionDiagnostic(),
                    ),
                  ),

                  // Diagnostic Result Box
                  if (_testResult != null) ...[
                    const SizedBox(height: 12),
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: _testResult!["success"] == true ? const Color(0xFFE8F5E9) : const Color(0xFFFFEBEE),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(
                          color: _testResult!["success"] == true ? const Color(0xFFA5D6A7) : const Color(0xFFEF9A9A),
                        ),
                      ),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Icon(
                            _testResult!["success"] == true ? Icons.check_circle_rounded : Icons.error_outline_rounded,
                            color: _testResult!["success"] == true ? const Color(0xFF2E7D32) : const Color(0xFFC62828),
                            size: 20,
                          ),
                          const SizedBox(width: 10),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  _testResult!["success"] == true
                                      ? "Connected successfully (${_testResult!['latency_ms']} ms)"
                                      : "Connection Failed",
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 13,
                                    color: _testResult!["success"] == true ? const Color(0xFF2E7D32) : const Color(0xFFC62828),
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  _testResult!["success"] == true
                                      ? "Active URL: ${_testResult!['url']}\nService: ${_testResult!['service']}"
                                      : "${_testResult!['error']}\n\nTip: For USB mobile, run 'adb reverse tcp:8000 tcp:8000' or select Wi-Fi LAN preset below.",
                                  style: const TextStyle(fontSize: 11.5, height: 1.35),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],

                  const SizedBox(height: 16),
                  const Text("Quick Presets:", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: CropGuardTheme.textSecondary)),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      ActionChip(
                        avatar: const Icon(Icons.usb_rounded, size: 16, color: CropGuardTheme.primary),
                        label: const Text("USB Mobile (127.0.0.1)"),
                        backgroundColor: Colors.white,
                        side: const BorderSide(color: CropGuardTheme.border),
                        onPressed: () {
                          _urlController.text = "http://127.0.0.1:8000";
                          _saveUrl("http://127.0.0.1:8000");
                          _runConnectionDiagnostic("http://127.0.0.1:8000");
                        },
                      ),
                      ActionChip(
                        avatar: const Icon(Icons.wifi_rounded, size: 16, color: CropGuardTheme.primary),
                        label: const Text("Wi-Fi LAN (192.168.0.146)"),
                        backgroundColor: Colors.white,
                        side: const BorderSide(color: CropGuardTheme.border),
                        onPressed: () {
                          _urlController.text = "http://192.168.0.146:8000";
                          _saveUrl("http://192.168.0.146:8000");
                          _runConnectionDiagnostic("http://192.168.0.146:8000");
                        },
                      ),
                      ActionChip(
                        avatar: const Icon(Icons.phone_android_rounded, size: 16, color: CropGuardTheme.primary),
                        label: const Text("Android Emulator (10.0.2.2)"),
                        backgroundColor: Colors.white,
                        side: const BorderSide(color: CropGuardTheme.border),
                        onPressed: () {
                          _urlController.text = "http://10.0.2.2:8000";
                          _saveUrl("http://10.0.2.2:8000");
                          _runConnectionDiagnostic("http://10.0.2.2:8000");
                        },
                      ),
                      ActionChip(
                        avatar: const Icon(Icons.cloud_rounded, size: 16, color: CropGuardTheme.primary),
                        label: const Text("Cloud (Render)"),
                        backgroundColor: Colors.white,
                        side: const BorderSide(color: CropGuardTheme.border),
                        onPressed: () {
                          _urlController.text = "https://ai-fb48.onrender.com";
                          _saveUrl("https://ai-fb48.onrender.com");
                          _runConnectionDiagnostic("https://ai-fb48.onrender.com");
                        },
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 18),

            // Mobile Connectivity Guide
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(18),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.phone_iphone_rounded, color: CropGuardTheme.primary, size: 22),
                      SizedBox(width: 10),
                      Text(
                        "Mobile Device Connection Guide",
                        style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                      ),
                    ],
                  ),
                  SizedBox(height: 10),
                  Text(
                    "• **Via USB Cable:** Connect mobile to laptop via USB with USB Debugging enabled. The app communicates directly over port 8000.\n\n"
                    "• **Via Wi-Fi:** Ensure your mobile phone and laptop are connected to the same Wi-Fi router, and tap the 'Wi-Fi LAN (192.168.0.146)' preset.\n\n"
                    "• **Offline Mode:** If not connected to the laptop, CropGuard AI automatically activates its on-device reasoning engine to diagnose crops and provide advice.",
                    style: TextStyle(fontSize: 12.5, color: CropGuardTheme.textSecondary, height: 1.45),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 18),

            // Local AI Engine Privacy
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(18),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.psychology_rounded, color: CropGuardTheme.primary, size: 22),
                      SizedBox(width: 10),
                      Text(
                        "Local AI & Multi-Language Engine",
                        style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                      ),
                    ],
                  ),
                  SizedBox(height: 8),
                  Text(
                    "100% On-Premise Execution: Zero external calls to OpenAI, Gemini, or third-party paid APIs. Full support for English, Hindi (हिंदी), and Urdu (اردو) with continuous self-learning.",
                    style: TextStyle(fontSize: 12.5, color: CropGuardTheme.textSecondary, height: 1.4),
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
