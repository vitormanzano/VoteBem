"""Tier B — RAG sobre propostas de governo (RF06, RF07 e parte de RF12)."""
import json
import re

from llm import chat_completion
from chat.system_prompts import SYSTEM_PROMPT_BASE
from retrieval.vector_search import search_chunks
from retrieval.tools import get_candidato_por_nome

ANALYZE_SYSTEM = (
    "Para uma pergunta sobre planos de governo de candidatos brasileiros à "
    "Presidência, gere um JSON com 2 campos:\n"
    "1. \"trecho_hipotetico\": 1-2 frases em pt-BR, no estilo de um trecho real "
    "de plano de governo sobre o tema da pergunta. NÃO mencione candidatos.\n"
    "2. \"candidatos\": lista de nomes de candidatos citados na pergunta "
    "(nome de urna ou primeiro nome). Se nenhum candidato é citado, lista vazia.\n\n"
    "Responda APENAS com o JSON, sem comentários ou markdown."
)


def _analyze_query(pergunta: str) -> tuple[str, list[str]]:
    """HyDE + extração de nomes em uma única chamada."""
    completion = chat_completion(
        messages=[
            {"role": "system", "content": ANALYZE_SYSTEM},
            {"role": "user", "content": pergunta},
        ],
        temperature=0.0,
        max_tokens=200,
    )
    raw = (completion.choices[0].message.content or "").strip()
    m = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not m:
        return pergunta, []
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return pergunta, []
    trecho = (data.get("trecho_hipotetico") or "").strip() or pergunta
    candidatos = data.get("candidatos") or []
    return trecho, [c for c in candidatos if isinstance(c, str) and c.strip()]


def _resolver_sqs(nomes: list[str]) -> list[int]:
    """Resolve cada nome em sq_candidatos via get_candidato_por_nome (todos os anos)."""
    sqs: list[int] = []
    for nome in nomes:
        for r in get_candidato_por_nome(nome):
            sq = int(r["sq_candidato"])
            if sq not in sqs:
                sqs.append(sq)
    return sqs


def run(
    pergunta: str,
    sq_candidatos: list[int] | None = None,
    k: int = 6,
) -> tuple[str, list[dict]]:
    """Pipeline RAG: análise → resolução → busca → resposta com citações."""
    trecho, nomes = _analyze_query(pergunta)

    # Filtro por candidato: se a pergunta cita nomes e o caller não passou
    # uma lista explícita, resolvemos os sq_candidato dos nomes citados.
    filtro = sq_candidatos
    if filtro is None and nomes:
        filtro = _resolver_sqs(nomes) or None

    chunks = search_chunks(trecho, sq_candidatos=filtro, k=k)

    if not chunks:
        return (
            "Não consta na base de dados oficial do TSE proposta de governo "
            "que contenha essa informação para os candidatos consultados.",
            [],
        )

    contexto_partes = []
    fontes = []
    for i, c in enumerate(chunks, start=1):
        contexto_partes.append(
            f"[{i}] {c['nm_urna_candidato']} (eleição {c['ano_eleicao']}):\n{c['texto']}"
        )
        fontes.append({
            "ref": i,
            "sq_candidato": int(c["sq_candidato"]),
            "nome": c["nm_urna_candidato"],
            "ano": int(c["ano_eleicao"]),
            "trecho": c["texto"][:200] + ("…" if len(c["texto"]) > 200 else ""),
        })

    prompt_user = (
        f"Pergunta do eleitor: {pergunta}\n\n"
        f"Use APENAS os trechos abaixo. Toda afirmação deve ser seguida da "
        f"referência [N] correspondente. Se os trechos não tratam da pergunta, "
        f"responda \"Não consta na base de dados oficial do TSE.\"\n\n"
        f"Trechos:\n\n"
        + "\n\n".join(contexto_partes)
    )

    completion = chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_BASE},
            {"role": "user", "content": prompt_user},
        ],
        temperature=0.1,
        max_tokens=1024,
    )
    resposta = (completion.choices[0].message.content or "").strip()
    return resposta, fontes
