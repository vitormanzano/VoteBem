"""Métricas de recuperação do Tier B (RAG) — Recall@K e Precision@K.

Para cada pergunta do tipo "proposta" no dataset, chama diretamente
vector_search.search_chunks() (SEM passar pelo LLM) e mede:

    - Hit@K: pelo menos um chunk de algum candidato esperado apareceu nos top-K?
    - Recall@K (por candidato): para cada candidato esperado, apareceu um
      chunk dele nos top-K? (média sobre todos os candidatos esperados)
    - Precision@K: dos K chunks retornados, quantos pertencem a algum
      candidato esperado? (média sobre as perguntas)

O ground-truth (sq_candidato esperado) é resolvido em tempo de execução a
partir do campo `candidato_esperado` do dataset, consultando o banco. Isso
trata automaticamente candidatos com múltiplas candidaturas (anos diferentes).

Uso (precisa do banco rodando — não precisa do FastAPI):
    .venv/bin/python src/ai/eval/metrics_retrieval.py
    .venv/bin/python src/ai/eval/metrics_retrieval.py --k 1,3,5,10
    .venv/bin/python src/ai/eval/metrics_retrieval.py --json out.json
"""
import argparse
import json
import sys
import time
from pathlib import Path

# permite importar módulos de src/ai sem instalar como pacote
SRC_AI = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC_AI))

from db import get_connection  # noqa: E402
from retrieval.vector_search import search_chunks  # noqa: E402

DATASET = Path(__file__).resolve().parent / "dataset.jsonl"

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
    return [i for i in items if i.get("tipo") == "proposta"]


def sq_candidatos_por_nome(termo: str) -> list[int]:
    """Resolve nome de urna -> todos os sq_candidato (todas as eleições).

    Usa ILIKE para tolerância a acento, caixa e nomes parciais.
    """
    pattern = f"%{termo.strip()}%"
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT DISTINCT c.sq_candidato
              FROM candidatura c
             WHERE c.ds_cargo = 'PRESIDENTE'
               AND c.nm_urna_candidato ILIKE %s
            """,
            (pattern,),
        )
        rows = [r[0] for r in cur.fetchall()]
        cur.close()
    finally:
        conn.close()
    return rows


def resolver_gabarito(candidato_esperado: str) -> dict[str, list[int]]:
    """'LULA|BOLSONARO' -> {'LULA': [sq1, sq2], 'BOLSONARO': [sq3, ...]}"""
    nomes = [n.strip() for n in candidato_esperado.split("|") if n.strip()]
    return {n: sq_candidatos_por_nome(n) for n in nomes}


def avaliar_item(item: dict, ks: list[int]) -> dict:
    """Mede Hit@K, Recall@K (por candidato) e Precision@K para uma pergunta."""
    pergunta = item["pergunta"]
    esperado_str = item.get("candidato_esperado", "")
    gabarito = resolver_gabarito(esperado_str)

    sq_relevantes: set[int] = set()
    for sqs in gabarito.values():
        sq_relevantes.update(sqs)

    candidatos_vazios = [n for n, sqs in gabarito.items() if not sqs]

    k_max = max(ks)
    chunks = search_chunks(pergunta, sq_candidatos=None, k=k_max, min_similarity=0.0)

    resultado_por_k: dict[int, dict] = {}
    for k in ks:
        topk = chunks[:k]
        sq_topk = [c["sq_candidato"] for c in topk]

        n_relevantes_topk = sum(1 for sq in sq_topk if sq in sq_relevantes)
        precisao = n_relevantes_topk / k if k > 0 else 0.0
        hit = n_relevantes_topk > 0

        recalls_por_candidato = {}
        for nome, sqs in gabarito.items():
            if not sqs:
                continue
            achou = any(sq in sqs for sq in sq_topk)
            recalls_por_candidato[nome] = 1.0 if achou else 0.0
        recall_macro = (
            sum(recalls_por_candidato.values()) / len(recalls_por_candidato)
            if recalls_por_candidato else 0.0
        )

        resultado_por_k[k] = {
            "hit": hit,
            "precision": precisao,
            "recall_macro": recall_macro,
            "recalls_por_candidato": recalls_por_candidato,
        }

    return {
        "id": item["id"],
        "pergunta": pergunta,
        "candidatos_esperados": list(gabarito.keys()),
        "candidatos_sem_match_no_banco": candidatos_vazios,
        "n_chunks_retornados": len(chunks),
        "por_k": resultado_por_k,
    }


def imprimir_tabela_agregada(resultados: list[dict], ks: list[int]) -> dict:
    """Calcula e imprime médias agregadas. Retorna dict com os números."""
    print(cor("\nMÉTRICAS AGREGADAS DE RECUPERAÇÃO", BOLD))
    print(f"{'K':>4}{'Hit@K':>12}{'Recall@K':>14}{'Precision@K':>16}")
    print(cor("-" * 46, CINZA))

    agregado: dict[int, dict] = {}
    n = len(resultados)
    if n == 0:
        print(cor("  (sem perguntas avaliadas)", VERMELHO))
        return {}

    for k in ks:
        hit = sum(1 for r in resultados if r["por_k"][k]["hit"]) / n
        recall = sum(r["por_k"][k]["recall_macro"] for r in resultados) / n
        precision = sum(r["por_k"][k]["precision"] for r in resultados) / n
        agregado[k] = {"hit": hit, "recall": recall, "precision": precision}
        print(
            f"{k:>4}"
            f"{hit*100:>11.1f}%"
            f"{recall*100:>13.1f}%"
            f"{precision*100:>15.1f}%"
        )
    return agregado


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", default="1,3,5,10", help="Valores de K, separados por vírgula")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--json", dest="out_json", default=None)
    args = ap.parse_args()

    ks = sorted({int(x) for x in args.k.split(",") if x.strip()})
    itens = carregar_dataset()
    if args.limit:
        itens = itens[: args.limit]

    print(cor(f"\n{len(itens)} perguntas tipo=proposta — K={ks}\n", BOLD))

    resultados = []
    inicio = time.time()

    for i, item in enumerate(itens, 1):
        print(f"[{i:2d}/{len(itens)}] {item['id']} esperado={cor(item.get('candidato_esperado',''), AMARELO)}")
        try:
            r = avaliar_item(item, ks)
        except Exception as e:  # noqa: BLE001
            print(f"     {cor('FAIL', VERMELHO)} {type(e).__name__}: {e}")
            continue

        resultados.append(r)
        if r["candidatos_sem_match_no_banco"]:
            print(f"     {cor('aviso:', AMARELO)} sem match no banco para {r['candidatos_sem_match_no_banco']}")

        marcas = []
        for k in ks:
            d = r["por_k"][k]
            mark = cor(f"K={k}:hit", VERDE) if d["hit"] else cor(f"K={k}:miss", VERMELHO)
            marcas.append(f"{mark} p={d['precision']*100:.0f}% r={d['recall_macro']*100:.0f}%")
        print(f"     {' | '.join(marcas)}")

    duracao = time.time() - inicio
    agregado = imprimir_tabela_agregada(resultados, ks)

    print(cor("\nRESUMO", BOLD))
    print(f"  perguntas avaliadas: {len(resultados)}")
    print(f"  duração: {duracao:.1f}s ({duracao/max(len(resultados),1):.2f}s/pergunta)")

    if args.out_json:
        Path(args.out_json).write_text(json.dumps({
            "ks": ks,
            "agregado": agregado,
            "por_item": resultados,
            "duracao_segundos": duracao,
        }, indent=2, ensure_ascii=False))
        print(cor(f"\nmétricas salvas em {args.out_json}", CINZA))

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
