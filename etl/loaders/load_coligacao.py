import pandas as pd
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert

from connection import Session
from models.coligacao import Coligacao

ANOS = [2010, 2014, 2018, 2022]
COLUNAS = ["SQ_COLIGACAO", "CD_ELEICAO", "NR_TURNO", "NM_COLIGACAO", "DS_COMPOSICAO_COLIGACAO", "TP_AGREMIACAO", "SG_UF"]

def load_coligacoes(data_dir: Path):
    dfs = []

    for ano in ANOS:
        caminho = data_dir / str(ano) / "consulta_coligacao" / f"consulta_coligacao_{ano}_BR.csv" 

        df = pd.read_csv(
                caminho,
                encoding = "latin-1",
                sep = ";",
                quotechar = '"',
                usecols = COLUNAS,
                dtype = {"SQ_COLIGACAO": str}
        )
        dfs.append(df)
    
    df_total = pd.concat(dfs, ignore_index = True)
    df_total.replace(["#NULO#", "#NULO", "#NE#", "#NE"], None, inplace = True)
    df_total = df_total[~df_total["SQ_COLIGACAO"].isin(["-1", "-3"])]

    df_total.drop_duplicates(subset = "SQ_COLIGACAO", inplace = True)

    df_total["SQ_COLIGACAO"] = df_total["SQ_COLIGACAO"].str.strip()
    df_total["CD_ELEICAO"] = df_total["CD_ELEICAO"].astype(int)
    df_total["NR_TURNO"] = df_total["NR_TURNO"].astype(int)
    df_total["NM_COLIGACAO"] = df_total["NM_COLIGACAO"].str.strip()
    df_total["DS_COMPOSICAO_COLIGACAO"] = df_total["DS_COMPOSICAO_COLIGACAO"].str.strip()
    df_total["TP_AGREMIACAO"] = df_total["TP_AGREMIACAO"].str.strip()
    df_total["SG_UF"] = df_total["SG_UF"].str.strip()

    session = Session()

    try:
        for _, row in df_total.iterrows():
            statement = insert(Coligacao).values(
                    sq_coligacao = row["SQ_COLIGACAO"],
                    cd_eleicao = row["CD_ELEICAO"],
                    nr_turno = row["NR_TURNO"],
                    nm_coligacao = row["NM_COLIGACAO"],
                    ds_composicao_coligacao = row["DS_COMPOSICAO_COLIGACAO"],
                    tp_agremiacao = row["TP_AGREMIACAO"],
                    sg_uf = row["SG_UF"]
            ).on_conflict_do_update(
                index_elements = ["sq_coligacao"],
                set_ = {
                    "cd_eleicao": row["CD_ELEICAO"],
                    "nr_turno": row["NR_TURNO"],
                    "nm_coligacao": row["NM_COLIGACAO"],
                    "ds_composicao_coligacao": row["DS_COMPOSICAO_COLIGACAO"],
                    "tp_agremiacao": row["TP_AGREMIACAO"],
                    "sg_uf": row["SG_UF"],
                    }
            )
            session.execute(statement)

        session.commit()
        print(f"{len(df_total)} coligações carregados com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar coligações: {ex}")

    finally:
        session.close()

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_coligacoes(data_dir)
