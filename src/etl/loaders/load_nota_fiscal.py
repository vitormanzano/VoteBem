import pandas as pd
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from connection import Session
from models.candidatura import Candidatura
from models.nota_fiscal import NotaFiscal

ANOS = [2018, 2022]

COLUNAS = [
    "CD_ELEICAO",
    "NR_CANDIDATO",
    "SG_UF_UA",
    "NR_CPF_CNPJ_EMITENTE",
    "DT_EMISSAO",
    "NR_NOTA_FISCAL",
    "NR_SERIE",
    "VR_NOTA_FISCAL",
    "NR_CHAVE_ACESSO",
    "NM_URL_ACESSO",
]


def _strip_or_none(valor):
    return valor.strip() if isinstance(valor, str) else None


def _valor(row, col):
    valor = row[col]
    return None if pd.isna(valor) else valor


def load_notas_fiscais(data_dir: Path):
    dfs = []

    for ano in ANOS:
        caminho = data_dir / str(ano) / "nota_fiscal_candidato" / f"nota_fiscal_candidato_{ano}_BR.csv"
        if not caminho.exists():
            continue

        df_ano = pd.read_csv(
            caminho,
            encoding="latin-1",
            sep=";",
            quotechar='"',
            usecols=COLUNAS,
            dtype={
                "CD_ELEICAO": str,
                "NR_CANDIDATO": str,
                "SG_UF_UA": str,
                "NR_CPF_CNPJ_EMITENTE": str,
                "NR_NOTA_FISCAL": str,
                "NR_SERIE": str,
                "NR_CHAVE_ACESSO": str,
                "NM_URL_ACESSO": str,
            },
        )

        if not df_ano.empty:
            dfs.append(df_ano)

    if not dfs:
        print("Nenhum arquivo de nota fiscal encontrado.")
        return

    df = pd.concat(dfs, ignore_index=True)
    df.replace(["#NULO#", "#NULO", "#NE#", "#NE"], None, inplace=True)

    for col in [
        "SG_UF_UA",
        "NR_CPF_CNPJ_EMITENTE",
        "NR_NOTA_FISCAL",
        "NR_SERIE",
        "NR_CHAVE_ACESSO",
        "NM_URL_ACESSO",
    ]:
        df[col] = df[col].apply(_strip_or_none)

    df["CD_ELEICAO"] = pd.to_numeric(df["CD_ELEICAO"], errors="coerce").astype("Int64")
    df["NR_CANDIDATO"] = pd.to_numeric(df["NR_CANDIDATO"], errors="coerce").astype("Int64")
    df["DT_EMISSAO"] = pd.to_datetime(df["DT_EMISSAO"], errors="coerce").dt.date
    df["VR_NOTA_FISCAL"] = pd.to_numeric(df["VR_NOTA_FISCAL"], errors="coerce")

    df = df[
        df["CD_ELEICAO"].notna()
        & df["NR_CANDIDATO"].notna()
        & df["SG_UF_UA"].notna()
        & (df["SG_UF_UA"] != "")
    ].copy()

    df["CD_ELEICAO"] = df["CD_ELEICAO"].astype(int)
    df["NR_CANDIDATO"] = df["NR_CANDIDATO"].astype(int)

    session = Session()

    try:
        candidaturas = session.execute(
            select(
                Candidatura.sq_candidato,
                Candidatura.cd_eleicao,
                Candidatura.nr_candidato,
                Candidatura.sg_uf,
            )
        ).fetchall()

        mapa_sq = {
            (int(row.cd_eleicao), int(row.nr_candidato), row.sg_uf): int(row.sq_candidato)
            for row in candidaturas
            if row.cd_eleicao is not None and row.nr_candidato is not None and row.sg_uf is not None
        }

        chaves = list(zip(df["CD_ELEICAO"], df["NR_CANDIDATO"], df["SG_UF_UA"]))
        df["SQ_CANDIDATO"] = [mapa_sq.get(chave) for chave in chaves]

        antes = len(df)
        df = df[df["SQ_CANDIDATO"].notna()].copy()
        ignorados = antes - len(df)

        if ignorados:
            print(f"{ignorados} notas fiscais ignoradas (candidatura não encontrada)")

        df["SQ_CANDIDATO"] = df["SQ_CANDIDATO"].astype(int)

        df.drop_duplicates(
            subset=[
                "CD_ELEICAO",
                "NR_CANDIDATO",
                "SG_UF_UA",
                "NR_NOTA_FISCAL",
                "NR_CPF_CNPJ_EMITENTE",
            ],
            inplace=True,
        )

        for _, row in df.iterrows():
            statement = insert(NotaFiscal).values(
                sq_candidato=int(row["SQ_CANDIDATO"]),
                cd_eleicao=int(row["CD_ELEICAO"]),
                nr_candidato=int(row["NR_CANDIDATO"]),
                sg_uf=row["SG_UF_UA"],
                nr_nota_fiscal=_valor(row, "NR_NOTA_FISCAL"),
                nr_serie=_valor(row, "NR_SERIE"),
                cpf_cnpj_emitente=_valor(row, "NR_CPF_CNPJ_EMITENTE"),
                dt_emissao=_valor(row, "DT_EMISSAO"),
                vr_nota_fiscal=None if pd.isna(row["VR_NOTA_FISCAL"]) else float(row["VR_NOTA_FISCAL"]),
                nr_chave_acesso=_valor(row, "NR_CHAVE_ACESSO"),
                nm_url_acesso=_valor(row, "NM_URL_ACESSO"),
            ).on_conflict_do_update(
                index_elements=[
                    "cd_eleicao",
                    "nr_candidato",
                    "sg_uf",
                    "nr_nota_fiscal",
                    "cpf_cnpj_emitente",
                ],
                set_={
                    "sq_candidato": int(row["SQ_CANDIDATO"]),
                    "nr_serie": _valor(row, "NR_SERIE"),
                    "dt_emissao": _valor(row, "DT_EMISSAO"),
                    "vr_nota_fiscal": None if pd.isna(row["VR_NOTA_FISCAL"]) else float(row["VR_NOTA_FISCAL"]),
                    "nr_chave_acesso": _valor(row, "NR_CHAVE_ACESSO"),
                    "nm_url_acesso": _valor(row, "NM_URL_ACESSO"),
                },
            )

            session.execute(statement)

        session.commit()
        print(f"{len(df)} notas fiscais carregadas com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar notas fiscais: {ex}")

    finally:
        session.close()


if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_notas_fiscais(data_dir)

