import 'package:flutter/material.dart';
import '../theme.dart';
import '../models/crop_model.dart';
import '../models/weather_model.dart';
import '../models/prediction_model.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../services/location_service.dart';
import '../widgets/weather_card.dart';
import '../widgets/health_score_gauge.dart';
import '../widgets/risk_badge.dart';
import 'crop_selection_screen.dart';
import 'weather_screen.dart';
import 'prediction_screen.dart';
import 'chatbot_screen.dart';
import 'history_screen.dart';
import 'profile_screen.dart';
import 'settings_screen.dart';
import 'about_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final ApiService _apiService = ApiService();
  CropModel _selectedCrop = CropModel.supportedCrops[0]; // Wheat
  WeatherModel? _weather;
  PredictionModel? _latestPrediction;
  bool _isLoading = true;
  String _farmLocation = "Locating farm...";

  @override
  void initState() {
    super.initState();
    _loadDashboardData();
  }

  Future<void> _loadDashboardData() async {
    setState(() => _isLoading = true);
    // 1. Resolve farmer's default location (from GPS, saved preferences, or profile)
    final savedLoc = await LocationService().getSavedDefaultLocation();
    final profileLoc = AuthService().currentUser?.farmLocation;
    final cityToQuery = savedLoc ?? (profileLoc != null && profileLoc.isNotEmpty ? profileLoc : "New Delhi");

    // 2. Fetch current weather for the farmer's location
    final w = await _apiService.fetchWeather(city: cityToQuery);

    // 3. Perform automated baseline prediction for selected crop
    final p = await _apiService.predictCropHealth(
      crop: _selectedCrop.name,
      weather: w,
      userId: AuthService().currentUser?.id,
    );

    if (mounted) {
      setState(() {
        _weather = w;
        _latestPrediction = p;
        _farmLocation = w.locationName;
        _isLoading = false;
      });
    }
  }

  void _onCropChanged(CropModel newCrop) async {
    setState(() {
      _selectedCrop = newCrop;
      _isLoading = true;
    });

    if (_weather != null) {
      final p = await _apiService.predictCropHealth(
        crop: newCrop.name,
        weather: _weather!,
        userId: AuthService().currentUser?.id,
      );
      if (mounted) {
        setState(() {
          _latestPrediction = p;
          _isLoading = false;
        });
      }
    } else {
      _loadDashboardData();
    }
  }

  @override
  Widget build(BuildContext context) {
    final user = AuthService().currentUser;
    final userName = user?.fullName ?? "Farmer";

    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(
        title: const Text("CropGuard AI"),
        leading: Builder(
          builder: (ctx) => IconButton(
            icon: const Icon(Icons.menu_rounded),
            onPressed: () => Scaffold.of(ctx).openDrawer(),
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.tune_rounded),
            tooltip: "Settings",
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const SettingsScreen()),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.account_circle_outlined),
            tooltip: "Farmer Profile",
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ProfileScreen()),
            ),
          ),
        ],
      ),
      drawer: _buildDrawer(context),
      body: _isLoading
          ? const Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircularProgressIndicator(color: CropGuardTheme.primary),
                  SizedBox(height: 16),
                  Text("Computing Meteorological AI Inference...", style: TextStyle(color: CropGuardTheme.textSecondary)),
                ],
              ),
            )
          : RefreshIndicator(
              onRefresh: _loadDashboardData,
              color: CropGuardTheme.primary,
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // 1. Greeting & Farm Location
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Welcome, $userName 👋",
                              style: const TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.w800,
                                color: CropGuardTheme.textPrimary,
                              ),
                            ),
                            const SizedBox(height: 3),
                            Row(
                              children: [
                                const Icon(Icons.location_on_rounded, size: 13, color: CropGuardTheme.primary),
                                const SizedBox(width: 4),
                                Text(
                                  _farmLocation,
                                  style: const TextStyle(fontSize: 13, color: CropGuardTheme.textSecondary),
                                ),
                              ],
                            ),
                          ],
                        ),
                        // Crop Selector Chip
                        GestureDetector(
                          onTap: () async {
                            final picked = await Navigator.push<CropModel>(
                              context,
                              MaterialPageRoute(
                                builder: (_) => CropSelectionScreen(selectedCrop: _selectedCrop),
                              ),
                            );
                            if (picked != null) _onCropChanged(picked);
                          },
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
                            decoration: BoxDecoration(
                              color: CropGuardTheme.primary.withOpacity(0.12),
                              borderRadius: BorderRadius.circular(20),
                              border: Border.all(color: CropGuardTheme.primaryLight, width: 1.2),
                            ),
                            child: Row(
                              children: [
                                Text(_selectedCrop.emoji, style: const TextStyle(fontSize: 16)),
                                const SizedBox(width: 6),
                                Text(
                                  _selectedCrop.name,
                                  style: const TextStyle(
                                    fontWeight: FontWeight.w700,
                                    color: CropGuardTheme.primaryDark,
                                    fontSize: 13,
                                  ),
                                ),
                                const Icon(Icons.arrow_drop_down, size: 18, color: CropGuardTheme.primaryDark),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),

                    // 2. Weather Summary Card
                    if (_weather != null)
                      GestureDetector(
                        onTap: () => Navigator.push(
                          context,
                          MaterialPageRoute(builder: (_) => WeatherScreen(initialWeather: _weather)),
                        ),
                        child: WeatherCard(
                          weather: _weather!,
                          onRefresh: _loadDashboardData,
                        ),
                      ),
                    const SizedBox(height: 20),

                    // 3. Crop Health Prediction Overview Card
                    if (_latestPrediction != null) _buildHealthOverviewCard(context, _latestPrediction!),
                    const SizedBox(height: 20),

                    // 4. Action Buttons (Quick Prediction & Ask AI)
                    Row(
                      children: [
                        Expanded(
                          child: ElevatedButton.icon(
                            icon: const Icon(Icons.analytics_outlined, size: 18),
                            label: const Text("Full Analysis"),
                            onPressed: () {
                              if (_latestPrediction != null) {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (_) => PredictionScreen(prediction: _latestPrediction!),
                                  ),
                                );
                              }
                            },
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: OutlinedButton.icon(
                            icon: const Icon(Icons.chat_bubble_outline_rounded, size: 18),
                            label: const Text("Ask Local AI"),
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => ChatbotScreen(
                                    activeCrop: _selectedCrop.name,
                                    currentPrediction: _latestPrediction,
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),

                    // 5. Recent Agronomic Alert / Causes Preview
                    if (_latestPrediction != null && _latestPrediction!.causes.isNotEmpty)
                      _buildAlertSnippet(_latestPrediction!),
                  ],
                ),
              ),
            ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: CropGuardTheme.primary,
        icon: const Icon(Icons.smart_toy_outlined, color: Colors.white),
        label: const Text("Ask CropGuard", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => ChatbotScreen(
                activeCrop: _selectedCrop.name,
                currentPrediction: _latestPrediction,
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildHealthOverviewCard(BuildContext context, PredictionModel pred) {
    return Container(
      decoration: CropGuardTheme.cardDecoration,
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                "Crop Health Diagnosis",
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w800,
                  color: CropGuardTheme.textPrimary,
                ),
              ),
              RiskBadge(status: pred.healthStatus, riskLevel: pred.riskLevel),
            ],
          ),
          const SizedBox(height: 18),
          Row(
            children: [
              HealthScoreGauge(score: pred.cropHealthScore, size: 110),
              const SizedBox(width: 20),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "${pred.crop} Health Index",
                      style: const TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w700,
                        color: CropGuardTheme.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      pred.primaryRiskFactor,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                        fontSize: 12,
                        color: CropGuardTheme.textSecondary,
                      ),
                    ),
                    const SizedBox(height: 10),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: const Color(0xFFE8F5E9),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        pred.agroClimaticRegime,
                        style: const TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w600,
                          color: CropGuardTheme.primary,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildAlertSnippet(PredictionModel pred) {
    final hasWarning = pred.healthStatus != "Healthy";
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: hasWarning ? const Color(0xFFFFF8E1) : const Color(0xFFF1F8E9),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: hasWarning ? const Color(0xFFFFB74D) : const Color(0xFFAED581),
          width: 1.2,
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            hasWarning ? Icons.warning_amber_rounded : Icons.check_circle_outline,
            color: hasWarning ? CropGuardTheme.warningOrange : CropGuardTheme.healthyGreen,
            size: 22,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  hasWarning ? "Agronomic Stress Factors" : "Optimal Conditions",
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w700,
                    color: hasWarning ? CropGuardTheme.warningOrange : CropGuardTheme.healthyGreen,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  pred.causes.first,
                  style: const TextStyle(fontSize: 12, color: CropGuardTheme.textPrimary, height: 1.3),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDrawer(BuildContext context) {
    final user = AuthService().currentUser;
    return Drawer(
      child: Column(
        children: [
          UserAccountsDrawerHeader(
            decoration: const BoxDecoration(color: CropGuardTheme.primary),
            accountName: Text(user?.fullName ?? "Farmer", style: const TextStyle(fontWeight: FontWeight.bold)),
            accountEmail: Text(user?.email ?? "farmer@cropguard.ai"),
            currentAccountPicture: CircleAvatar(
              backgroundColor: Colors.white,
              child: Text(
                (user?.fullName.isNotEmpty == true ? user!.fullName[0] : "F").toUpperCase(),
                style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold, color: CropGuardTheme.primary),
              ),
            ),
          ),
          ListTile(
            leading: const Icon(Icons.dashboard_outlined, color: CropGuardTheme.primary),
            title: const Text("Home Dashboard"),
            onTap: () => Navigator.pop(context),
          ),
          ListTile(
            leading: const Icon(Icons.spa_outlined, color: CropGuardTheme.primary),
            title: const Text("Select Crop"),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => CropSelectionScreen(selectedCrop: _selectedCrop)),
              ).then((c) {
                if (c != null) _onCropChanged(c);
              });
            },
          ),
          ListTile(
            leading: const Icon(Icons.cloud_outlined, color: CropGuardTheme.primary),
            title: const Text("Weather Telemetry"),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => WeatherScreen(initialWeather: _weather)));
            },
          ),
          ListTile(
            leading: const Icon(Icons.smart_toy_outlined, color: CropGuardTheme.primary),
            title: const Text("CropGuard AI Assistant (Local)"),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => ChatbotScreen(
                    activeCrop: _selectedCrop.name,
                    currentPrediction: _latestPrediction,
                  ),
                ),
              );
            },
          ),
          ListTile(
            leading: const Icon(Icons.history_rounded, color: CropGuardTheme.primary),
            title: const Text("Prediction History"),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const HistoryScreen()));
            },
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.settings_outlined, color: CropGuardTheme.textSecondary),
            title: const Text("Settings & API Endpoint"),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen()));
            },
          ),
          ListTile(
            leading: const Icon(Icons.info_outline, color: CropGuardTheme.textSecondary),
            title: const Text("About Project & AI Practicals"),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const AboutScreen()));
            },
          ),
          const Spacer(),
          ListTile(
            leading: const Icon(Icons.logout_rounded, color: CropGuardTheme.dangerRed),
            title: const Text("Sign Out", style: TextStyle(color: CropGuardTheme.dangerRed)),
            onTap: () async {
              await AuthService().logout();
              if (context.mounted) {
                Navigator.of(context).pushNamedAndRemoveUntil('/', (route) => false);
              }
            },
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}
