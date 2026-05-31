"""Busca semântica em PROPOSTA_CHUNK via pgvector.

Retorna chunks ordenados por similaridade cosseno (1 - distância).
"""
from typing import Any

import numpy as np
from psycopg2.extras import RealDictCursor

from db import get_connection
from embeddings import embed


def search_chunks(
    query: str,
    sq_candidatos: list[int] | None = None,
    k: int = 6,
    min_similarity: float = 0.20,
) -> list[dict[str, Any]]:
    """Top-K chunks mais próximos da query, opcionalmente filtrados por candidato.

    min_similarity: corta resultados ruins (cosseno < 0.30 raramente são úteis
    em pt-BR com MiniLM-L12-v2). Devolve dicts com:
    sq_candidato, ano_eleicao, idx, texto, nm_urna_candidato,
    nm_candidato, similaridade.
    """
    q_emb = np.asarray(embed(query), dtype=np.float32)

    sql = """
        SELECT pc.sq_candidato,
               pc.ano_eleicao,
               pc.idx,
               pc.texto,
               c.nm_urna_candidato,
               cand.nm_candidato,
               1 - (pc.embedding <=> %s::vector) AS similaridade
          FROM proposta_chunk pc
          JOIN candidatura c ON c.sq_candidato = pc.sq_candidato
          JOIN candidato cand ON cand.nr_cpf_candidato = c.nr_cpf_candidato
    """
    params: list[Any] = [q_emb]

    if sq_candidatos:
        sql += " WHERE pc.sq_candidato = ANY(%s)"
        params.append(sq_candidatos)

    sql += " ORDER BY pc.embedding <=> %s::vector LIMIT %s"
    params.extend([q_emb, k])

    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]
        cur.close()
    finally:
        conn.close()

    return [r for r in rows if r["similaridade"] >= min_similarity]
