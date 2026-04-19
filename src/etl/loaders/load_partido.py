import pandas as pd
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert

from connection import Session
from models.partido import Partido

ANOS = [2010, 2014, 2018, 2022]
COLUNAS = ["NR_PARTIDO", "SG_PARTIDO", "NM_PARTIDO"]

def load_partidos(data_dir: Path):
    dfs = []

    for ano in ANOS:
        caminho = data_dir / str(ano) / "consulta_candidato" / f"consulta_cand_{ano}_BR.csv"
        
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

    df_total = df_total[~df_total["NR_PARTIDO"].isin(["-1", "-3"])] # Descarta linhas com NR_PARTIDO inválido

    df_total.drop_duplicates(subset = "NR_PARTIDO", inplace = True)
    
    df_total["NR_PARTIDO"] = df_total["NR_PARTIDO"].astype(int)
    df_total["SG_PARTIDO"] = df_total["SG_PARTIDO"].str.strip()
    df_total["NM_PARTIDO"] = df_total["NM_PARTIDO"].str.strip()


    session = Session()

    try:
        for _, row in df_total.iterrows():
            statement = insert(Partido).values(
                    nr_partido = row["NR_PARTIDO"],
                    sg_partido = row["SG_PARTIDO"],
                    nm_partido = row["NM_PARTIDO"]
            ).on_conflict_do_update( 
                    index_elements = ["nr_partido"],
                    set_ = {
                        "sg_partido": row["SG_PARTIDO"],
                        "nm_partido": row["NM_PARTIDO"],
                        }
            )
            session.execute(statement)

        session.commit()
        print(f"{len(df_total)} partidos carregados com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar partidos: {ex}")

    finally:
        session.close()

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_partidos(data_dir)
