@echo off
title Building EduManage Android APK...
echo ========================================================
echo        EduManage ERP - Android APK Builder
echo ========================================================
echo.

cd /d "%~dp0android_app"

echo Checking Java / Android environment...
where java >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] Java / JDK is not installed or JAVA_HOME is not set.
    echo.
    echo Easy 1-Click Alternatives to get your APK:
    echo --------------------------------------------------------
    echo 1. Open Android Studio -> Open Project -> 'f:\M_100184\android_app'
    echo    Then click: Build -> Build Bundle(s) / APK(s) -> Build APK
    echo.
    echo 2. WebAPK / PWABuilder (Online 1-Click APK Generator):
    echo    Go to https://www.pwabuilder.com and paste your server URL to download signed APK!
    echo --------------------------------------------------------
    echo.
    pause
    exit /b 1
)

echo Building Android APK package...
call gradlew.bat assembleDebug

if exist "app\build\outputs\apk\debug\app-debug.apk" (
    copy /y "app\build\outputs\apk\debug\app-debug.apk" "..\EduManage_App.apk"
    echo.
    echo ========================================================
    echo SUCCESS! Your Android APK has been built:
    echo Location: f:\M_100184\EduManage_App.apk
    echo ========================================================
) else (
    echo.
    echo Build finished. If APK was generated, check:
    echo f:\M_100184\android_app\app\build\outputs\apk\debug\
)

pause
