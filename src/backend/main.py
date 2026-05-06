from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import httpx
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB_NAME"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )


def buscar_dados(pergunta: str) -> str:
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    resultados = []

    try:
        # Detecta ano mencionado na pergunta
        ano = None
        for palavra in pergunta.split():
            if palavra.isdigit() and len(palavra) == 4:
                ano = int(palavra)
                break

        # Detecta nomes mencionados na pergunta
        palavras = [p for p in pergunta.lower().split() if len(p) > 3]

        if palavras:
            condicao_parts = []
            params = []
            for p in palavras:
                condicao_parts.append(
                    "(LOWER(c.nm_candidato) LIKE %s OR LOWER(c.nm_urna_candidato) LIKE %s)"
                )
                params.extend([f"%{p}%", f"%{p}%"])

            where_extra = " OR ".join(condicao_parts)

            query = (
                "SELECT DISTINCT c.nr_cpf_candidato, c.nm_candidato, c.nm_urna_candidato,"
                " c.ds_genero, c.ds_grau_instrucao, c.ds_estado_civil, c.ds_cor_raca,"
                " c.dt_nascimento, c.sg_uf_nascimento"
                " FROM CANDIDATO c"
                " JOIN CANDIDATURA ca ON c.nr_cpf_candidato = ca.nr_cpf_candidato"
                " WHERE ca.cd_cargo = 1"
                " AND (" + where_extra + ")"
            )
            cur.execute(query, params)
            candidatos = cur.fetchall()
        else:
            candidatos = []

        # Se não achou por nome, busca por ano ou todos
        if not candidatos:
            if ano:
                cur.execute("""
                    SELECT DISTINCT c.nr_cpf_candidato, c.nm_candidato, c.nm_urna_candidato,
                           c.ds_genero, c.ds_grau_instrucao, c.ds_estado_civil, c.ds_cor_raca,
                           c.dt_nascimento, c.sg_uf_nascimento
                    FROM CANDIDATO c
                    JOIN CANDIDATURA ca ON c.nr_cpf_candidato = ca.nr_cpf_candidato
                    JOIN ELEICAO e ON ca.cd_eleicao = e.cd_eleicao
                    WHERE ca.cd_cargo = 1
                      AND e.ano_eleicao = %s
                      AND e.nr_turno = 1
                """, (ano,))
            else:
                cur.execute("""
                    SELECT DISTINCT c.nr_cpf_candidato, c.nm_candidato, c.nm_urna_candidato,
                           c.ds_genero, c.ds_grau_instrucao, c.ds_estado_civil, c.ds_cor_raca,
                           c.dt_nascimento, c.sg_uf_nascimento
                    FROM CANDIDATO c
                    JOIN CANDIDATURA ca ON c.nr_cpf_candidato = ca.nr_cpf_candidato
                    WHERE ca.cd_cargo = 1
                    LIMIT 100
                """)
            candidatos = cur.fetchall()

        for cand in candidatos:
            cpf = cand["nr_cpf_candidato"]
            nome = cand["nm_candidato"]
            info = f"\n--- CANDIDATO: {nome} ---\n"
            info += f"Nome na urna: {cand['nm_urna_candidato']} | Gênero: {cand['ds_genero']} | "
            info += f"Instrução: {cand['ds_grau_instrucao']} | Estado civil: {cand['ds_estado_civil']} | "
            info += f"Cor/Raça: {cand['ds_cor_raca']} | Nascimento: {cand['dt_nascimento']} | UF: {cand['sg_uf_nascimento']}\n"

            # Busca candidaturas — filtra por ano se mencionado
            if ano:
                cur.execute("""
                    SELECT DISTINCT ON (e.ano_eleicao)
                           ca.sq_candidato, e.ano_eleicao, p.sg_partido, p.nm_partido,
                           ca.ds_situacao_candidatura, ca.vr_despesa_max_campanha
                    FROM CANDIDATURA ca
                    JOIN ELEICAO e ON ca.cd_eleicao = e.cd_eleicao AND e.nr_turno = 1
                    JOIN PARTIDO p ON ca.nr_partido = p.nr_partido
                    WHERE ca.nr_cpf_candidato = %s
                      AND ca.cd_cargo = 1
                      AND e.ano_eleicao = %s
                    ORDER BY e.ano_eleicao, p.sg_partido
                """, (cpf, ano))
            else:
                cur.execute("""
                    SELECT DISTINCT ON (e.ano_eleicao)
                           ca.sq_candidato, e.ano_eleicao, p.sg_partido, p.nm_partido,
                           ca.ds_situacao_candidatura, ca.vr_despesa_max_campanha
                    FROM CANDIDATURA ca
                    JOIN ELEICAO e ON ca.cd_eleicao = e.cd_eleicao AND e.nr_turno = 1
                    JOIN PARTIDO p ON ca.nr_partido = p.nr_partido
                    WHERE ca.nr_cpf_candidato = %s
                      AND ca.cd_cargo = 1
                    ORDER BY e.ano_eleicao, p.sg_partido
                """, (cpf,))
            candidaturas = cur.fetchall()

            for cand_row in candidaturas:
                sq = cand_row["sq_candidato"]
                info += f"\nEleição {cand_row['ano_eleicao']} | Partido: {cand_row['sg_partido']} ({cand_row['nm_partido']}) | "
                info += f"Situação: {cand_row['ds_situacao_candidatura']} | Despesa máx: R$ {cand_row['vr_despesa_max_campanha']}\n"

                cur.execute("""
                    SELECT nr_turno, nr_votos, ds_sit_tot_turno
                    FROM RESULTADO_TURNO WHERE sq_candidato = %s ORDER BY nr_turno
                """, (sq,))
                for r in cur.fetchall():
                    info += f"  Turno {r['nr_turno']}: {r['nr_votos']:,} votos | Resultado: {r['ds_sit_tot_turno']}\n"

                cur.execute("""
                    SELECT ds_tipo_bem, ds_bem, vr_bem
                    FROM BEM_CANDIDATO WHERE sq_candidato = %s ORDER BY vr_bem DESC LIMIT 5
                """, (sq,))
                bens = cur.fetchall()
                if bens:
                    total = sum(b["vr_bem"] or 0 for b in bens)
                    info += f"  Patrimônio total declarado: R$ {total:,.2f}\n"
                    for b in bens[:3]:
                        info += f"    - {b['ds_tipo_bem']}: {b['ds_bem']} (R$ {b['vr_bem']:,.2f})\n"

                cur.execute("""
                    SELECT SUM(vr_despesa) as total, COUNT(*) as qtd
                    FROM DESPESA_CANDIDATO WHERE sq_candidato = %s
                """, (sq,))
                desp = cur.fetchone()
                if desp and desp["total"]:
                    info += f"  Despesas de campanha: R$ {desp['total']:,.2f} ({desp['qtd']} registros)\n"

                cur.execute("""
                    SELECT COUNT(*) as qtd FROM CERTIDAO_CRIMINAL WHERE sq_candidato = %s
                """, (sq,))
                cert = cur.fetchone()
                if cert and cert["qtd"] > 0:
                    info += f"  Certidões criminais: {cert['qtd']} registro(s)\n"

                cur.execute("""
                    SELECT ds_tp_motivo, ds_motivo FROM MOTIVO_CASSACAO WHERE sq_candidato = %s
                """, (sq,))
                for cas in cur.fetchall():
                    info += f"  Cassação: {cas['ds_tp_motivo']} - {cas['ds_motivo']}\n"

            resultados.append(info)

        conn.close()
        return "\n".join(resultados) if resultados else "Nenhum dado encontrado para essa consulta."

    except Exception as e:
        conn.close()
        raise e


SYSTEM_PROMPT = """Você é um assistente informativo do sistema Voto Consciente.
Seu papel é exclusivamente apresentar dados objetivos sobre candidatos à presidência do Brasil nas eleições de 2010, 2014, 2018 e 2022.

REGRAS ABSOLUTAS:
- Apresente APENAS os dados fornecidos no contexto. Nunca invente ou suponha informações.
- Liste TODOS os candidatos encontrados nos dados, sem omitir nenhum.
- NUNCA faça recomendações, opiniões, julgamentos ou análises subjetivas.
- NUNCA compare candidatos de forma valorativa.
- NUNCA use adjetivos positivos ou negativos sobre candidatos, partidos ou desempenhos.
- NUNCA sugira em quem votar, quem é melhor ou pior.
- Responda SEMPRE em português do Brasil.
- Se os dados não contiverem a informação solicitada, diga: "Não há dados disponíveis sobre isso no sistema."
- Seja direto, claro e factual.
- Formate números de votos e valores monetários de forma legível."""


class Mensagem(BaseModel):
    pergunta: str
    historico: list = []


@app.post("/chat")
async def chat(msg: Mensagem):
    try:
        dados = buscar_dados(msg.pergunta)

        historico_txt = "\n".join([
            f"{m['papel']}: {m['texto']}" for m in msg.historico[-6:]
        ]) if msg.historico else ""

        prompt = f"""{SYSTEM_PROMPT}

DADOS DISPONÍVEIS NO SISTEMA:
{dados}

HISTÓRICO DA CONVERSA:
{historico_txt}

PERGUNTA DO USUÁRIO: {msg.pergunta}

RESPOSTA:"""

        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={"model": "votebem", "prompt": prompt, "stream": False},
            timeout=300.0
        )
        return {"resposta": response.json()["response"]}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/candidatos")
async def listar_candidatos():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT DISTINCT ON (c.nr_cpf_candidato, e.ano_eleicao)
               c.nm_candidato, c.nm_urna_candidato, p.sg_partido, e.ano_eleicao
        FROM CANDIDATO c
        JOIN CANDIDATURA ca ON c.nr_cpf_candidato = ca.nr_cpf_candidato
        JOIN PARTIDO p ON ca.nr_partido = p.nr_partido
        JOIN ELEICAO e ON ca.cd_eleicao = e.cd_eleicao AND e.nr_turno = 1
        WHERE ca.cd_cargo = 1
        ORDER BY c.nr_cpf_candidato, e.ano_eleicao, p.sg_partido
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/health")
async def health():
    return {"status": "ok"}