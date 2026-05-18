"""Comparação de propostas de governo entre 2-4 candidatos (RF07).

Consome RESUMO_PROPOSTA pré-computado (Dia 6) — não chama o RAG em runtime.
Custo por tema: 1 chamada LLM com input pequeno (~2k tokens).
"""
from typing import Any

from psycopg2.extras import RealDictCursor

from chat.system_prompts import SYSTEM_PROMPT_BASE
from db import get_connection
from llm import chat_completion

SEM_PROPOSTA_MARK = "Não consta proposta sobre este tema"

SYSTEM_COMPARACAO = (
    SYSTEM_PROMPT_BASE
    + "\n\nVocê está COMPARANDO propostas de candidatos sobre UM tema. "
    "Use APENAS os resumos fornecidos. "
    "Estruture em 2-3 parágrafos curtos: (1) semelhanças, (2) diferenças, "
    "(3) pontos exclusivos. NUNCA emita opinião, NUNCA sugira candidato. "
    "Se algum candidato não tem proposta sobre o tema, diga claramente."
)


def _carregar_dados(sq_candidatos: list[int]) -> dict[int, dict[str, Any]]:
    """Devolve {sq: {nome, ano, resumos: {tema: texto}}} para os candidatos pedidos."""
    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT c.sq_candidato, c.nm_urna_candidato, e.ano_eleicao
              FROM candidatura c
              JOIN eleicao e ON e.cd_eleicao = c.cd_eleicao
             WHERE c.sq_candidato = ANY(%s)
        """, (sq_candidatos,))
        candidatos: dict[int, dict[str, Any]] = {}
        for r in cur.fetchall():
            candidatos[int(r["sq_candidato"])] = {
                "sq_candidato": int(r["sq_candidato"]),
                "nm_urna_candidato": r["nm_urna_candidato"],
                "ano_eleicao": int(r["ano_eleicao"]) if r["ano_eleicao"] is not None else None,
                "resumos": {},
            }
        for sq in sq_candidatos:
            sq = int(sq)
            if sq not in candidatos:
                candidatos[sq] = {
                    "sq_candidato": sq,
                    "nm_urna_candidato": f"sq={sq}",
                    "ano_eleicao": None,
                    "resumos": {},
                }

        cur.execute("""
            SELECT sq_candidato, ds_tema, tx_resumo
              FROM resumo_proposta
             WHERE sq_candidato = ANY(%s)
        """, (sq_candidatos,))
        for r in cur.fetchall():
            sq = int(r["sq_candidato"])
            candidatos[sq]["resumos"][r["ds_tema"]] = r["tx_resumo"]

        cur.close()
        return candidatos
    finally:
        conn.close()


def _label(c: dict) -> str:
    ano = c.get("ano_eleicao")
    return f"{c['nm_urna_candidato']} ({ano})" if ano else c["nm_urna_candidato"]


def _comparar_um_tema(
    sq_candidatos: list[int],
    tema: str,
    candidatos: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    sem_proposta: list[str] = []
    com_proposta: list[tuple[str, str]] = []  # [(label, resumo)]

    for sq in sq_candidatos:
        c = candidatos[int(sq)]
        resumo = (c["resumos"].get(tema) or "").strip()
        if not resumo or SEM_PROPOSTA_MARK.lower() in resumo.lower():
            sem_proposta.append(_label(c))
        else:
            com_proposta.append((_label(c), resumo))

    if not com_proposta:
        return {
            "tema": tema,
            "texto": f"Nenhum dos candidatos consultados tem proposta sobre {tema}.",
            "candidatos_sem_proposta": sem_proposta,
        }

    if len(com_proposta) == 1:
        label, resumo = com_proposta[0]
        return {
            "tema": tema,
            "texto": (
                f"Apenas {label} tem proposta sobre {tema}. "
                f"Os demais candidatos não trataram do tema.\n\n{resumo}"
            ),
            "candidatos_sem_proposta": sem_proposta,
        }

    contexto = "\n\n".join(f"### {label}:\n{resumo}" for label, resumo in com_proposta)
    user = (
        f"Tema: {tema}\n\n"
        f"Resumos das propostas dos candidatos:\n\n{contexto}\n\n"
        "Compare os candidatos sobre este tema. Aponte semelhanças, diferenças "
        "e pontos exclusivos. 2-3 parágrafos curtos."
    )
    completion = chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_COMPARACAO},
            {"role": "user", "content": user},
        ],
        temperature=0.1,
        max_tokens=600,
    )
    return {
        "tema": tema,
        "texto": (completion.choices[0].message.content or "").strip(),
        "candidatos_sem_proposta": sem_proposta,
    }


def comparar(
    sq_candidatos: list[int],
    temas: list[str],
) -> tuple[list[dict], list[dict]]:
    """Devolve (candidatos_resumido, comparacoes_por_tema)."""
    candidatos = _carregar_dados(sq_candidatos)
    candidatos_resumido = [
        {
            "sq_candidato": int(sq),
            "nome": candidatos[int(sq)]["nm_urna_candidato"],
            "ano": candidatos[int(sq)]["ano_eleicao"],
            "temas_disponiveis": sorted(candidatos[int(sq)]["resumos"].keys()),
        }
        for sq in sq_candidatos
    ]
    comparacoes = [_comparar_um_tema(sq_candidatos, t, candidatos) for t in temas]
    return candidatos_resumido, comparacoes
