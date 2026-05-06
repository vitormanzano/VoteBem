"""
gerar_dataset.py - Gera dataset expandido para fine-tuning
"""
import psycopg2
import psycopg2.extras
import json
import os
import random
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB_NAME"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def gerar_dataset():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dados = []

    # Busca todos candidatos com dados completos
    cur.execute("""
        SELECT DISTINCT ON (c.nr_cpf_candidato, e.ano_eleicao)
               c.nr_cpf_candidato, c.nm_candidato, c.nm_urna_candidato,
               c.ds_genero, c.ds_grau_instrucao, c.ds_estado_civil,
               c.ds_cor_raca, c.dt_nascimento, c.sg_uf_nascimento,
               p.sg_partido, p.nm_partido,
               ca.sq_candidato, ca.ds_situacao_candidatura, ca.vr_despesa_max_campanha,
               e.ano_eleicao
        FROM CANDIDATO c
        JOIN CANDIDATURA ca ON c.nr_cpf_candidato = ca.nr_cpf_candidato
        JOIN PARTIDO p ON ca.nr_partido = p.nr_partido
        JOIN ELEICAO e ON ca.cd_eleicao = e.cd_eleicao AND e.nr_turno = 1
        WHERE ca.cd_cargo = 1
        ORDER BY c.nr_cpf_candidato, e.ano_eleicao, p.sg_partido
    """)
    candidatos = cur.fetchall()

    # Agrupa candidatos por ano
    por_ano = {}
    for c in candidatos:
        ano = c["ano_eleicao"]
        if ano not in por_ano:
            por_ano[ano] = []
        por_ano[ano].append(c)

    todos_candidatos = []

    for cand in candidatos:
        sq = cand["sq_candidato"]
        nome = cand["nm_candidato"]
        urna = cand["nm_urna_candidato"] or nome
        ano = cand["ano_eleicao"]
        partido = cand["sg_partido"]
        nm_partido = cand["nm_partido"]
        situacao = cand["ds_situacao_candidatura"]
        genero = cand["ds_genero"]
        instrucao = cand["ds_grau_instrucao"]
        estado_civil = cand["ds_estado_civil"]
        cor_raca = cand["ds_cor_raca"]
        nascimento = cand["dt_nascimento"]
        uf_nasc = cand["sg_uf_nascimento"]
        despesa_max = cand["vr_despesa_max_campanha"]

        # Resultados
        cur.execute("SELECT nr_turno, nr_votos, ds_sit_tot_turno FROM RESULTADO_TURNO WHERE sq_candidato = %s ORDER BY nr_turno", (sq,))
        resultados = cur.fetchall()

        # Bens
        cur.execute("SELECT ds_tipo_bem, ds_bem, vr_bem FROM BEM_CANDIDATO WHERE sq_candidato = %s ORDER BY vr_bem DESC", (sq,))
        bens = cur.fetchall()
        patrimonio_total = sum(b["vr_bem"] or 0 for b in bens)

        # Despesas
        cur.execute("SELECT SUM(vr_despesa) as total, COUNT(*) as qtd FROM DESPESA_CANDIDATO WHERE sq_candidato = %s", (sq,))
        desp = cur.fetchone()
        total_despesas = desp["total"] if desp and desp["total"] else 0
        qtd_despesas = desp["qtd"] if desp else 0

        # Certidões
        cur.execute("SELECT COUNT(*) as qtd FROM CERTIDAO_CRIMINAL WHERE sq_candidato = %s", (sq,))
        cert = cur.fetchone()
        qtd_cert = cert["qtd"] if cert else 0

        # Cassações
        cur.execute("SELECT ds_tp_motivo, ds_motivo FROM MOTIVO_CASSACAO WHERE sq_candidato = %s", (sq,))
        cassacoes = cur.fetchall()

        # Coligação
        cur.execute("""
            SELECT co.nm_coligacao, co.ds_composicao_coligacao
            FROM CANDIDATURA ca JOIN COLIGACAO co ON ca.sq_coligacao = co.sq_coligacao
            WHERE ca.sq_candidato = %s
        """, (sq,))
        coligacao = cur.fetchone()

        # Salva info completa
        info = {
            "nome": nome, "urna": urna, "ano": ano, "partido": partido,
            "nm_partido": nm_partido, "situacao": situacao, "genero": genero,
            "instrucao": instrucao, "estado_civil": estado_civil, "cor_raca": cor_raca,
            "nascimento": str(nascimento), "uf_nasc": uf_nasc, "despesa_max": despesa_max,
            "resultados": [dict(r) for r in resultados],
            "bens": [dict(b) for b in bens], "patrimonio_total": float(patrimonio_total),
            "total_despesas": float(total_despesas), "qtd_despesas": qtd_despesas,
            "qtd_cert": qtd_cert, "cassacoes": [dict(c) for c in cassacoes],
            "coligacao": dict(coligacao) if coligacao else None
        }
        todos_candidatos.append(info)

        # ── Gera pares pergunta/resposta ──

        # 1. Partido
        for pergunta in [
            f"Qual partido {nome} representou em {ano}?",
            f"Por qual partido {urna} concorreu em {ano}?",
            f"Qual a legenda de {nome} nas eleições de {ano}?",
        ]:
            dados.append(fmt(pergunta, f"{nome} representou o {partido} ({nm_partido}) nas eleições presidenciais de {ano}."))

        # 2. Situação
        dados.append(fmt(
            f"Qual foi a situação da candidatura de {nome} em {ano}?",
            f"A candidatura de {nome} em {ano} teve situação: {situacao}."
        ))

        # 3. Perfil
        dados.append(fmt(
            f"Qual o perfil de {nome}?",
            f"{nome} é do gênero {genero}, grau de instrução {instrucao}, estado civil {estado_civil}, cor/raça {cor_raca}, nascido(a) em {nascimento} no estado {uf_nasc}."
        ))

        # 4. Votos
        for r in resultados:
            turno = r["nr_turno"]
            votos = r["nr_votos"]
            resultado = r["ds_sit_tot_turno"]
            for pergunta in [
                f"Quantos votos {nome} recebeu no {turno}º turno de {ano}?",
                f"Qual o resultado de {urna} no {turno}º turno das eleições de {ano}?",
                f"Como foi o desempenho de {nome} no turno {turno} de {ano}?",
            ]:
                dados.append(fmt(pergunta, f"{nome} recebeu {votos:,} votos no {turno}º turno de {ano}. Resultado: {resultado}."))

        # 5. Patrimônio
        if patrimonio_total > 0:
            lista_bens = ". ".join([f"{b['ds_tipo_bem']}: R$ {b['vr_bem']:,.2f}" for b in bens[:5]])
            for pergunta in [
                f"Qual o patrimônio declarado de {nome} em {ano}?",
                f"Quanto {urna} declarou de patrimônio nas eleições de {ano}?",
                f"Quais os bens de {nome} declarados em {ano}?",
            ]:
                dados.append(fmt(pergunta, f"{nome} declarou patrimônio total de R$ {patrimonio_total:,.2f} em {ano}. Principais bens: {lista_bens}."))

        # 6. Despesas
        if total_despesas > 0:
            for pergunta in [
                f"Quanto {nome} gastou na campanha de {ano}?",
                f"Quais foram as despesas de campanha de {urna} em {ano}?",
                f"Qual o total de gastos de {nome} nas eleições de {ano}?",
            ]:
                dados.append(fmt(pergunta, f"{nome} registrou R$ {total_despesas:,.2f} em despesas de campanha nas eleições de {ano}, com {qtd_despesas} registros."))

        # 7. Certidões
        if qtd_cert > 0:
            dados.append(fmt(
                f"{nome} possui certidões criminais?",
                f"Sim, {nome} possui {qtd_cert} certidão(ões) criminal(is) registrada(s) no sistema."
            ))
        else:
            dados.append(fmt(
                f"{nome} possui certidões criminais?",
                f"Não há certidões criminais registradas para {nome} no sistema."
            ))

        # 8. Cassações
        if cassacoes:
            for cas in cassacoes:
                dados.append(fmt(
                    f"{nome} teve alguma cassação?",
                    f"Sim, {nome} teve cassação registrada: {cas['ds_motivo']}."
                ))
        else:
            dados.append(fmt(
                f"{nome} teve alguma cassação?",
                f"Não há registros de cassação para {nome} no sistema."
            ))

        # 9. Coligação
        if coligacao:
            dados.append(fmt(
                f"Qual a coligação de {nome} em {ano}?",
                f"Em {ano}, {nome} integrou a coligação '{coligacao['nm_coligacao']}', composta por: {coligacao['ds_composicao_coligacao']}."
            ))

        # 10. Informações completas
        info_completa = f"{nome} ({urna}) concorreu à presidência em {ano} pelo {partido}. Situação: {situacao}."
        if resultados:
            for r in resultados:
                info_completa += f" {r['nr_turno']}º turno: {r['nr_votos']:,} votos ({r['ds_sit_tot_turno']})."
        if patrimonio_total > 0:
            info_completa += f" Patrimônio declarado: R$ {patrimonio_total:,.2f}."
        if total_despesas > 0:
            info_completa += f" Despesas de campanha: R$ {total_despesas:,.2f}."
        if qtd_cert > 0:
            info_completa += f" Certidões criminais: {qtd_cert}."

        dados.append(fmt(f"Me dê todas as informações sobre {nome} em {ano}.", info_completa))
        dados.append(fmt(f"Quem é {nome}?", info_completa))

    # ── Perguntas por ano ──
    for ano, lista in por_ano.items():
        nomes = [f"{c['nm_candidato']} ({c['sg_partido']})" for c in lista]
        lista_str = ", ".join(nomes)

        for pergunta in [
            f"Quais candidatos concorreram à presidência em {ano}?",
            f"Quem foram os candidatos a presidente em {ano}?",
            f"Liste os candidatos presidenciais de {ano}.",
            f"Quais foram as candidaturas presidenciais em {ano}?",
        ]:
            dados.append(fmt(pergunta, f"Os candidatos à presidência em {ano} foram: {lista_str}."))

        # Por partido em cada ano
        for c in lista:
            dados.append(fmt(
                f"Qual candidato do {c['sg_partido']} concorreu em {ano}?",
                f"O candidato do {c['sg_partido']} ({c['nm_partido']}) nas eleições de {ano} foi {c['nm_candidato']}."
            ))

    # ── Perguntas gerais ──
    todos_anos = sorted(por_ano.keys())
    dados.append(fmt(
        "Quais anos de eleições estão disponíveis no sistema?",
        f"O sistema possui dados das eleições presidenciais de {', '.join(str(a) for a in todos_anos)}."
    ))

    todos_nomes = list(set([c["nome"] for c in todos_candidatos]))
    dados.append(fmt(
        "Quais candidatos estão no sistema?",
        f"O sistema possui dados de {len(todos_nomes)} candidatos presidenciais: {', '.join(todos_nomes[:20])}."
    ))

    conn.close()

    # Embaralha para melhor treinamento
    random.shuffle(dados)

    output_path = os.path.join(os.path.dirname(__file__), "dataset_politico.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"Dataset gerado com {len(dados)} exemplos em: {output_path}")
    return output_path

def fmt(pergunta, resposta):
    """Formato Phi-3"""
    return {
        "text": f"<|user|>\n{pergunta}<|end|>\n<|assistant|>\n{resposta}<|end|>"
    }

if __name__ == "__main__":
    gerar_dataset()