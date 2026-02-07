@echo off
echo Starting the backend server...

REM Change to the backend directory
cd /d "%~dp0backend"

echo Checking if virtual environment exists...
IF NOT EXIST "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating the virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Check if NeonDB URL is set, if not use SQLite
IF NOT DEFINED NEON_DB_URL (
    echo Using SQLite database (fallback for development)
) ELSE (
    echo Using NeonDB database
)

echo Starting FastAPI server on http://localhost:8000...
echo Make sure no other process is using port 8000
echo Press Ctrl+C to stop the server
python main.py

echo.
echo Server stopped.
pause