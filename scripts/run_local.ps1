Param(
  [string]$PgPassword = "postgres",
  [string]$PgDb = "vendacerta",
  [int]$PgPort = 5432
)

$ErrorActionPreference = 'Stop'

Write-Host "=== VendaCerta - Setup local (Windows) ===" -ForegroundColor Cyan

# 1) Verificar Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  Write-Error "Docker não encontrado no PATH. Instale Docker Desktop."
  exit 1
}

# 2) Subir PostgreSQL (se necessário)
$containerName = "vendacerta-pg"
$exists = docker ps -a --format '{{.Names}}' | Select-String -SimpleMatch $containerName
if (-not $exists) {
  Write-Host "Subindo PostgreSQL 17 em Docker..."
  docker run --name $containerName -e POSTGRES_PASSWORD=$PgPassword -e POSTGRES_DB=$PgDb -p $PgPort:5432 -d postgres:17 | Out-Null
} else {
  $running = docker ps --format '{{.Names}}' | Select-String -SimpleMatch $containerName
  if (-not $running) {
    Write-Host "Iniciando container existente..."
    docker start $containerName | Out-Null
  } else {
    Write-Host "PostgreSQL já em execução."
  }
}

Write-Host "Aguardando PostgreSQL iniciar..."
Start-Sleep -Seconds 8

# 3) Ambiente Python
if (-not (Test-Path .\venv)) {
  Write-Host "Criando venv..."
  python -m venv venv
}
. .\venv\Scripts\Activate.ps1

Write-Host "Atualizando pip e instalando dependências..."
pip install --upgrade pip | Out-Null
pip install -r requirements.txt | Out-Null

# 4) Variáveis de ambiente
$env:DATABASE_URL = "postgresql://postgres:$PgPassword@localhost:$PgPort/$PgDb"
$env:ENABLE_EXCEL_CHECK = "0"
$env:RUN_DB_INIT_ON_START = "1"
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"

Write-Host "DATABASE_URL=$($env:DATABASE_URL)"

# 5) Corrigir schema e validar
Write-Host "Executando correção de schema..."
python .\fix_database_railway.py

Write-Host "Validando colunas em 'usuarios'..."
python .\scripts\check_schema.py
if ($LASTEXITCODE -ne 0) {
  Write-Warning "Schema ainda não está completo. Verifique logs acima."
}

# 6) Subir app (Flask)
Write-Host "Iniciando aplicação em http://localhost:5000 ..."
flask run
