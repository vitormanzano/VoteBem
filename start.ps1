$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BACKEND_DIR = Join-Path $ROOT "src\backend\VoteBem"
$FRONTEND_DIR = Join-Path $ROOT "src\frontend\VoteBem"
$FRONTEND_PORT = 3000
$BACKEND_PORT  = 5253

# Verifica portas em uso
foreach ($port in @($BACKEND_PORT, $FRONTEND_PORT)) {
    $inUse = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($inUse) { Write-Warning "Porta $port ja esta em uso." }
}

Write-Host "Iniciando backend .NET na porta $BACKEND_PORT..."
$backend = Start-Process powershell -ArgumentList "-NoExit", "-Command",
    "dotnet run --project `"$BACKEND_DIR`"" -PassThru

Write-Host "Iniciando servidor frontend na porta $FRONTEND_PORT..."

# Tenta python3 primeiro, senão cai para python
$pythonCmd = if (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" } else { "python" }
$frontend = Start-Process powershell -ArgumentList "-NoExit", "-Command",
    "$pythonCmd -m http.server $FRONTEND_PORT --directory `"$FRONTEND_DIR`"" -PassThru

Write-Host ""
Write-Host "----------------------------------------------"
Write-Host "  Backend:  http://localhost:$BACKEND_PORT"
Write-Host "  Frontend: http://localhost:$FRONTEND_PORT/voto%20Consciente/candidatos.html"
Write-Host "  Feche esta janela para encerrar tudo."
Write-Host "----------------------------------------------"
Write-Host ""

try {
    Wait-Process -Id $backend.Id -ErrorAction SilentlyContinue
} finally {
    Stop-Process -Id $backend.Id  -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $frontend.Id -Force -ErrorAction SilentlyContinue
    Write-Host "Servicos encerrados."
}
