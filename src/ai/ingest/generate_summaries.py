"""Gera RESUMO_PROPOSTA para cada (candidato × tema) usando os chunks
indexados em PROPOSTA_CHUNK.

Idempotente: pula combinações já presentes em RESUMO_PROPOSTA.
Pode rodar em fatias com --limit / --only-sq / --only-tema.
Retry agressivo em rate limit (429): tenta extrair o tempo de espera
da mensagem do Groq e dorme antes de tentar de novo.

Uso:
    .venv/bin/python src/ai/ingest/generate_summaries.py
    .venv/bin/python src/ai/ingest/generate_summaries.py --limit 2
    .venv/bin/python src/ai/ingest/generate_summaries.py --model llama-3.1-8b-instant
    .venv/bin/python src/ai/ingest/generate_summaries.py --only-sq 280001607829
"""
import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import config
from db import get_connection
from llm import chat_completion
from retrieval.vector_search import search_chunks

SYSTEM_RESUMO = (
    "Você resume propostas de governo extraídas de PDFs oficiais do TSE. "
    "Use APENAS os trechos fornecidos — não invente, não traga conhecimento externo. "
    "Se os trechos NÃO tratarem do tema solicitado, responda EXATAMENTE: "
    "Não consta proposta sobre este tema. "
    "Caso contrário, gere de 3 a 5 bullets curtos (uma frase cada, "
    "no máximo 25 palavras), em português brasileiro simples, sem opinião. "
    "Não cite [N], não use markdown, apenas \"- \" como marcador."
)

CHUNKS_POR_TEMA = 8
MAX_TOKENS_RESUMO = 400
RATE_LIMIT_PADRAO_S = 90.0
SEM_PROPOSTA = "Não consta proposta sobre este tema"


def parse_retry_seconds(msg: str) -> float:
    """Extrai 'try again in Xm Ys' / 'in X.Ys' da mensagem de erro do Groq."""
    m = re.search(r"try again in\s+(?:(\d+)m)?\s*([\d.]+)s", msg)
    if not m:
        return RATE_LIMIT_PADRAO_S
    minutos = int(m.group(1) or 0)
    segundos = float(m.group(2))
    return minutos * 60 + segundos + 2  # margem de 2s


def gerar_resumo(sq_candidato: int, tema: str, model: str | None) -> str:
    chunks = search_chunks(
        f"propostas sobre {tema}",
        sq_candidatos=[sq_candidato],
        k=CHUNKS_POR_TEMA,
        min_similarity=0.0,
    )
    if not chunks:
        return SEM_PROPOSTA

    contexto = "\n\n---\n".join(c["texto"] for c in chunks)
    prompt = f"Tema: {tema}\n\nTrechos das propostas:\n\n{contexto}\n\nResuma."

    completion = chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_RESUMO},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=MAX_TOKENS_RESUMO,
        model=model,
    )
    return (completion.choices[0].message.content or "").strip() or SEM_PROPOSTA


def upsert_resumo(cur, sq_candidato: int, tema: str, resumo: str) -> None:
    cur.execute(
        "DELETE FROM resumo_proposta WHERE sq_candidato = %s AND ds_tema = %s",
        (sq_candidato, tema),
    )
    cur.execute(
        """INSERT INTO resumo_proposta (sq_candidato, ds_tema, tx_resumo, dt_geracao)
           VALUES (%s, %s, %s, NOW())""",
        (sq_candidato, tema, resumo),
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", help="Override de GROQ_MODEL para esta execução")
    ap.add_argument("--limit", type=int, default=None,
                    help="Processar no máximo N candidatos")
    ap.add_argument("--only-sq", type=int, default=None,
                    help="Processar apenas este sq_candidato")
    ap.add_argument("--only-tema", type=str, default=None,
                    help="Processar apenas este tema (deve estar em config.TEMAS)")
    ap.add_argument("--force", action="store_true",
                    help="Reprocessa mesmo se já existir resumo no banco")
    args = ap.parse_args()

    temas = config.TEMAS
    if args.only_tema:
        if args.only_tema not in temas:
            print(f"Tema '{args.only_tema}' não está em config.TEMAS: {temas}")
            return 2
        temas = [args.only_tema]

    conn = get_connection()
    cur = conn.cursor()

    n_temas = len(temas)
    if args.only_sq:
        cur.execute(
            "SELECT DISTINCT sq_candidato FROM proposta_chunk WHERE sq_candidato = %s",
            (args.only_sq,),
        )
        sqs = [r[0] for r in cur.fetchall()]
    else:
        # lista os candidatos que AINDA têm temas pendentes,
        # ordenando primeiro os com mais lacunas (faz quem está zerado antes)
        cur.execute("""
            SELECT pc.sq_candidato,
                   COALESCE(rp.temas_feitos, 0) AS feitos
              FROM (SELECT DISTINCT sq_candidato FROM proposta_chunk) pc
              LEFT JOIN (
                  SELECT sq_candidato, COUNT(DISTINCT ds_tema) AS temas_feitos
                    FROM resumo_proposta
                   GROUP BY sq_candidato
              ) rp ON rp.sq_candidato = pc.sq_candidato
             WHERE COALESCE(rp.temas_feitos, 0) < %s OR %s
             ORDER BY feitos ASC, pc.sq_candidato
        """, (n_temas, args.force))
        sqs = [r[0] for r in cur.fetchall()]
    if args.limit:
        sqs = sqs[: args.limit]

    total = len(sqs) * len(temas)
    print(f"Candidatos: {len(sqs)}  |  Temas: {len(temas)}  |  Combinações: {total}")
    if args.model:
        print(f"Modelo (override): {args.model}")

    feitos = 0
    pulados = 0
    falhas: list[tuple[int, str, str]] = []
    sem_chunks = 0

    for sq in sqs:
        for tema in temas:
            if not args.force:
                cur.execute(
                    "SELECT 1 FROM resumo_proposta WHERE sq_candidato=%s AND ds_tema=%s LIMIT 1",
                    (sq, tema),
                )
                if cur.fetchone():
                    pulados += 1
                    continue

            tentativas = 0
            while True:
                tentativas += 1
                try:
                    resumo = gerar_resumo(sq, tema, args.model)
                    break
                except Exception as e:
                    msg = str(e)
                    if "429" in msg or "rate_limit" in msg.lower():
                        if tentativas >= 2:
                            print(f"  [erro] sq={sq} {tema}: rate limit persistente, pulando")
                            falhas.append((sq, tema, "rate_limit"))
                            resumo = None
                            break
                        wait = parse_retry_seconds(msg)
                        print(f"  [rate limit] aguardando {wait:.0f}s antes de retry…")
                        time.sleep(wait)
                        continue
                    print(f"  [erro] sq={sq} {tema}: {e}")
                    falhas.append((sq, tema, str(e)[:80]))
                    resumo = None
                    break

            if resumo is None:
                continue

            if resumo == SEM_PROPOSTA:
                sem_chunks += 1

            upsert_resumo(cur, sq, tema, resumo)
            conn.commit()
            feitos += 1
            preview = resumo.splitlines()[0][:70] if resumo else ""
            print(f"  [{feitos+pulados+len(falhas):>3}/{total}] sq={sq} {tema:22s} → {preview!r}")

    cur.close()
    conn.close()

    print()
    print(f"Concluído: {feitos} novos, {pulados} já existiam, "
          f"{sem_chunks} sem dados sobre o tema, {len(falhas)} falhas")
    if falhas:
        print("Falhas:")
        for sq, tema, motivo in falhas[:10]:
            print(f"  sq={sq} tema={tema} → {motivo}")
        if len(falhas) > 10:
            print(f"  … e mais {len(falhas) - 10}")
    return 0 if not falhas else 1


if __name__ == "__main__":
    sys.exit(main())
