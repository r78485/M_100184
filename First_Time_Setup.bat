@echo off
title EduManage — প্যাকেজ ইনস্টল করছে...

set "APP_DIR=%~dp0"
set "APP_DIR=%APP_DIR:~0,-1%"
set "PIP=%APP_DIR%\venv\Scripts\pip.exe"

echo.
echo ============================================================
echo   EduManage — প্রয়োজনীয় প্যাকেজ ইনস্টল হচ্ছে
echo ============================================================
echo.

if not exist "%PIP%" (
    echo [ত্রুটি] venv\Scripts\pip.exe খুঁজে পাওয়া যায়নি!
    pause
    exit /b 1
)

echo reportlab ইনস্টল হচ্ছে...
"%PIP%" install reportlab pillow qrcode python-barcode

echo.
echo সব requirements ইনস্টল হচ্ছে...
"%PIP%" install -r "%APP_DIR%\requirements.txt"

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ সব প্যাকেজ সফলভাবে ইনস্টল হয়েছে!
) else (
    echo ⚠️  কিছু প্যাকেজ ইনস্টলে সমস্যা হয়েছে। উপরের বার্তা দেখুন।
)

echo.
echo এখন মাইগ্রেশন চালাচ্ছে...
"%APP_DIR%\venv\Scripts\python.exe" "%APP_DIR%\manage.py" migrate

echo.
echo ✅ সম্পন্ন! এখন Start_EduManage.bat চালান।
echo.
pause
