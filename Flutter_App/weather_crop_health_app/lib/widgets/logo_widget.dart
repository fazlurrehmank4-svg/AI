import 'package:flutter/material.dart';
import '../theme.dart';

class CropGuardLogo extends StatelessWidget {
  final double size;
  final bool showText;
  final bool isDark;

  const CropGuardLogo({
    Key? key,
    this.size = 64,
    this.showText = true,
    this.isDark = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        CustomPaint(
          size: Size(size, size),
          painter: _LogoPainter(),
        ),
        if (showText) ...[
          const SizedBox(height: 10),
          Text(
            "CropGuard AI",
            style: TextStyle(
              fontSize: size * 0.32,
              fontWeight: FontWeight.w800,
              letterSpacing: -0.5,
              color: isDark ? Colors.white : CropGuardTheme.primaryDark,
            ),
          ),
          const SizedBox(height: 3),
          Text(
            "Weather-Based Crop Health Predictor",
            style: TextStyle(
              fontSize: size * 0.16,
              fontWeight: FontWeight.w500,
              color: isDark ? Colors.white70 : CropGuardTheme.textSecondary,
              letterSpacing: 0.2,
            ),
          ),
        ],
      ],
    );
  }
}

class _LogoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;

    // 1. Background Shield / Rounded Hexagon with Gradient
    final rect = Rect.fromLTWH(0, 0, w, h);
    final bgPaint = Paint()
      ..shader = const LinearGradient(
        colors: [Color(0xFF1B5E20), Color(0xFF2E7D32), Color(0xFF4CAF50)],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ).createShader(rect);

    final rrect = RRect.fromRectAndRadius(rect, Radius.circular(w * 0.28));
    canvas.drawRRect(rrect, bgPaint);

    // 2. Weather Element (Sun Accent in top-right)
    final sunPaint = Paint()
      ..color = const Color(0xFFFFD54F)
      ..style = PaintingStyle.fill;
    canvas.drawCircle(Offset(w * 0.72, h * 0.28), w * 0.14, sunPaint);

    // 3. Central Stylized Leaf (Vibrant Mint)
    final leafPath = Path();
    leafPath.moveTo(w * 0.50, h * 0.22);
    leafPath.cubicTo(w * 0.78, h * 0.35, w * 0.78, h * 0.72, w * 0.50, h * 0.82);
    leafPath.cubicTo(w * 0.22, h * 0.72, w * 0.22, h * 0.35, w * 0.50, h * 0.22);
    leafPath.close();

    final leafPaint = Paint()
      ..color = const Color(0xFFE8F5E9)
      ..style = PaintingStyle.fill;
    canvas.drawPath(leafPath, leafPaint);

    // 4. Digital AI Neural / Network Nodes inside leaf
    final aiLinePaint = Paint()
      ..color = const Color(0xFF2E7D32)
      ..strokeWidth = w * 0.035
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    // Central Stem
    canvas.drawLine(Offset(w * 0.50, h * 0.32), Offset(w * 0.50, h * 0.75), aiLinePaint);
    // Neural Branch Left
    canvas.drawLine(Offset(w * 0.50, h * 0.48), Offset(w * 0.36, h * 0.42), aiLinePaint);
    // Neural Branch Right
    canvas.drawLine(Offset(w * 0.50, h * 0.58), Offset(w * 0.64, h * 0.52), aiLinePaint);

    // AI Node Dots
    final nodePaint = Paint()
      ..color = const Color(0xFF1B5E20)
      ..style = PaintingStyle.fill;

    canvas.drawCircle(Offset(w * 0.36, h * 0.42), w * 0.045, nodePaint);
    canvas.drawCircle(Offset(w * 0.64, h * 0.52), w * 0.045, nodePaint);
    canvas.drawCircle(Offset(w * 0.50, h * 0.32), w * 0.045, nodePaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
