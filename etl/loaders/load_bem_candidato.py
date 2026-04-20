import pandas as pd
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from connection import Session
from models.bem_candidato import BemCandidato
from models.candidatura import Candidatura

ANOS = [2010, 2014, 2018, 2022]
COLUNAS_BASE = ["SQ_CANDIDATO", "CD_TIPO_BEM_CANDIDATO", "DS_TIPO_BEM_CANDIDATO", "DS_BEM_CANDIDATO", "VR_BEM_CANDIDATO"]

def load_bens_candidato(data_dir: Path):
    dfs = []

    for ano in ANOS:
        caminho = data_dir / str(ano) / "bem_candidato" / f"bem_candidato_{ano}_BR.csv"

        # Coluna de ordem muda de nome entre 2010 e 2014+
        col_ordem = "NR_ORDEM_CANDIDATO" if ano == 2010 else "NR_ORDEM_BEM_CANDIDATO"

        df = pd.read_csv(
                caminho,
                encoding = "latin-1",
                sep = ";",
                quotechar = '"',
                usecols = COLUNAS_BASE + [col_ordem],
                dtype = {"SQ_CANDIDATO": str}
        )
        df.rename(columns = {col_ordem: "NR_ORDEM_BEM_CANDIDATO"}, inplace = True)
        dfs.append(df)

    df_total = pd.concat(dfs, ignore_index = True)
    df_total.replace(["#NULO#", "#NULO", "#NE#", "#NE"], None, inplace = True)

    df_total.drop_duplicates(subset = ["SQ_CANDIDATO", "NR_ORDEM_BEM_CANDIDATO"], inplace = True)

    df_total["SQ_CANDIDATO"] = df_total["SQ_CANDIDATO"].str.strip()
    df_total["NR_ORDEM_BEM_CANDIDATO"] = df_total["NR_ORDEM_BEM_CANDIDATO"].astype(int)
    df_total["CD_TIPO_BEM_CANDIDATO"] = df_total["CD_TIPO_BEM_CANDIDATO"].astype(int)
    df_total["DS_TIPO_BEM_CANDIDATO"] = df_total["DS_TIPO_BEM_CANDIDATO"].str.strip()
    df_total["DS_BEM_CANDIDATO"] = df_total["DS_BEM_CANDIDATO"].str.strip()
    df_total["VR_BEM_CANDIDATO"] = df_total["VR_BEM_CANDIDATO"].str.replace(",", ".").astype(float)

    session = Session()

    sqs_existentes = set(
        str(row[0]) for row in session.execute(select(Candidatura.sq_candidato)).fetchall()
    )
    antes = len(df_total)
    df_total = df_total[df_total["SQ_CANDIDATO"].isin(sqs_existentes)]
    ignorados = antes - len(df_total)
    if ignorados:
        print(f"{ignorados} bens ignorados (candidatura não encontrada)")

    try:
        for _, row in df_total.iterrows():
            statement = insert(BemCandidato).values(
                    sq_candidato = row["SQ_CANDIDATO"],
                    nr_ordem_bem = row["NR_ORDEM_BEM_CANDIDATO"],
                    cd_tipo_bem = row["CD_TIPO_BEM_CANDIDATO"],
                    ds_tipo_bem = row["DS_TIPO_BEM_CANDIDATO"],
                    ds_bem = row["DS_BEM_CANDIDATO"],
                    vr_bem = row["VR_BEM_CANDIDATO"],
            ).on_conflict_do_update(
                    index_elements = ["sq_candidato", "nr_ordem_bem"],
                    set_ = {
                        "cd_tipo_bem": row["CD_TIPO_BEM_CANDIDATO"],
                        "ds_tipo_bem": row["DS_TIPO_BEM_CANDIDATO"],
                        "ds_bem": row["DS_BEM_CANDIDATO"],
                        "vr_bem": row["VR_BEM_CANDIDATO"],
                    }
            )
            session.execute(statement)

        session.commit()
        print(f"{len(df_total)} bens dos candidatos carregados com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar bens dos candidatos: {ex}")

    finally:
        session.close()

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_bens_candidato(data_dir)
