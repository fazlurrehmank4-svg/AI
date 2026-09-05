@echo off
echo ============================================================
echo CropGuard AI: Flutter Android Release APK Build Script
echo ============================================================

cd Flutter_App\weather_crop_health_app
echo [1/3] Fetching Flutter dependencies...
call flutter pub get

echo [2/3] Analyzing Flutter codebase...
call flutter analyze

echo [3/3] Building Release Android APK...
call flutter build apk --release

echo ============================================================
echo Build Process Finished!
echo APK Output Location:
echo Flutter_App\weather_crop_health_app\build\app\outputs\flutter-apk\app-release.apk
echo ============================================================
pause
