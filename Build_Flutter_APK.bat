@echo off
setlocal enableextensions enabledelayedexpansion
title Building EduManage Flutter Android APK...
echo ========================================================
echo        EduManage ERP - Flutter APK Builder
echo ========================================================
echo.

cd /d "%~dp0flutter_app"

echo Current Directory: %CD%
echo.

echo Checking Flutter installation...
where flutter >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Flutter is not found in PATH or has path parenthesis issue.
    echo.
    echo Easy Fix Steps:
    echo --------------------------------------------------------
    echo 1. Open PowerShell or Command Prompt.
    echo 2. Navigate to flutter_app folder:
    echo        cd f:\M_100184\flutter_app
    echo 3. Run:
    echo        flutter.bat pub get
    echo        flutter.bat build apk --release
    echo --------------------------------------------------------
    echo.
    pause
    exit /b 1
)

echo Fetching Flutter packages...
call flutter.bat pub get

echo.
echo Compiling Flutter APK (Release Mode)...
call flutter.bat build apk --release

if exist "build\app\outputs\flutter-apk\app-release.apk" (
    copy /y "build\app\outputs\flutter-apk\app-release.apk" "..\EduManage_Flutter_App.apk" >nul
    echo.
    echo ========================================================
    echo SUCCESS! Your Flutter APK has been created:
    echo File Location: f:\M_100184\EduManage_Flutter_App.apk
    echo ========================================================
) else if exist "build\app\outputs\apk\release\app-release.apk" (
    copy /y "build\app\outputs\apk\release\app-release.apk" "..\EduManage_Flutter_App.apk" >nul
    echo.
    echo ========================================================
    echo SUCCESS! Your Flutter APK has been created:
    echo File Location: f:\M_100184\EduManage_Flutter_App.apk
    echo ========================================================
) else (
    echo.
    echo Build command finished. Please check output above.
)

pause
