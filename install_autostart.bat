@echo off
setlocal EnableDelayedExpansion
title EduManage — অটো-স্টার্ট ইনস্টলার

echo.
echo ============================================================
echo    EduManage -- Windows অটো-স্টার্ট সেটআপ
echo    (Windows লগইন করলে স্বয়ংক্রিয়ভাবে চালু হবে)
echo ============================================================
echo.

:: বর্তমান ডিরেক্টরি
set "APP_DIR=%~dp0"
set "APP_DIR=%APP_DIR:~0,-1%"
set "LAUNCHER=%APP_DIR%\Start_EduManage.bat"
set "TASK_NAME=EduManage_AutoStart"

:: Python পাথ খোঁজা
set "PYTHON_EXE="
for %%p in (
    "%APP_DIR%\venv\Scripts\pythonw.exe"
    "%APP_DIR%\venv\Scripts\python.exe"
    "python.exe"
) do (
    if exist %%~p (
        set "PYTHON_EXE=%%~p"
        goto :found_python
    )
)

:found_python
if "!PYTHON_EXE!"=="" (
    echo [ত্রুটি] Python খুঁজে পাওয়া যায়নি!
    echo venv সক্রিয় করে আবার চেষ্টা করুন।
    pause
    exit /b 1
)

echo [তথ্য] অ্যাপ ফোল্ডার: %APP_DIR%
echo [তথ্য] Python: !PYTHON_EXE!
echo.

:: পুরনো টাস্ক থাকলে মুছে দেওয়া
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

:: নতুন Task Scheduler টাস্ক তৈরি
:: লগইনে একবার চলবে, ইন্টারেক্টিভ মোড
schtasks /create ^
    /tn "%TASK_NAME%" ^
    /tr "\"!PYTHON_EXE!\" \"%APP_DIR%\launcher.py\"" ^
    /sc ONLOGON ^
    /rl HIGHEST ^
    /delay 0000:30 ^
    /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo  ✅ সফল! EduManage এখন Windows লগইনে স্বয়ংক্রিয় চালু হবে।
    echo.
    echo  টাস্কের নাম: %TASK_NAME%
    echo  অপসারণ করতে: uninstall_autostart.bat চালান
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo  ❌ ব্যর্থ! অ্যাডমিন হিসেবে চালানোর চেষ্টা করুন।
    echo  এই ফাইলটি Right-click করে "Run as administrator" বেছে নিন।
    echo ============================================================
)

echo.
pause
