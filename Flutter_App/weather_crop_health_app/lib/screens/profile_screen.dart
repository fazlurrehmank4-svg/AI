import 'package:flutter/material.dart';
import '../theme.dart';
import '../services/auth_service.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  String _appLanguage = "en"; // "en", "hi", "ur"

  @override
  Widget build(BuildContext context) {
    final user = AuthService().currentUser;

    final isHindi = _appLanguage == "hi";
    final isUrdu = _appLanguage == "ur";

    final appBarTitle = isUrdu
        ? "کسان پروفائل"
        : isHindi
            ? "किसान प्रोफ़ाइल"
            : "Farmer Profile";

    final langCardTitle = isUrdu
        ? "ایپ کی زبان تبدیل کریں"
        : isHindi
            ? "ऐप भाषा बदलें (Language)"
            : "App Language (भाषा / زبان)";

    final detailsCardTitle = isUrdu
        ? "فارم اور سیکورٹی تفصیلات"
        : isHindi
            ? "फॉर्म और सुरक्षा विवरण"
            : "Farm & Security Details";

    final locationLabel = isUrdu
        ? "فارم کا علاقہ"
        : isHindi
            ? "फार्म क्षेत्र"
            : "Farm Region";

    final cropsLabel = isUrdu
        ? "اہم فصلیں"
        : isHindi
            ? "प्रमुख फसलें"
            : "Primary Crops";

    final dbSecurityLabel = isUrdu
        ? "ڈیٹا بیس کی حفاظت"
        : isHindi
            ? "डेटाबेस सुरक्षा"
            : "Database Security";

    final userIsolationLabel = isUrdu
        ? "صارف کی حفاظت"
        : isHindi
            ? "उपयोगकर्ता अलगाव"
            : "User Isolation";

    final signOutLabel = isUrdu
        ? "سائن آؤٹ کریں"
        : isHindi
            ? "साइन आउट करें"
            : "Sign Out";

    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(title: Text(appBarTitle)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            // Avatar & Name Card
            Container(
              width: double.infinity,
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  CircleAvatar(
                    radius: 38,
                    backgroundColor: CropGuardTheme.primary,
                    child: Text(
                      (user?.fullName.isNotEmpty == true ? user!.fullName[0] : "F").toUpperCase(),
                      style: const TextStyle(fontSize: 32, fontWeight: FontWeight.w800, color: Colors.white),
                    ),
                  ),
                  const SizedBox(height: 14),
                  Text(
                    user?.fullName ?? "Farmer",
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    user?.email ?? "farmer@cropguard.ai",
                    style: const TextStyle(fontSize: 13, color: CropGuardTheme.textSecondary),
                  ),
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: const Color(0xFFE8F5E9),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      user?.isGuest == true ? "Guest Producer" : "Verified Agriculturalist",
                      style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: CropGuardTheme.primary),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 18),

            // LEFT SIDE OF PROFILE / LANGUAGE SELECTOR CARD
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(18),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.language_rounded, color: CropGuardTheme.primary, size: 22),
                      const SizedBox(width: 10),
                      Text(
                        langCardTitle,
                        style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildLangChip("en", "English 🇬🇧"),
                      _buildLangChip("hi", "हिंदी 🇮🇳"),
                      _buildLangChip("ur", "اردو 🇵🇰"),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 18),

            // Profile Details
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    detailsCardTitle,
                    style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                  ),
                  const SizedBox(height: 12),
                  _buildProfileRow(Icons.place_outlined, locationLabel, user?.farmLocation ?? "Central Agricultural Zone"),
                  const Divider(color: CropGuardTheme.border),
                  _buildProfileRow(Icons.spa_outlined, cropsLabel, "Wheat, Tomato, Rice"),
                  const Divider(color: CropGuardTheme.border),
                  _buildProfileRow(Icons.security_outlined, dbSecurityLabel, "Supabase Row Level Security (RLS)"),
                  const Divider(color: CropGuardTheme.border),
                  _buildProfileRow(Icons.storage_outlined, userIsolationLabel, "Enforced via auth.uid()"),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Sign out button
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                icon: const Icon(Icons.logout, color: CropGuardTheme.dangerRed),
                label: Text(signOutLabel, style: const TextStyle(color: CropGuardTheme.dangerRed)),
                onPressed: () async {
                  await AuthService().logout();
                  if (context.mounted) {
                    Navigator.of(context).pushNamedAndRemoveUntil('/', (route) => false);
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLangChip(String langCode, String label) {
    final isSelected = _appLanguage == langCode;
    return GestureDetector(
      onTap: () {
        setState(() {
          _appLanguage = langCode;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: CropGuardTheme.primary,
            duration: const Duration(seconds: 2),
            content: Text(
              langCode == "ur"
                  ? "زبان اردو میں تبدیل کر دی گئی ہے"
                  : langCode == "hi"
                      ? "भाषा बदलकर हिंदी कर दी गई है"
                      : "Language switched to English",
            ),
          ),
        );
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected ? CropGuardTheme.primary : CropGuardTheme.background,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: isSelected ? CropGuardTheme.primary : CropGuardTheme.border,
            width: 1.2,
          ),
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

  Widget _buildProfileRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Icon(icon, color: CropGuardTheme.primary, size: 20),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: const TextStyle(fontSize: 11, color: CropGuardTheme.textSecondary)),
                const SizedBox(height: 2),
                Text(value, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: CropGuardTheme.textPrimary)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
