@echo off
echo Setting up and starting the full application stack...

echo.
echo =============================================
echo Starting Backend Server
echo =============================================
echo.

REM Start backend in a new command window
start "Backend Server" cmd /k "cd /d E:\h-2\backend && call venv\Scripts\activate.bat && python main.py"

timeout /t 5 /nobreak >nul

echo.
echo =============================================
echo Starting Frontend Server
echo =============================================
echo.

REM Start frontend in another command window
start "Frontend Server" cmd /k "cd /d E:\h-2\frontend && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Note: Close this window when you're done.
pause