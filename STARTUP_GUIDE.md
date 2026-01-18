# Startup Guide

This guide explains how to properly start both the backend and frontend servers to avoid connection errors.

## Prerequisites

- Python 3.8+ installed
- Node.js and npm installed
- Ensure ports 8000 (backend) and 3000 (frontend) are available

## Quick Start (Recommended)

### Full Stack Startup
Run the automated script to start both servers:
```bash
start-full-stack.bat
```

This will open separate command windows for both backend and frontend servers.

### Backend Only
To start just the backend server:
```bash
start-backend.bat
```

## Manual Setup

### Starting the Backend Server

1. Open a command prompt and navigate to the backend directory:
```bash
cd E:\h-2\backend
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies (first time only):
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
python main.py
```
or
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Starting the Frontend Server

1. Open a new command prompt (do not close the backend server)
2. Navigate to the frontend directory:
```bash
cd E:\h-2\frontend
```

3. Install dependencies (first time only):
```bash
npm install
```

4. Start the frontend server:
```bash
npm run dev
```

## Troubleshooting

### "Failed to connect to the server" Error
This error occurs when the frontend cannot connect to the backend server. Solutions:

1. Make sure the backend server is running on port 8000
2. Verify that no firewall is blocking connections
3. Check that the backend server is accessible at http://localhost:8000
4. Run the check-backend.py script to diagnose issues:
```bash
python check-backend.py
```

### Port Already in Use
If you get "port already in use" errors:
1. Find processes using the port:
```bash
netstat -ano | findstr :8000
```
2. Kill the process if needed:
```bash
taskkill /PID <process-id> /F
```

### Virtual Environment Issues
If you encounter Python package errors:
1. Recreate the virtual environment:
```bash
cd E:\h-2\backend
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables
The backend requires certain environment variables to be set. The application includes fallback to SQLite if NeonDB is unavailable. For development, the SQLite fallback should work fine.

## Connection Logic

The frontend automatically attempts to connect to the backend using multiple possible URLs:
- `http://localhost:8000` (primary)
- `http://127.0.0.1:8000`
- `http://host.docker.internal:8000` (for Docker environments)

The first accessible URL will be used for subsequent requests. Enhanced timeout handling prevents hanging connections.