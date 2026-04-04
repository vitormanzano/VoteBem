import pandas as pd
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert

from etl.connection import Session
from etl.models.eleicao import Eleicao 

ANOS = [2010, 2014, 2018, 2022]
COLUNAS = ["CD_ELEICAO", "NR_TURNO", "DS_ELEICAO", "CD_TIPO_ELEICAO", "DT_ELEICAO"]

def load_eleicoes(data_dir: Path):
    dfs = []

    for ano in ANOS:
        caminho = data_dir / str(ano) / "consulta_cand" / f"consulta_cand_{ano}_BR.csv"

        df = pd.read_csv(
                caminho,
                encoding = "latin-1",
                sep = ";",
                quotechar = '"',
                usecols = COLUNAS
        )  
        dfs.append(df)

    df_total = pd.concat(dfs, ignore_index = True)

    df_total.replace(["#NULO#", "#NULO", "#NE#", "#NE"], None, inplace = True)

    df_total = df_total[~df_total["CD_ELEICAO"].isin(["-1", "-3"])]

    df_total.drop_duplicates(subset = "CD_ELEICAO", inplace = True)

    df_total["CD_ELEICAO"] = df_total["CD_ELEICAO"].astype(int)
    df_total["NR_TURNO"] = df_total["NR_TURNO"].astype(int)
    df_total["DS_ELEICAO"] = df_total["DS_ELEICAO"].str.strip()
    df_total["CD_TIPO_ELEICAO"] = df_total["CD_TIPO_ELEICAO"].astype(int)
    df_total["DT_ELEICAO"] = pd.to_datetime(df_total["DT_ELEICAO"], format="%d/%m/%Y").dt.date                         

    session =  Session()

    try:
        for _, row in df_total.iterrows():
            statement = insert(Eleicao).values(
                    nr_eleicao = row["CD_ELEICAO"],
                    nr_turno = row["NR_TURNO"],
                    ds_eleicao = row["DS_ELEICAO"],
                    cd_tipo_eleicao = row ["CD_TIPO_ELEICAO"],
                    dt_eleicao = row["DT_ELEICAO"]
            ).on_conflict_do_update(
                    index_elements = ["nr_eleicao"],
                    set_ = {
                        "nr_turno": row["NR_TURNO"],
                        "ds_eleicao": row["DS_ELEICAO"],
                        "cd_tipo_eleicao": row["CD_TIPO_ELEICAO"],
                        "dt_eleicao": row["DT_ELEICAO"],
                        }
            )
            session.execute(statement)

        session.commit()
        print(f"{len(df_total)} eleições carregadas com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar eleições {ex}")

    finally:
        session.close()

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_eleicoes(data_dir)
