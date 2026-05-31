#!/usr/bin/env bash

ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT/src/backend/VoteBem"
FRONTEND_DIR="$ROOT/src/frontend/VoteBem"
FRONTEND_PORT=3000
BACKEND_PORT=5253

# Mata processos filhos ao sair
cleanup() {
  echo ""
  echo "Encerrando serviços..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null
  wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null
  echo "Pronto."
}
trap cleanup EXIT INT TERM

# Verifica se a porta já está em uso
check_port() {
  lsof -ti :"$1" > /dev/null 2>&1 && echo "AVISO: porta $1 já está em uso." || true
}

check_port $BACKEND_PORT
check_port $FRONTEND_PORT

echo "Iniciando backend .NET na porta $BACKEND_PORT..."
dotnet run --project "$BACKEND_DIR" &
BACKEND_PID=$!

echo "Iniciando servidor frontend na porta $FRONTEND_PORT..."
python3 -m http.server $FRONTEND_PORT --directory "$FRONTEND_DIR" 2>&1 &
FRONTEND_PID=$!
sleep 1
if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
  echo "ERRO: servidor frontend falhou ao iniciar."
  kill "$BACKEND_PID" 2>/dev/null
  exit 1
fi

echo ""
echo "----------------------------------------------"
echo "  Backend:  http://localhost:$BACKEND_PORT"
echo "  Frontend: http://localhost:$FRONTEND_PORT/voto%20Consciente/candidatos.html"
echo "  Pressione Ctrl+C para encerrar tudo."
echo "----------------------------------------------"
echo ""

wait
