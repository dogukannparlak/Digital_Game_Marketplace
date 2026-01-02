# Digital Game Marketplace Starter Script
# Usage:
#   .\start_project.ps1           - Start servers only
#   .\start_project.ps1 -Seed     - Seed database and start servers

param(
    [switch]$Seed
)

Write-Host "========================================"
Write-Host "  Digital Game Marketplace Starter"
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Seed database if requested
if ($Seed) {
    Write-Host "[1/3] Seeding database..." -ForegroundColor Yellow
    python -m backend.seed_data
    Write-Host ""
}

# Start Backend
Write-Host "[2/3] Starting Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

Start-Sleep -Seconds 3

# Start Frontend
Write-Host "[3/3] Starting Frontend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

Write-Host ""
Write-Host "========================================"
Write-Host "  Servers are starting..."
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Backend:  " -NoNewline; Write-Host "http://localhost:8000" -ForegroundColor Blue
Write-Host "  Frontend: " -NoNewline; Write-Host "http://localhost:5173" -ForegroundColor Blue
Write-Host "  API Docs: " -NoNewline; Write-Host "http://localhost:8000/docs" -ForegroundColor Blue
Write-Host ""
Write-Host "  Test Accounts:" -ForegroundColor Yellow
Write-Host "    Admin:   admin / admin123"
Write-Host "    Player:  player / player123"
Write-Host "    Dev:     rockstar_games / dev123"
Write-Host ""
Write-Host "========================================"
