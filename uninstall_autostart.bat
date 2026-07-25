@echo off
title EduManage — অটো-স্টার্ট অপসারণ

set "TASK_NAME=EduManage_AutoStart"

echo.
echo ============================================================
echo    EduManage -- অটো-স্টার্ট অপসারণ
echo ============================================================
echo.

schtasks /delete /tn "%TASK_NAME%" /f

if %ERRORLEVEL% EQU 0 (
    echo  ✅ সফল! EduManage অটো-স্টার্ট সরিয়ে দেওয়া হয়েছে।
) else (
    echo  ⚠️  টাস্ক পাওয়া যায়নি বা ইতিমধ্যে সরানো হয়েছে।
)

echo.
pause
