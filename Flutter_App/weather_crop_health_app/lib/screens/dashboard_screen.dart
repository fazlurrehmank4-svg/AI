import 'package:flutter/material.dart';
import '../theme.dart';
import '../models/crop_model.dart';
import '../models/weather_model.dart';
import '../models/prediction_model.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../services/location_service.dart';
import '../services/language_service.dart';
import '../widgets/weather_card.dart';
import '../widgets/health_score_gauge.dart';
import '../widgets/risk_badge.dart';
import '../widgets/forecast_alert_card.dart';
import '../models/forecast_alert_model.dart';
import '../widgets/logo_widget.dart';
import 'crop_selection_screen.dart';
import 'weather_screen.dart';
import 'prediction_screen.dart';
import 'chatbot_screen.dart';
import 'history_screen.dart';
import 'profile_screen.dart';
import 'settings_screen.dart';
import 'about_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final ApiService _apiService = ApiService();
  CropModel _selectedCrop = CropModel.supportedCrops[0]; // Wheat
  WeatherModel? _weather;
  PredictionModel? _latestPrediction;
  ForecastAlertModel? _forecastAlert;
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

    // 4. Fetch 3-Day Crop Hazard & Forecast Alert
    final fa = await _apiService.fetch3DayCropAlert(
      crop: _selectedCrop.name,
      city: cityToQuery,
    );

    if (mounted) {
      setState(() {
        _weather = w;
        _latestPrediction = p;
        _forecastAlert = fa;
        _farmLocation = w.locationName;
        _isLoading = false;
      });
    }
  }

  Future<void> _applyNewWeather(WeatherModel w) async {
    setState(() {
      _weather = w;
      _farmLocation = w.locationName;
      _isLoading = true;
    });

    await LocationService().setSavedDefaultLocation(w.locationName);
    await AuthService().updateFarmLocation(w.locationName);

    final p = await _apiService.predictCropHealth(
      crop: _selectedCrop.name,
      weather: w,
      userId: AuthService().currentUser?.id,
    );

    final fa = await _apiService.fetch3DayCropAlert(
      crop: _selectedCrop.name,
      city: w.locationName,
    );

    if (mounted) {
      setState(() {
        _latestPrediction = p;
        _forecastAlert = fa;
        _isLoading = false;
      });
    }
  }

  Future<void> _changeLocation(String city) async {
    setState(() => _isLoading = true);
    await LocationService().setSavedDefaultLocation(city);
    await AuthService().updateFarmLocation(city);
    final w = await _apiService.fetchWeather(city: city);
    await _applyNewWeather(w);
  }

  Future<void> _detectGpsLocation() async {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Detecting GPS coordinates..."), duration: Duration(seconds: 2)),
    );
    final loc = await LocationService().getCurrentLocation();
    if (!mounted) return;
    if (loc != null) {
      final w = await _apiService.fetchWeather(lat: loc.latitude, lon: loc.longitude);
      await _applyNewWeather(w);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: CropGuardTheme.primary,
          content: Text("📍 Farm location set to: ${w.locationName}"),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          backgroundColor: Colors.orange,
          content: Text("Could not retrieve GPS coordinates. Please check location permissions."),
        ),
      );
    }
  }

  void _showLocationPickerBottomSheet() {
    final searchCtrl = TextEditingController(text: _farmLocation);
    final popularAgriDistricts = [
      "Pune", "Nashik", "Ludhiana", "Varanasi", "Nagpur",
      "Hyderabad", "Bengaluru", "Ahmedabad", "Jaipur", "Indore",
    ];

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (ctx) {
        return Padding(
          padding: EdgeInsets.only(
            left: 20,
            right: 20,
            top: 20,
            bottom: MediaQuery.of(ctx).viewInsets.bottom + 20,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Container(
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: Colors.grey.shade300,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                "Choose Your Farm Location",
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w800,
                  color: CropGuardTheme.textPrimary,
                ),
              ),
              const SizedBox(height: 6),
              const Text(
                "Select your agricultural district or auto-detect via GPS for live weather telemetry.",
                style: TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary),
              ),
              const SizedBox(height: 16),

              // 1. Auto GPS Detect Button
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: CropGuardTheme.primary.withValues(alpha: 0.1),
                  foregroundColor: CropGuardTheme.primary,
                  elevation: 0,
                  minimumSize: const Size(double.infinity, 46),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                    side: const BorderSide(color: CropGuardTheme.primary),
                  ),
                ),
                icon: const Icon(Icons.my_location_rounded, size: 18),
                label: const Text(
                  "Use Current GPS Location",
                  style: TextStyle(fontWeight: FontWeight.w700),
                ),
                onPressed: () {
                  Navigator.pop(ctx);
                  _detectGpsLocation();
                },
              ),
              const SizedBox(height: 16),

              // 2. Custom Location Search Input
              TextField(
                controller: searchCtrl,
                autofocus: false,
                decoration: InputDecoration(
                  hintText: "Type any district (e.g. Nashik, Ludhiana)...",
                  prefixIcon: const Icon(Icons.search, color: CropGuardTheme.primary),
                  suffixIcon: IconButton(
                    icon: const Icon(Icons.check_circle_rounded, color: CropGuardTheme.primary),
                    onPressed: () {
                      final val = searchCtrl.text.trim();
                      if (val.isNotEmpty) {
                        Navigator.pop(ctx);
                        _changeLocation(val);
                      }
                    },
                  ),
                ),
                onSubmitted: (val) {
                  if (val.trim().isNotEmpty) {
                    Navigator.pop(ctx);
                    _changeLocation(val.trim());
                  }
                },
              ),
              const SizedBox(height: 16),

              // 3. Quick Popular Districts
              const Text(
                "Major Agricultural Hubs",
                style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: CropGuardTheme.textSecondary),
              ),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: popularAgriDistricts.map((city) {
                  final isSelected = _farmLocation.toLowerCase().contains(city.toLowerCase());
                  return ChoiceChip(
                    label: Text(city),
                    selected: isSelected,
                    selectedColor: CropGuardTheme.primary.withValues(alpha: 0.2),
                    backgroundColor: Colors.white,
                    side: BorderSide(
                      color: isSelected ? CropGuardTheme.primary : CropGuardTheme.border,
                    ),
                    labelStyle: TextStyle(
                      fontSize: 12,
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                      color: isSelected ? CropGuardTheme.primaryDark : CropGuardTheme.textPrimary,
                    ),
                    onSelected: (_) {
                      Navigator.pop(ctx);
                      _changeLocation(city);
                    },
                  );
                }).toList(),
              ),
            ],
          ),
        );
      },
    );
  }

  Future<void> _openWeatherScreen() async {
    final updatedWeather = await Navigator.push<WeatherModel>(
      context,
      MaterialPageRoute(builder: (_) => WeatherScreen(initialWeather: _weather)),
    );
    if (updatedWeather != null) {
      _applyNewWeather(updatedWeather);
    } else {
      _loadDashboardData();
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
      final fa = await _apiService.fetch3DayCropAlert(
        crop: newCrop.name,
        city: _weather?.locationName ?? _farmLocation,
      );
      if (mounted) {
        setState(() {
          _latestPrediction = p;
          _forecastAlert = fa;
          _isLoading = false;
        });
      }
    } else {
      _loadDashboardData();
    }
  }

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<String>(
      valueListenable: LanguageService(),
      builder: (context, currentLang, _) {
        final user = AuthService().currentUser;
        final userName = user?.fullName ?? "Farmer";

        return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: const [
            CropGuardLogo(size: 26, showText: false),
            SizedBox(width: 8),
            Text("CropGuard AI"),
          ],
        ),
        leading: Builder(
          builder: (ctx) => IconButton(
            icon: const Icon(Icons.menu_rounded),
            onPressed: () => Scaffold.of(ctx).openDrawer(),
          ),
        ),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.language_rounded),
            tooltip: "Change Language (भाषा / زبان)",
            onSelected: (lang) {
              LanguageService().setLanguage(lang);
              final label = lang == "ur" ? "اردو" : lang == "hi" ? "हिंदी" : "English";
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  backgroundColor: CropGuardTheme.primary,
                  duration: const Duration(seconds: 2),
                  content: Text("Language set to $label"),
                ),
              );
            },
            itemBuilder: (ctx) => const [
              PopupMenuItem(value: "en", child: Text("English")),
              PopupMenuItem(value: "hi", child: Text("हिंदी")),
              PopupMenuItem(value: "ur", child: Text("اردو")),
            ],
          ),
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
                    // 1. Greeting & Farm Location (Mobile Responsive & Overflow-Safe)
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                "Welcome, $userName 👋",
                                style: const TextStyle(
                                  fontSize: 19,
                                  fontWeight: FontWeight.w800,
                                  color: CropGuardTheme.textPrimary,
                                ),
                                overflow: TextOverflow.ellipsis,
                              ),
                              const SizedBox(height: 3),
                              InkWell(
                                onTap: _showLocationPickerBottomSheet,
                                borderRadius: BorderRadius.circular(16),
                                child: Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                                  decoration: BoxDecoration(
                                    color: Colors.white,
                                    borderRadius: BorderRadius.circular(16),
                                    border: Border.all(color: CropGuardTheme.primary.withValues(alpha: 0.25)),
                                    boxShadow: [
                                      BoxShadow(
                                        color: Colors.black.withValues(alpha: 0.04),
                                        blurRadius: 4,
                                        offset: const Offset(0, 2),
                                      ),
                                    ],
                                  ),
                                  child: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      const Icon(Icons.location_on_rounded, size: 14, color: CropGuardTheme.primary),
                                      const SizedBox(width: 4),
                                      Flexible(
                                        child: Text(
                                          _farmLocation,
                                          style: const TextStyle(
                                            fontSize: 12.5,
                                            fontWeight: FontWeight.w700,
                                            color: CropGuardTheme.primaryDark,
                                          ),
                                          overflow: TextOverflow.ellipsis,
                                          maxLines: 1,
                                        ),
                                      ),
                                      const SizedBox(width: 4),
                                      const Icon(Icons.edit_location_alt_outlined, size: 14, color: CropGuardTheme.textSecondary),
                                    ],
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 10),
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
                              color: CropGuardTheme.primary.withValues(alpha: 0.12),
                              borderRadius: BorderRadius.circular(20),
                              border: Border.all(color: CropGuardTheme.primaryLight, width: 1.2),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
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
                        onTap: _openWeatherScreen,
                        child: WeatherCard(
                          weather: _weather!,
                          onRefresh: _loadDashboardData,
                        ),
                      ),
                    const SizedBox(height: 20),

                    // 3. Crop Health Prediction Overview Card
                    if (_latestPrediction != null) _buildHealthOverviewCard(context, _latestPrediction!),
                    const SizedBox(height: 20),

                    // 4. 3-Day Crop Hazard & Forecast Alert Card
                    if (_forecastAlert != null) ...[
                      ForecastAlertCard(
                        forecastAlert: _forecastAlert!,
                        onRefresh: _loadDashboardData,
                      ),
                      const SizedBox(height: 20),
                    ],

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
      },
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
            children: [
              const Expanded(
                child: Text(
                  "Crop Health Diagnosis",
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
                    color: CropGuardTheme.textPrimary,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: 8),
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
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF1B5E20), Color(0xFF2E7D32)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            accountName: Text(user?.fullName ?? "Farmer", style: const TextStyle(fontWeight: FontWeight.bold)),
            accountEmail: Text(user?.email ?? "farmer@cropguard.ai"),
            currentAccountPicture: Container(
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.white,
              ),
              padding: const EdgeInsets.all(4),
              child: const CropGuardLogo(size: 48, showText: false),
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
              _openWeatherScreen();
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
