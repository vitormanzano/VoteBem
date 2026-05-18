# Restaura o banco VoteBem a partir de db\dumps\votebem.dump.
# Equivalente ao restore_db.sh para colegas em Windows.
#
# Uso (PowerShell, na raiz do projeto):
#   .\scripts\restore_db.ps1
#
# Pré-requisitos:
#   - docker compose já subiu o serviço VoteBem  (docker compose up -d)
#   - .env (na raiz) com POSTGRES_USER e POSTGRES_DB_NAME preenchidos

$ErrorActionPreference = "Stop"

$ROOT       = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$DUMP_LOCAL = Join-Path $ROOT "db\dumps\votebem.dump"
$CONTAINER  = "VoteBem"
$DUMP_REMOTO = "/tmp/votebem.dump"

if (-not (Test-Path $DUMP_LOCAL)) {
    Write-Error "Dump não encontrado em $DUMP_LOCAL. Peça pro Vitor o arquivo (~550KB)."
    exit 1
}

$running = docker ps --filter "name=$CONTAINER" --format "{{.Names}}"
if (-not ($running -match "^$CONTAINER$")) {
    Write-Error "Container '$CONTAINER' não está rodando. Rode 'docker compose up -d' antes."
    exit 1
}

# Carrega .env da raiz (PowerShell não tem 'source')
$envFile = Join-Path $ROOT ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | Where-Object { $_ -match "^[A-Za-z_][A-Za-z0-9_]*=" } | ForEach-Object {
        $name, $value = $_.Split("=", 2)
        Set-Item -Path "Env:$name" -Value $value
    }
}

$PGUSER = if ($env:POSTGRES_USER) { $env:POSTGRES_USER } else { "postgres" }
$PGDB   = if ($env:POSTGRES_DB_NAME) { $env:POSTGRES_DB_NAME } else { "VoteBem" }

Write-Host "==> copiando dump para o container..."
docker cp "$DUMP_LOCAL" "${CONTAINER}:${DUMP_REMOTO}"

Write-Host "==> restaurando dentro do container (1-3 min)..."
docker exec $CONTAINER pg_restore `
    -U $PGUSER -d $PGDB `
    --clean --if-exists --no-owner --no-privileges `
    $DUMP_REMOTO

docker exec $CONTAINER rm $DUMP_REMOTO

Write-Host ""
Write-Host "==> validando..."
docker exec $CONTAINER psql -U $PGUSER -d $PGDB -c @"
SELECT
  (SELECT COUNT(*) FROM candidatura)         AS candidaturas,
  (SELECT COUNT(*) FROM proposta_chunk)      AS chunks,
  (SELECT COUNT(*) FROM resumo_proposta)     AS resumos,
  (SELECT COUNT(DISTINCT sq_candidato)
     FROM resumo_proposta)                   AS candidatos_com_resumo;
"@

Write-Host ""
Write-Host "OK - banco restaurado. Próximos passos:"
Write-Host "  1. crie src\ai\.env (Copy-Item src\ai\.env.example src\ai\.env) e preencha GROQ_API_KEY"
Write-Host "  2. suba a IA:    .venv\Scripts\Activate.ps1 ; uvicorn main:app --app-dir src\ai --port 8001"
Write-Host "  3. suba o backend: cd src\backend\VoteBem ; dotnet run --launch-profile http"
