@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
python auto_backup_drive.py
echo Backup finished.
