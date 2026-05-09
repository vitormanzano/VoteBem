"""REPL simples para conversar com o /ai/chat sem ter que montar curl.

Uso:
    .venv/bin/python src/ai/test_chat.py

Requer o uvicorn já rodando em http://127.0.0.1:8001.
Digite a pergunta e dê Enter. 'sair' (ou Ctrl+D) encerra.
"""
import json
import sys
import time
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8001/ai/chat"
HEALTH = "http://127.0.0.1:8001/health"


def cor(texto: str, codigo: str) -> str:
    return f"\033[{codigo}m{texto}\033[0m"


def perguntar(pergunta: str) -> dict:
    body = json.dumps({"pergunta": pergunta}).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def imprimir_resposta(d: dict, dt: float) -> None:
    cat = d.get("categoria") or "?"
    cor_cat = {"estruturado": "36", "proposta": "33", "recusar": "31", "fora_escopo": "35"}.get(cat, "37")
    print(f"\n{cor('categoria', '90')}: {cor(cat, cor_cat)}  {cor(f'({dt:.1f}s)', '90')}")
    print(f"{cor('resposta:', '32')}\n{d.get('resposta', '')}\n")
    fontes = d.get("fontes") or []
    if fontes:
        print(cor(f"fontes ({len(fontes)}):", "34"))
        for f in fontes:
            ref = f.get("ref")
            nome = f.get("nome", "?")
            ano = f.get("ano", "?")
            trecho = (f.get("trecho") or "").replace("\n", " ")
            print(f"  [{ref}] {nome} {ano}")
            print(f"      {cor(trecho[:160], '90')}")
    print(cor("─" * 60, "90"))


def main() -> int:
    # Confere se servidor está rodando
    try:
        with urllib.request.urlopen(HEALTH, timeout=3) as r:
            info = json.loads(r.read().decode("utf-8"))
        print(cor(f"conectado — modelo: {info.get('model')}", "32"))
    except (urllib.error.URLError, OSError) as e:
        print(cor(f"servidor não respondeu em {HEALTH}", "31"))
        print(cor("rode antes:  .venv/bin/uvicorn main:app --app-dir src/ai --port 8001", "90"))
        return 1

    print(cor("digite uma pergunta ('sair' ou Ctrl+D para encerrar)", "90"))
    print(cor("─" * 60, "90"))

    while True:
        try:
            pergunta = input(cor("pergunta> ", "1;36")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not pergunta:
            continue
        if pergunta.lower() in ("sair", "exit", "quit"):
            return 0

        t0 = time.time()
        try:
            resp = perguntar(pergunta)
        except urllib.error.HTTPError as e:
            print(cor(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')}", "31"))
            continue
        except Exception as e:
            print(cor(f"erro: {e}", "31"))
            continue
        imprimir_resposta(resp, time.time() - t0)


if __name__ == "__main__":
    sys.exit(main())
