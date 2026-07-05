# FLINS-OS Setup (Windows PowerShell)
# Run with: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host "=== FLINS-OS Setup ===" -ForegroundColor Cyan

# 1. Python venv
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}
& .\venv\Scripts\Activate.ps1

# 2. Install deps
Write-Host "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Env file
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env - go fill in your GEMINI_API_KEY and other keys." -ForegroundColor Yellow
}

# 4. Vault check
New-Item -ItemType Directory -Force -Path "vault\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "vault\research" | Out-Null
New-Item -ItemType Directory -Force -Path "vault\projects" | Out-Null
Write-Host "vault mounted" -ForegroundColor Green

# 5. Skills check
$skillCount = (Get-ChildItem -Path "skills" -Filter "SKILL.md" -Recurse).Count
Write-Host "skills linked ($skillCount found)" -ForegroundColor Green

Write-Host ""
Write-Host "Setup done. Run:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1"
Write-Host "  python core\main.py"
