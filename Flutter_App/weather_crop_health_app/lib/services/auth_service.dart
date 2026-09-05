import 'package:shared_preferences/shared_preferences.dart';

class FarmerUser {
  final String id;
  final String email;
  final String fullName;
  final String farmLocation;
  final bool isGuest;

  FarmerUser({
    required this.id,
    required this.email,
    required this.fullName,
    required this.farmLocation,
    this.isGuest = false,
  });
}

class AuthService {
  static final AuthService _instance = AuthService._internal();
  factory AuthService() => _instance;
  AuthService._internal();

  FarmerUser? _currentUser;
  String? _authToken;

  FarmerUser? get currentUser => _currentUser;
  String? get authToken => _authToken;
  bool get isAuthenticated => _currentUser != null;

  Future<void> init() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final id = prefs.getString("user_id");
      final email = prefs.getString("user_email");
      final name = prefs.getString("user_name");
      final loc = prefs.getString("farm_loc");
      final isGuest = prefs.getBool("is_guest") ?? false;
      _authToken = prefs.getString("auth_token");

      if (id != null && email != null) {
        _currentUser = FarmerUser(
          id: id,
          email: email,
          fullName: name ?? "Farmer",
          farmLocation: loc ?? "Green Valley Farm",
          isGuest: isGuest,
        );
      }
    } catch (_) {}
  }

  Future<bool> login({required String email, required String password}) async {
    // In production, communicates with Supabase Auth endpoint:
    // https://tspdpkyhszrebrclsefz.supabase.co/auth/v1/token?grant_type=password
    // Here we validate input format and persist user session securely.
    if (email.isEmpty || password.length < 6) return false;

    final user = FarmerUser(
      id: "usr_${email.hashCode.abs()}",
      email: email,
      fullName: email.split("@")[0].capitalizeFirst(),
      farmLocation: "Central Agricultural Zone",
      isGuest: false,
    );

    await _saveUser(user, "jwt_token_sample_${DateTime.now().millisecondsSinceEpoch}");
    return true;
  }

  Future<bool> signup({required String email, required String password, required String fullName, required String location}) async {
    if (email.isEmpty || password.length < 6) return false;

    final user = FarmerUser(
      id: "usr_${email.hashCode.abs()}",
      email: email,
      fullName: fullName.isNotEmpty ? fullName : "Farmer",
      farmLocation: location.isNotEmpty ? location : "Greenfield Valley",
      isGuest: false,
    );

    await _saveUser(user, "jwt_token_sample_${DateTime.now().millisecondsSinceEpoch}");
    return true;
  }

  Future<void> loginAsGuest() async {
    final guest = FarmerUser(
      id: "guest-farmer-01",
      email: "guest@cropguard.ai",
      fullName: "Guest Farmer",
      farmLocation: "Demonstration Agri-Station",
      isGuest: true,
    );
    await _saveUser(guest, null);
  }

  Future<void> logout() async {
    _currentUser = null;
    _authToken = null;
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove("user_id");
      await prefs.remove("user_email");
      await prefs.remove("user_name");
      await prefs.remove("farm_loc");
      await prefs.remove("is_guest");
      await prefs.remove("auth_token");
    } catch (_) {}
  }
  Future<void> updateFarmLocation(String newLocation) async {
    final clean = newLocation.trim();
    if (clean.isEmpty) return;
    if (_currentUser != null) {
      _currentUser = FarmerUser(
        id: _currentUser!.id,
        email: _currentUser!.email,
        fullName: _currentUser!.fullName,
        farmLocation: clean,
        isGuest: _currentUser!.isGuest,
      );
    }
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("farm_loc", clean);
      await prefs.setString("farmer_default_location", clean);
    } catch (_) {}
  }

  Future<void> _saveUser(FarmerUser user, String? token) async {
    _currentUser = user;
    _authToken = token;
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("user_id", user.id);
      await prefs.setString("user_email", user.email);
      await prefs.setString("user_name", user.fullName);
      await prefs.setString("farm_loc", user.farmLocation);
      await prefs.setBool("is_guest", user.isGuest);
      if (token != null) {
        await prefs.setString("auth_token", token);
      }
    } catch (_) {}
  }
}

extension StringExtension on String {
  String capitalizeFirst() {
    if (isEmpty) return this;
    return "${this[0].toUpperCase()}${substring(1)}";
  }
}
