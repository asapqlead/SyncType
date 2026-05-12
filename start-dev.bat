@echo off
REM SyncType Development Startup Script for Windows
echo.
echo Starting SyncType Development Environment...
echo.

REM Check if we're in the right directory
if not exist "backend\" (
    echo Error: Please run this script from the synctype-integrated directory
    pause
    exit /b 1
)

if not exist "frontend\" (
    echo Error: Please run this script from the synctype-integrated directory
    pause
    exit /b 1
)

echo Starting Backend (FastAPI)...
echo Backend will run on http://localhost:8000
echo.

REM Start backend in new window
cd backend
if not exist ".venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate
)

start "SyncType Backend" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
cd ..

timeout /t 3 /nobreak >nul

echo.
echo Starting Frontend (Vite + React)...
echo Frontend will run on http://localhost:5173
echo.

REM Start frontend in new window
cd frontend
if not exist "node_modules\" (
    echo Node modules not found. Installing...
    call npm install
)

start "SyncType Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ==========================================
echo    SyncType is running!
echo ==========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:5173
echo API Docs:    http://localhost:8000/docs
echo.
echo Press any key to open the frontend in your browser...
pause >nul

start http://localhost:5173

echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause
