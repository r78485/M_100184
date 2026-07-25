@echo off
setlocal EnableDelayedExpansion
title EduManage — অফলাইন সিস্টেম চলছে...

set "APP_DIR=%~dp0"
set "APP_DIR=%APP_DIR:~0,-1%"

echo.
echo ============================================================
echo   EduManage -- অফলাইন স্কুল ম্যানেজমেন্ট সিস্টেম
echo   অনলাইন ব্যাকআপ: https://m-100184.onrender.com
echo ============================================================
echo.

:: Python খোঁজা (venv অগ্রাধিকার)
set "PYTHON_EXE="
for %%p in (
    "%APP_DIR%\venv\Scripts\pythonw.exe"
    "%APP_DIR%\venv\Scripts\python.exe"
    "python"
) do (
    if exist %%~p (
        set "PYTHON_EXE=%%~p"
        goto :found
    )
)
:: PATH থেকে python নেওয়া
set "PYTHON_EXE=python"

:found
echo [তথ্য] Python: !PYTHON_EXE!
echo [তথ্য] চালু হচ্ছে...
echo.

:: Launcher চালানো (এটি সার্ভার + সিঙ্ক + ব্রাউজার সব চালু করে)
"!PYTHON_EXE!" "%APP_DIR%\launcher.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ত্রুটি] চালু করা যায়নি। নিচের কারণ হতে পারে:
    echo   - Python ইনস্টল নেই
    echo   - venv সেটআপ করা হয়নি
    echo   - requirements ইনস্টল করা হয়নি
    echo.
    echo সমাধান: venv\Scripts\activate চালিয়ে pip install -r requirements.txt দিন
    pause
)
