@echo off
echo Starting EduManage Offline System...
echo Please do not close this window while using the software.

:: Start Django Server in the background
start /b python manage.py runserver 127.0.0.1:8000

:: Wait for 3 seconds to let the server start
timeout /t 3 /nobreak > NUL

:: Open the default browser to the system page
start http://127.0.0.1:8000/
