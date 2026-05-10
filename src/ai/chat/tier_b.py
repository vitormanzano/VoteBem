"""Tier B — RAG sobre propostas de governo (RF06, RF07 e parte de RF12)."""
import json
import re

from psycopg2.extras import RealDictCursor

from llm import chat_completion
from chat.system_prompts import SYSTEM_PROMPT_BASE
from db import get_connection
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


def _disponibilidade(nomes: list[str]) -> list[dict]:
    """Para cada nome citado, lista todas as candidaturas presidenciais com info
    sobre disponibilidade de proposta pesquisável.

    Retorna [{termo, sq_candidato, nome, ano, tem_chunks}, ...]
    """
    if not nomes:
        return []
    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        infos: list[dict] = []
        vistos: set[int] = set()
        for nome in nomes:
            cur.execute(
                """
                SELECT c.sq_candidato,
                       c.nm_urna_candidato,
                       e.ano_eleicao,
                       EXISTS (
                         SELECT 1 FROM proposta_chunk pc
                          WHERE pc.sq_candidato = c.sq_candidato
                       ) AS tem_chunks
                  FROM candidatura c
                  JOIN eleicao e ON e.cd_eleicao = c.cd_eleicao
                 WHERE c.ds_cargo = 'PRESIDENTE'
                   AND c.nm_urna_candidato ILIKE %s
                 ORDER BY e.ano_eleicao
                """,
                (f"%{nome}%",),
            )
            for r in cur.fetchall():
                sq = int(r["sq_candidato"])
                if sq in vistos:
                    continue
                vistos.add(sq)
                infos.append({
                    "termo": nome,
                    "sq_candidato": sq,
                    "nome": r["nm_urna_candidato"],
                    "ano": int(r["ano_eleicao"]),
                    "tem_chunks": bool(r["tem_chunks"]),
                })
        cur.close()
        return infos
    finally:
        conn.close()


def _msg_indisponibilidade(infos: list[dict]) -> str:
    """Mensagem útil quando nenhum candidato citado tem proposta pesquisável."""
    if not infos:
        return (
            "Os candidatos citados não constam na base de dados do TSE "
            "como candidatos à Presidência entre 2010 e 2022."
        )

    # agrupa por nome de urna
    por_nome: dict[str, list[int]] = {}
    for i in infos:
        por_nome.setdefault(i["nome"], []).append(i["ano"])

    partes = []
    for nome, anos in por_nome.items():
        anos_str = ", ".join(str(a) for a in sorted(anos))
        partes.append(
            f"{nome} concorreu em {anos_str}, mas o TSE disponibilizou "
            f"apenas digitalização escaneada (sem texto pesquisável) das propostas."
        )
    return (
        "Não há propostas em formato pesquisável para essa consulta:\n- "
        + "\n- ".join(partes)
    )


def run(
    pergunta: str,
    sq_candidatos: list[int] | None = None,
    k: int = 6,
) -> tuple[str, list[dict]]:
    """Pipeline RAG: análise → resolução → busca → resposta com citações."""
    trecho, nomes = _analyze_query(pergunta)

    filtro = sq_candidatos
    aviso_anos = ""

    if filtro is None and nomes:
        infos = _disponibilidade(nomes)
        sqs_com = [i["sq_candidato"] for i in infos if i["tem_chunks"]]
        sqs_sem = [i for i in infos if not i["tem_chunks"]]

        if not sqs_com:
            # nenhum dos candidatos citados tem proposta pesquisável
            return _msg_indisponibilidade(infos), []

        filtro = sqs_com

        # Sempre informa ao LLM a disponibilidade completa dos candidatos
        # citados — anos que ele concorreu e quais têm texto pesquisável.
        # Assim o LLM sabe responder "X não concorreu em Y" e
        # "PDF de Y é só digitalização" sem inventar.
        por_nome: dict[str, list[tuple[int, bool]]] = {}
        for i in infos:
            por_nome.setdefault(i["nome"], []).append((i["ano"], i["tem_chunks"]))

        linhas = []
        for nome, lista in por_nome.items():
            partes_anos = [
                f"{ano} ({'disponível' if tem else 'apenas digitalização escaneada'})"
                for ano, tem in sorted(lista)
            ]
            linhas.append(f"- {nome}: {', '.join(partes_anos)}")
        aviso_anos = (
            "DISPONIBILIDADE DOS CANDIDATOS CITADOS (use SEMPRE esta informação "
            "antes de responder):\n"
            + "\n".join(linhas)
            + "\nSe o eleitor pediu um ano em que o candidato não concorreu, "
            "informe isso explicitamente. Se pediu um ano sem texto pesquisável, "
            "diga que apenas a digitalização está disponível e ofereça os anos cobertos.\n\n"
        )

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
            "trecho": c["texto"],
        })

    prompt_user = (
        f"Pergunta do eleitor: {pergunta}\n\n"
        + aviso_anos
        + "Use APENAS os trechos abaixo. Toda afirmação deve ser seguida da "
        + "referência [N] correspondente. Se os trechos não tratam da pergunta, "
        + "responda \"Não consta na base de dados oficial do TSE.\"\n\n"
        + "Trechos:\n\n"
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
