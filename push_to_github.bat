@echo off
echo ========================================================
echo Pushing EduManage Project to GitHub...
echo Repository: https://github.com/r78485/M_100184.git
echo ========================================================

:: Ensure we are inside the project folder
cd /d "f:\M_100184"

git init
git remote remove origin 2>nul
git remote add origin https://github.com/r78485/M_100184.git
git branch -M main
git add .
git commit -m "Update EduManage ERP: Fees & Invoices delete features and NCTB subjects"
git pull origin main --rebase 2>nul
git push -u origin main --force

echo.
echo Done! Project pushed to GitHub successfully.
pause

