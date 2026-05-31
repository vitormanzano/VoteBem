#!/usr/bin/env bash
#
# Restaura o banco VoteBem a partir de db/dumps/votebem.dump.
# Pula setup.py / extract_pdfs.py / generate_summaries.py — útil para
# colegas que querem testar sem esperar o pipeline completo.
#
# Uso:
#   scripts/restore_db.sh
#
# Pré-requisitos:
#   - docker compose já subiu o serviço VoteBem (`docker compose up -d`)
#   - .env com POSTGRES_USER e POSTGRES_DB_NAME preenchidos
#
set -euo pipefail

DUMP_LOCAL="db/dumps/votebem.dump"
CONTAINER="VoteBem"
DUMP_REMOTO="/tmp/votebem.dump"

if [[ ! -f "$DUMP_LOCAL" ]]; then
    echo "ERRO: dump não encontrado em $DUMP_LOCAL"
    echo "      peça pro Vitor o arquivo (~550KB)"
    exit 1
fi

if ! docker ps --filter "name=$CONTAINER" --format '{{.Names}}' | grep -q "$CONTAINER"; then
    echo "ERRO: container $CONTAINER não está rodando."
    echo "      rode 'docker compose up -d' antes."
    exit 1
fi

if [[ -f .env ]]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

PGUSER="${POSTGRES_USER:-postgres}"
PGDB="${POSTGRES_DB_NAME:-VoteBem}"

echo "==> copiando dump para o container..."
docker cp "$DUMP_LOCAL" "${CONTAINER}:${DUMP_REMOTO}"

echo "==> restaurando dentro do container (pode demorar 1-3 min)..."
docker exec "$CONTAINER" pg_restore \
    -U "$PGUSER" -d "$PGDB" \
    --clean --if-exists --no-owner --no-privileges \
    "$DUMP_REMOTO"

docker exec "$CONTAINER" rm "$DUMP_REMOTO"

echo
echo "==> validando..."
docker exec "$CONTAINER" psql -U "$PGUSER" -d "$PGDB" -c "
SELECT
  (SELECT COUNT(*) FROM candidatura)         AS candidaturas,
  (SELECT COUNT(*) FROM proposta_chunk)      AS chunks,
  (SELECT COUNT(*) FROM resumo_proposta)     AS resumos,
  (SELECT COUNT(DISTINCT sq_candidato)
     FROM resumo_proposta)                   AS candidatos_com_resumo;
"

echo
echo "✓ banco restaurado. próximos passos:"
echo "  1. crie src/ai/.env (cp src/ai/.env.example src/ai/.env) e preencha GROQ_API_KEY"
echo "  2. suba a IA: .venv/bin/uvicorn main:app --app-dir src/ai --port 8001"
echo "  3. suba o backend: cd src/backend/VoteBem && dotnet run --launch-profile http"
