@echo off
echo ========================================
echo   Digital Game Marketplace Starter
echo ========================================
echo.

REM Check if this is first run (seed database)
if "%1"=="--seed" (
    echo [1/3] Seeding database...
    python -m backend.seed_data
    echo.
)

echo [2/3] Starting Backend Server...
start "Backend Server" cmd /k "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak > nul

echo [3/3] Starting Frontend Server...
cd frontend
start "Frontend Server" cmd /k "npm run dev"

echo.
echo ========================================
echo   Servers are starting...
echo ========================================
echo.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/docs
echo.
echo   Test Accounts:
echo     Admin:   admin / admin123
echo     Player:  player / player123
echo     Dev:     rockstar_games / dev123
echo.
echo ========================================
