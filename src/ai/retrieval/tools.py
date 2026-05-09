"""Funções tool-callable que executam SQL real contra o Postgres do VoteBem.

Cada função recebe argumentos primitivos (que o LLM consegue gerar),
faz UMA query e retorna estruturas JSON-serializáveis.
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from psycopg2.extras import RealDictCursor

from db import get_connection


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fmt_brl(v: Decimal | float | int | None) -> str | None:
    if v is None:
        return None
    s = f"{float(v):,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def _jsonify(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_jsonify(v) for v in obj]
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj


def _query(sql: str, params: tuple = ()) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, params)
        rows = [_jsonify(dict(r)) for r in cur.fetchall()]
        cur.close()
        return rows
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Ferramentas expostas ao LLM
# ---------------------------------------------------------------------------

def get_candidato_por_nome(termo: str) -> list[dict]:
    """Busca candidaturas presidenciais cujo nome de urna ou nome civil contenha o termo.

    Retorna até 20 resultados ordenados por ano decrescente.
    O LLM deve usar isto primeiro para descobrir o sq_candidato.
    """
    pattern = f"%{termo.strip()}%"
    rows = _query("""
        SELECT c.sq_candidato,
               c.nr_cpf_candidato,
               c.nm_urna_candidato,
               cand.nm_candidato,
               e.ano_eleicao,
               COALESCE(p.sg_partido, 'SEM PARTIDO') AS sg_partido,
               c.ds_situacao_candidatura
          FROM candidatura c
          JOIN candidato cand ON cand.nr_cpf_candidato = c.nr_cpf_candidato
          LEFT JOIN partido p ON p.nr_partido = c.nr_partido
          JOIN eleicao e ON e.cd_eleicao = c.cd_eleicao AND e.nr_turno = 1
         WHERE c.ds_cargo = 'PRESIDENTE'
           AND (c.nm_urna_candidato ILIKE %s OR cand.nm_candidato ILIKE %s)
         ORDER BY e.ano_eleicao DESC, c.nm_urna_candidato
         LIMIT 20
    """, (pattern, pattern))
    return rows


def get_perfil(sq_candidato: int) -> dict:
    """Perfil completo de uma candidatura: dados pessoais, partido, situação."""
    rows = _query("""
        SELECT c.sq_candidato,
               c.nr_cpf_candidato,
               cand.nm_candidato,
               c.nm_urna_candidato,
               cand.dt_nascimento,
               cand.ds_genero,
               cand.ds_grau_instrucao,
               cand.ds_estado_civil,
               cand.ds_cor_raca,
               c.ds_cargo,
               c.ds_ocupacao,
               c.ds_situacao_candidatura,
               c.foto_url,
               c.vr_despesa_max_campanha,
               COALESCE(p.sg_partido, 'SEM PARTIDO') AS sg_partido,
               COALESCE(p.nm_partido, '') AS nm_partido,
               e.ano_eleicao
          FROM candidatura c
          JOIN candidato cand ON cand.nr_cpf_candidato = c.nr_cpf_candidato
          LEFT JOIN partido p ON p.nr_partido = c.nr_partido
          JOIN eleicao e ON e.cd_eleicao = c.cd_eleicao AND e.nr_turno = 1
         WHERE c.sq_candidato = %s
    """, (sq_candidato,))
    if not rows:
        return {"encontrado": False, "sq_candidato": sq_candidato}
    perfil = rows[0]
    perfil["encontrado"] = True
    perfil["vr_despesa_max_campanha_formatado"] = _fmt_brl(perfil.get("vr_despesa_max_campanha"))
    return perfil


def get_bens(sq_candidato: int) -> dict:
    """Patrimônio total e composição por categoria para uma candidatura."""
    detalhe = _query("""
        SELECT ds_tipo_bem,
               COUNT(*)            AS qtd,
               COALESCE(SUM(vr_bem), 0) AS valor_total
          FROM bem_candidato
         WHERE sq_candidato = %s
         GROUP BY ds_tipo_bem
         ORDER BY valor_total DESC
    """, (sq_candidato,))

    total = sum(d["valor_total"] for d in detalhe)
    return {
        "sq_candidato": sq_candidato,
        "patrimonio_total": total,
        "patrimonio_total_formatado": _fmt_brl(total),
        "tem_bens_declarados": len(detalhe) > 0,
        "categorias": [
            {
                "tipo": d["ds_tipo_bem"],
                "quantidade": d["qtd"],
                "valor_total": d["valor_total"],
                "valor_total_formatado": _fmt_brl(d["valor_total"]),
            }
            for d in detalhe
        ],
    }


def get_situacao_juridica(sq_candidato: int) -> dict:
    """Situação da candidatura, motivos de cassação e certidões criminais."""
    perfil = _query("""
        SELECT c.ds_situacao_candidatura, e.ano_eleicao, c.nm_urna_candidato
          FROM candidatura c
          JOIN eleicao e ON e.cd_eleicao = c.cd_eleicao AND e.nr_turno = 1
         WHERE c.sq_candidato = %s
    """, (sq_candidato,))
    if not perfil:
        return {"encontrado": False, "sq_candidato": sq_candidato}

    cassacoes = _query("""
        SELECT ds_tp_motivo, ds_motivo
          FROM motivo_cassacao
         WHERE sq_candidato = %s
    """, (sq_candidato,))

    certidoes = _query("""
        SELECT id_certidao, nm_arquivo, dt_emissao, dt_validade
          FROM certidao_criminal
         WHERE sq_candidato = %s
         ORDER BY dt_emissao DESC NULLS LAST
    """, (sq_candidato,))

    base = perfil[0]
    base["encontrado"] = True
    base["sq_candidato"] = sq_candidato
    base["motivos_cassacao"] = cassacoes
    base["certidoes_criminais"] = certidoes
    base["tem_cassacao"] = len(cassacoes) > 0
    base["tem_certidao_disponivel"] = len(certidoes) > 0
    return base


def get_historico_eleitoral(nr_cpf_candidato: str) -> list[dict]:
    """Todas as candidaturas presidenciais do mesmo CPF, com votos por turno."""
    cpf = "".join(ch for ch in nr_cpf_candidato if ch.isdigit())
    rows = _query("""
        SELECT c.sq_candidato,
               c.nm_urna_candidato,
               e.ano_eleicao,
               c.ds_cargo,
               COALESCE(p.sg_partido, 'SEM PARTIDO') AS sg_partido,
               c.ds_situacao_candidatura,
               COALESCE(SUM(rt.nr_votos), 0)::bigint AS total_votos,
               (ARRAY_AGG(rt.ds_sit_tot_turno ORDER BY rt.nr_turno DESC))[1]
                   AS situacao_final
          FROM candidatura c
          JOIN eleicao e ON e.cd_eleicao = c.cd_eleicao AND e.nr_turno = 1
          LEFT JOIN partido p ON p.nr_partido = c.nr_partido
          LEFT JOIN resultado_turno rt ON rt.sq_candidato = c.sq_candidato
         WHERE c.nr_cpf_candidato = %s
           AND c.ds_cargo = 'PRESIDENTE'
         GROUP BY c.sq_candidato, c.nm_urna_candidato, e.ano_eleicao,
                  c.ds_cargo, p.sg_partido, c.ds_situacao_candidatura
         ORDER BY e.ano_eleicao
    """, (cpf,))
    return rows


def listar_candidatos_por_ano(ano: int) -> list[dict]:
    """Lista todos os candidatos PRESIDENTE de um ano eleitoral."""
    rows = _query("""
        SELECT c.sq_candidato,
               c.nm_urna_candidato,
               COALESCE(p.sg_partido, 'SEM PARTIDO') AS sg_partido,
               c.ds_situacao_candidatura
          FROM candidatura c
          LEFT JOIN partido p ON p.nr_partido = c.nr_partido
          JOIN eleicao e ON e.cd_eleicao = c.cd_eleicao AND e.nr_turno = 1
         WHERE c.ds_cargo = 'PRESIDENTE'
           AND e.ano_eleicao = %s
         ORDER BY c.nm_urna_candidato
    """, (ano,))
    return rows


# ---------------------------------------------------------------------------
# Registro central usado pelo Tier A
# ---------------------------------------------------------------------------

TOOL_FUNCTIONS = {
    "get_candidato_por_nome": get_candidato_por_nome,
    "get_perfil": get_perfil,
    "get_bens": get_bens,
    "get_situacao_juridica": get_situacao_juridica,
    "get_historico_eleitoral": get_historico_eleitoral,
    "listar_candidatos_por_ano": listar_candidatos_por_ano,
}
