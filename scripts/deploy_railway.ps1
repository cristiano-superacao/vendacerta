param(
    [switch]$SkipLogin
)

Write-Host "=================================================="
Write-Host "Deploy VendaCerta no Railway (Windows/PowerShell)"
Write-Host "=================================================="

# 1) Verificar CLI do Railway
$railway = Get-Command railway -ErrorAction SilentlyContinue
if (-not $railway) {
    Write-Host "Railway CLI não encontrado. Tentando instalar via npm..."
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $npm) {
        Write-Error "npm não encontrado. Instale Node.js (https://nodejs.org) ou instale o Railway CLI manualmente."
        exit 1
    }
    npm install -g @railway/cli
    $railway = Get-Command railway -ErrorAction SilentlyContinue
    if (-not $railway) {
        Write-Error "Falha ao instalar Railway CLI. Tente instalar manualmente: npm i -g @railway/cli"
        exit 1
    }
}

# 2) Login (se não pulado)
if (-not $SkipLogin) {
    Write-Host "Efetuando login no Railway (abrirá o navegador)..."
    railway login
}

# 3) Linkar projeto ao Railway (selecionar workspace/projeto no prompt)
Write-Host "Linkando projeto atual ao Railway..."
railway link

# 4) Subir deploy
Write-Host "Enviando deploy (railway up)..."
railway up

Write-Host "Finalizado. Teste sua URL pública: /ping e /login."
