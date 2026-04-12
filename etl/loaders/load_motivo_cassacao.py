import pandas as pd
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from connection import Session
from models.motivo_cassacao import MotivoCassacao
from models.candidatura import Candidatura

ANOS = [2018]
COLUNAS = ["SQ_CANDIDATO", "DS_TP_MOTIVO", "DS_MOTIVO"]

def load_motivos_cassacao(data_dir: Path):
    dfs = []

    for ano in ANOS:
        caminho = data_dir / str(ano) / "motivo_cassacao" / f"motivo_cassacao_{ano}_BR.csv"

        df = pd.read_csv(
            caminho,
            encoding="latin-1",
            sep=";",
            quotechar='"',
            usecols=COLUNAS,
            dtype={"SQ_CANDIDATO": str},
        )
        dfs.append(df)

    df_total = pd.concat(dfs, ignore_index=True)
    df_total.replace(["#NULO#", "#NULO", "#NE#", "#NE"], None, inplace=True)

    df_total.drop_duplicates(subset=["SQ_CANDIDATO", "DS_MOTIVO"], inplace=True)

    df_total["SQ_CANDIDATO"] = df_total["SQ_CANDIDATO"].str.strip()
    df_total["DS_TP_MOTIVO"] = df_total["DS_TP_MOTIVO"].apply(lambda x: x.strip() if isinstance(x, str) else None)
    df_total["DS_MOTIVO"] = df_total["DS_MOTIVO"].apply(lambda x: x.strip() if isinstance(x, str) else None)

    session = Session()

    sqs_existentes = set(
        str(row[0]) for row in session.execute(select(Candidatura.sq_candidato)).fetchall()
    )
    antes = len(df_total)
    df_total = df_total[df_total["SQ_CANDIDATO"].isin(sqs_existentes)]
    ignorados = antes - len(df_total)

    if ignorados:
        print(f"{ignorados} motivos ignorados (candidatura não encontrada)")

    try:
        for _, row in df_total.iterrows():
            statement = insert(MotivoCassacao).values(
                sq_candidato=row["SQ_CANDIDATO"],
                ds_tp_motivo=row["DS_TP_MOTIVO"],
                ds_motivo=row["DS_MOTIVO"],
            ).on_conflict_do_update(
                index_elements=["sq_candidato", "ds_motivo"],
                set_={
                    "ds_tp_motivo": row["DS_TP_MOTIVO"],
                    "ds_motivo": row["DS_MOTIVO"],
                }
            )
            session.execute(statement)

        session.commit()
        print(f"{len(df_total)} motivos de cassacao carregados com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar motivos de cassacao: {ex}")

    finally:
        session.close()

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_motivos_cassacao(data_dir)

