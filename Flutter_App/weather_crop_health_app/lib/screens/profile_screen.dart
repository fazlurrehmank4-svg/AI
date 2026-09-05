import 'package:flutter/material.dart';
import '../theme.dart';
import '../services/auth_service.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final user = AuthService().currentUser;

    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(title: const Text("Farmer Profile")),
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
            const SizedBox(height: 20),

            // Profile Details
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  _buildProfileRow(Icons.place_outlined, "Farm Region", user?.farmLocation ?? "Central Agricultural Zone"),
                  const Divider(color: CropGuardTheme.border),
                  _buildProfileRow(Icons.spa_outlined, "Primary Crops", "Wheat, Tomato, Rice"),
                  const Divider(color: CropGuardTheme.border),
                  _buildProfileRow(Icons.security_outlined, "Database Security", "Supabase Row Level Security (RLS)"),
                  const Divider(color: CropGuardTheme.border),
                  _buildProfileRow(Icons.storage_outlined, "User Isolation", "Enforced via auth.uid()"),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Sign out button
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                icon: const Icon(Icons.logout, color: CropGuardTheme.dangerRed),
                label: const Text("Sign Out", style: TextStyle(color: CropGuardTheme.dangerRed)),
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

  Widget _buildProfileRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Icon(icon, size: 20, color: CropGuardTheme.primary),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: const TextStyle(fontSize: 12, color: CropGuardTheme.textSecondary)),
                const SizedBox(height: 2),
                Text(value, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: CropGuardTheme.textPrimary)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
