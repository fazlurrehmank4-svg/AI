import 'package:flutter/material.dart';
import '../theme.dart';
import '../widgets/logo_widget.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CropGuardTheme.background,
      appBar: AppBar(title: const Text("About CropGuard AI")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        child: Column(
          children: [
            const CropGuardLogo(size: 72, showText: true),
            const SizedBox(height: 24),

            // Mission Statement
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "College AI Mini-Project Overview",
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                  ),
                  SizedBox(height: 8),
                  Text(
                    "CropGuard AI is a comprehensive, production-grade agricultural decision support system designed to assist farmers in understanding crop vigor, identifying meteorological disease vulnerabilities, and receiving actionable precautions.\n\n"
                    "The application integrates the first 9 Artificial Intelligence Laboratory Practicals into a single cohesive, deployable architecture with a FastAPI backend and Supabase database.",
                    style: TextStyle(fontSize: 13, color: CropGuardTheme.textSecondary, height: 1.45),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 18),

            // AI Practicals Mapping Table
            Container(
              decoration: CropGuardTheme.cardDecoration,
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Integrated AI Lab Practicals",
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: CropGuardTheme.textPrimary),
                  ),
                  const SizedBox(height: 14),
                  _buildPracticalRow("P01", "NumPy, Pandas, Matplotlib", "Data engineering & correlation visualization"),
                  _buildPracticalRow("P02", "BFS & DFS Graph Search", "Vulnerability state-space exploration"),
                  _buildPracticalRow("P03", "GBFS & A* Search", "Informed heuristic remediation cost planning"),
                  _buildPracticalRow("P04", "Hill Climbing Search", "Microclimate irrigation & shade optimization"),
                  _buildPracticalRow("P05", "Forward & Backward Chaining", "Root cause deduction & XAI proof engine"),
                  _buildPracticalRow("P06", "Linear Regression", "Continuous crop health score (0-100)"),
                  _buildPracticalRow("P07", "Decision Tree & k-NN", "Operational risk status classification"),
                  _buildPracticalRow("P08", "K-Means Clustering", "Agro-ecological vulnerability zoning"),
                  _buildPracticalRow("P09", "Domain-Specific NLP", "Local farmer chatbot (Zero external LLMs)"),
                  _buildPracticalRow("P10", "Integrated Mini-Project", "Full-stack mobile + API system"),
                ],
              ),
            ),
            const SizedBox(height: 18),

            // Scientific Disclaimer
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFFFF3E0),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: const Color(0xFFFFB74D), width: 1.2),
              ),
              child: const Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.info_rounded, color: CropGuardTheme.warningOrange, size: 20),
                  SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      "Educational Decision-Support Disclaimer: CropGuard AI provides probabilistic risk advisories based on meteorological indicators. It is not an unconditional diagnosis or a substitute for on-site agricultural extension inspection.",
                      style: TextStyle(fontSize: 12, color: CropGuardTheme.textPrimary, height: 1.35),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildPracticalRow(String code, String tech, String role) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: CropGuardTheme.primary.withOpacity(0.12),
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(
              code,
              style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w800, color: CropGuardTheme.primaryDark),
            ),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(tech, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: CropGuardTheme.textPrimary)),
                Text(role, style: const TextStyle(fontSize: 11, color: CropGuardTheme.textSecondary)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
