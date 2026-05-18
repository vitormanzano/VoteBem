"""Métricas de classificação do router (chat/router.py).

Chama router.classify(pergunta) DIRETO — sem passar pelo endpoint /ai/chat —
para isolar o desempenho do roteador. Cada item do dataset é uma chamada LLM
rápida (~1s, max 40 tokens) em vez do pipeline completo (10-30s).

Métricas calculadas a partir da matriz de confusão 4x4:
    - Acurácia global
    - Precisão, Recall, F1 por classe
    - Precisão, Recall, F1 macro (média entre as 4 classes)

Classes: estruturado, proposta, recusar, fora_escopo.

Uso (não precisa do FastAPI rodando, mas precisa do .env com GROQ_API_KEY):
    .venv/bin/python src/ai/eval/metrics_router.py
    .venv/bin/python src/ai/eval/metrics_router.py --limit 8
    .venv/bin/python src/ai/eval/metrics_router.py --json out.json
"""
import argparse
import json
import sys
import time
from pathlib import Path

SRC_AI = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC_AI))

from chat.router import classify  # noqa: E402

DATASET = Path(__file__).resolve().parent / "dataset.jsonl"
CLASSES = ["estruturado", "proposta", "recusar", "fora_escopo"]

ALIASES_MODELO = {
    "70b": "llama-3.3-70b-versatile",
    "8b": "llama-3.1-8b-instant",
}

VERDE = "\033[32m"
VERMELHO = "\033[31m"
AMARELO = "\033[33m"
CINZA = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


def cor(t: str, c: str) -> str:
    return f"{c}{t}{RESET}"


def carregar_dataset() -> list[dict]:
    items = []
    with open(DATASET) as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def metricas_por_classe(matriz: dict[str, dict[str, int]], classe: str) -> dict:
    tp = matriz[classe][classe]
    fp = sum(matriz[c][classe] for c in CLASSES if c != classe)
    fn = sum(matriz[classe][c] for c in CLASSES if c != classe)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1}


def imprimir_matriz(matriz: dict[str, dict[str, int]]) -> None:
    print(cor("\nMATRIZ DE CONFUSÃO", BOLD))
    print(cor("(linhas = esperado, colunas = previsto)\n", CINZA))

    larg_label = max(len(c) for c in CLASSES) + 2
    larg_col = 12

    cab = " " * larg_label + "".join(f"{c:>{larg_col}}" for c in CLASSES) + f"{'total':>{larg_col}}"
    print(cab)
    print(cor("-" * len(cab), CINZA))

    for esperado in CLASSES:
        linha = f"{esperado:<{larg_label}}"
        total = 0
        for previsto in CLASSES:
            v = matriz[esperado][previsto]
            total += v
            if esperado == previsto:
                linha += cor(f"{v:>{larg_col}}", VERDE)
            elif v > 0:
                linha += cor(f"{v:>{larg_col}}", VERMELHO)
            else:
                linha += f"{v:>{larg_col}}"
        linha += f"{total:>{larg_col}}"
        print(linha)


def imprimir_metricas(metricas: dict[str, dict], suporte: dict[str, int]) -> None:
    print(cor("\nMÉTRICAS POR CLASSE", BOLD))
    print(f"{'classe':<14}{'precisão':>11}{'recall':>11}{'F1':>11}{'suporte':>11}")
    print(cor("-" * 58, CINZA))
    for c in CLASSES:
        m = metricas[c]
        s = suporte[c]
        print(
            f"{c:<14}"
            f"{m['precision']*100:>10.1f}%"
            f"{m['recall']*100:>10.1f}%"
            f"{m['f1']*100:>10.1f}%"
            f"{s:>11d}"
        )

    macro_p = sum(metricas[c]["precision"] for c in CLASSES) / len(CLASSES)
    macro_r = sum(metricas[c]["recall"] for c in CLASSES) / len(CLASSES)
    macro_f1 = sum(metricas[c]["f1"] for c in CLASSES) / len(CLASSES)
    total_s = sum(suporte.values())
    print(cor("-" * 58, CINZA))
    print(
        f"{'macro avg':<14}"
        f"{macro_p*100:>10.1f}%"
        f"{macro_r*100:>10.1f}%"
        f"{macro_f1*100:>10.1f}%"
        f"{total_s:>11d}"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--json", dest="out_json", default=None)
    ap.add_argument(
        "--model",
        default=None,
        help="Override do modelo. Aceita alias '70b'/'8b' ou nome completo Groq. Default: o configurado no .env (GROQ_MODEL).",
    )
    args = ap.parse_args()

    modelo = ALIASES_MODELO.get(args.model, args.model) if args.model else None

    itens = carregar_dataset()
    if args.limit:
        itens = itens[: args.limit]

    rotulo = modelo or "default (.env)"
    print(cor(f"\n{len(itens)} perguntas — router.classify() em {rotulo}\n", BOLD))

    matriz = {esperado: {previsto: 0 for previsto in CLASSES} for esperado in CLASSES}
    suporte = {c: 0 for c in CLASSES}
    erros: list[dict] = []
    falhas = 0
    inicio = time.time()

    for i, item in enumerate(itens, 1):
        esperado = item["tipo"]
        if esperado not in CLASSES:
            continue
        suporte[esperado] += 1

        pergunta = item["pergunta"]
        print(f"[{i:2d}/{len(itens)}] esperado={cor(esperado, AMARELO):20s} {item['id']} {pergunta[:55]}")

        try:
            t0 = time.time()
            previsto = classify(pergunta, model=modelo)
            dt = time.time() - t0
        except Exception as e:  # noqa: BLE001
            print(f"     {cor('FAIL', VERMELHO)} {type(e).__name__}: {e}")
            falhas += 1
            continue

        matriz[esperado][previsto] += 1
        if esperado == previsto:
            print(f"     {cor('OK', VERDE)} ({dt:.1f}s) previsto={previsto}")
        else:
            print(f"     {cor('ERRO', VERMELHO)} ({dt:.1f}s) previsto={previsto}")
            erros.append({"id": item["id"], "esperado": esperado, "previsto": previsto, "pergunta": pergunta})

    duracao = time.time() - inicio

    imprimir_matriz(matriz)

    metricas = {c: metricas_por_classe(matriz, c) for c in CLASSES}
    imprimir_metricas(metricas, suporte)

    total = sum(suporte.values()) - falhas
    acertos = sum(matriz[c][c] for c in CLASSES)
    acuracia = acertos / total if total > 0 else 0.0

    print(cor("\nAGREGADO", BOLD))
    print(f"  acurácia global: {acuracia*100:.1f}%  ({acertos}/{total})")
    print(f"  falhas LLM:      {falhas}")
    print(f"  duração total:   {duracao:.1f}s ({duracao/max(total,1):.2f}s/pergunta)")

    if erros:
        print(cor("\nERROS DE CLASSIFICAÇÃO", BOLD))
        for e in erros:
            print(f"  {e['id']}: esperado={e['esperado']}, previsto={e['previsto']} — {e['pergunta'][:60]}")

    if args.out_json:
        Path(args.out_json).write_text(json.dumps({
            "modelo": rotulo,
            "matriz_confusao": matriz,
            "metricas_por_classe": metricas,
            "suporte": suporte,
            "acuracia": acuracia,
            "falhas_llm": falhas,
            "duracao_segundos": duracao,
            "erros": erros,
        }, indent=2, ensure_ascii=False))
        print(cor(f"\nmétricas salvas em {args.out_json}", CINZA))

    print()
    return 0 if not erros and falhas == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
