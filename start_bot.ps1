Write-Host "WhatsApp Reminder Bot - Startup Script" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

Write-Host "1. Activating Virtual Environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host "2. Starting ngrok tunnel (port 8000)..." -ForegroundColor Yellow
Write-Host "You will see the ngrok URL - COPY IT!" -ForegroundColor Cyan
Write-Host ""

Start-Process cmd -ArgumentList "/c ngrok http 8000"

Write-Host "3. Waiting 3 seconds for ngrok to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "4. Starting bot on http://localhost:8000" -ForegroundColor Yellow
Write-Host ""

python main.py

Write-Host ""
Write-Host "Bot stopped!" -ForegroundColor Red
