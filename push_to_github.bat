@echo off
echo ========================================================
echo Pushing EduManage Project to GitHub...
echo Repository: https://github.com/r78485/M_100184.git
echo ========================================================

cd /d "%~dp0"

git init
git remote remove origin 2>nul
git remote add origin https://github.com/r78485/M_100184.git
git branch -M main
git add .
git commit -m "Fix Render SQLite missing table error with auto migration check on container start"
git push -u origin main

echo.
echo Done! Project pushed to GitHub successfully.
pause
