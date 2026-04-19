import pandas as pd
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert

from connection import Session
from models.resultado_turno import ResultadoTurno

ANOS = [2010, 2014, 2018, 2022]

COLUNAS_CAND = [
    "SQ_CANDIDATO", "CD_ELEICAO", "NR_TURNO",
    "CD_SIT_TOT_TURNO", "DS_SIT_TOT_TURNO",
]
COLUNAS_VOTOS = ["SQ_CANDIDATO", "NR_TURNO", "QT_VOTOS_NOMINAIS"]


def load_resultados_turno(data_dir: Path):
    dfs_cand = []
    dfs_votos = []

    for ano in ANOS:
        caminho_cand = data_dir / str(ano) / "consulta_candidato" / f"consulta_cand_{ano}_BR.csv"
        df = pd.read_csv(
            caminho_cand,
            encoding="latin-1",
            sep=";",
            quotechar='"',
            usecols=COLUNAS_CAND,
            dtype={"SQ_CANDIDATO": str},
        )
        dfs_cand.append(df)

        caminho_votos = data_dir / str(ano) / "votacao_candidato_munzona" / f"votacao_candidato_munzona_{ano}_BR.csv"
        if caminho_votos.exists():
            df_v = pd.read_csv(
                caminho_votos,
                encoding="latin-1",
                sep=";",
                quotechar='"',
                usecols=COLUNAS_VOTOS,
                dtype={"SQ_CANDIDATO": str},
            )
            dfs_votos.append(df_v)

    df = pd.concat(dfs_cand, ignore_index=True)
    df_votos = pd.concat(dfs_votos, ignore_index=True) if dfs_votos else pd.DataFrame(
        columns=["SQ_CANDIDATO", "NR_TURNO", "QT_VOTOS_NOMINAIS"]
    )

    df.replace(["#NULO#", "#NULO", "#NE#", "#NE"], None, inplace=True)

    df["SQ_CANDIDATO"]     = df["SQ_CANDIDATO"].str.strip()
    df["CD_ELEICAO"]       = df["CD_ELEICAO"].astype(int)
    df["NR_TURNO"]         = df["NR_TURNO"].astype(int)
    df["CD_SIT_TOT_TURNO"] = pd.to_numeric(df["CD_SIT_TOT_TURNO"], errors="coerce").astype("Int64")
    df["DS_SIT_TOT_TURNO"] = df["DS_SIT_TOT_TURNO"].where(df["DS_SIT_TOT_TURNO"].notna(), None)
    df["DS_SIT_TOT_TURNO"] = df["DS_SIT_TOT_TURNO"].apply(
        lambda x: x.strip() if isinstance(x, str) else None
    )

    df = df[df["SQ_CANDIDATO"].notna() & (df["SQ_CANDIDATO"] != "")]
    df["SQ_CANDIDATO"] = df["SQ_CANDIDATO"].astype("int64")

    # Uma linha por (sq_candidato, nr_turno)
    df = df.drop_duplicates(subset=["SQ_CANDIDATO", "NR_TURNO"])

    # Agrega votos por (candidato, turno)
    df_votos = df_votos.groupby(["SQ_CANDIDATO", "NR_TURNO"], as_index=False)["QT_VOTOS_NOMINAIS"].sum()
    df_votos.rename(columns={"QT_VOTOS_NOMINAIS": "NR_VOTOS"}, inplace=True)
    df_votos["SQ_CANDIDATO"] = df_votos["SQ_CANDIDATO"].str.strip().astype("int64")
    df_votos["NR_TURNO"] = df_votos["NR_TURNO"].astype(int)

    df = df.merge(df_votos, on=["SQ_CANDIDATO", "NR_TURNO"], how="left")
    df["NR_VOTOS"] = df["NR_VOTOS"].fillna(0).astype(int)

    session = Session()
    try:
        for _, row in df.iterrows():
            stmt = insert(ResultadoTurno).values(
                sq_candidato     = int(row["SQ_CANDIDATO"]),
                cd_eleicao       = int(row["CD_ELEICAO"]),
                nr_turno         = int(row["NR_TURNO"]),
                nr_votos         = int(row["NR_VOTOS"]),
                cd_sit_tot_turno = None if pd.isna(row["CD_SIT_TOT_TURNO"]) else int(row["CD_SIT_TOT_TURNO"]),
                ds_sit_tot_turno = row["DS_SIT_TOT_TURNO"],
            ).on_conflict_do_update(
                index_elements=["sq_candidato", "nr_turno"],
                set_={
                    "cd_eleicao":       int(row["CD_ELEICAO"]),
                    "nr_votos":         int(row["NR_VOTOS"]),
                    "cd_sit_tot_turno": None if pd.isna(row["CD_SIT_TOT_TURNO"]) else int(row["CD_SIT_TOT_TURNO"]),
                    "ds_sit_tot_turno": row["DS_SIT_TOT_TURNO"],
                },
            )
            session.execute(stmt)

        session.commit()
        print(f"{len(df)} resultados por turno carregados com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar resultados por turno: {ex}")

    finally:
        session.close()


if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_resultados_turno(data_dir)
