import pandas as pd
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from connection import Session
from models.rede_social import RedeSocial
from models.candidatura import Candidatura

ANOS = [2022]
COLUNAS = ["SQ_CANDIDATO", "NR_ORDEM", "DS_URL"]

TIPOS_REDE = {
    "instagram": "INSTAGRAM",
    "twitter": "TWITTER",
    "facebook": "FACEBOOK",
    "youtube": "YOUTUBE",
    "tiktok": "TIKTOK",
    "linkedin": "LINKEDIN",
}

def extrair_tipo_rede(url):
    if pd.isna(url):
        return None
    url_lower = url.lower()
    for chave, tipo in TIPOS_REDE.items():
        if chave in url_lower:
            return tipo
    return "OUTRO"

def load_redes_sociais(data_dir: Path):
    dfs = []

    for ano in ANOS:
        caminho = data_dir / str(ano) / "rede_social_candidato" / f"rede_social_candidato_{ano}_BR.csv"

        df = pd.read_csv(
                caminho,
                encoding = "latin-1",
                sep = ";",
                quotechar = '"',
                usecols = COLUNAS,
                dtype = {"SQ_CANDIDATO": str}
        )
        dfs.append(df)

    df_total = pd.concat(dfs, ignore_index = True)
    df_total.replace(["#NULO#", "#NULO", "#NE#", "#NE"], None, inplace = True)

    df_total.drop_duplicates(subset = ["SQ_CANDIDATO", "NR_ORDEM"], inplace = True)

    df_total["SQ_CANDIDATO"] = df_total["SQ_CANDIDATO"].str.strip()
    df_total["NR_ORDEM"] = df_total["NR_ORDEM"].astype(int)
    df_total["DS_URL"] = df_total["DS_URL"].str.strip()
    df_total["TIPO_REDE_SOCIAL"] = df_total["DS_URL"].apply(extrair_tipo_rede)

    session = Session()

    sqs_existentes = set(
        str(row[0]) for row in session.execute(select(Candidatura.sq_candidato)).fetchall()
    )
    antes = len(df_total)
    df_total = df_total[df_total["SQ_CANDIDATO"].isin(sqs_existentes)]
    ignorados = antes - len(df_total)
    if ignorados:
        print(f"{ignorados} redes sociais ignoradas (candidatura não encontrada)")

    try:
        for _, row in df_total.iterrows():
            statement = insert(RedeSocial).values(
                    sq_candidato = row["SQ_CANDIDATO"],
                    nr_ordem = row["NR_ORDEM"],
                    ds_url = row["DS_URL"],
                    tipo_rede_social = row["TIPO_REDE_SOCIAL"]
            ).on_conflict_do_update(
                    index_elements = ["sq_candidato", "nr_ordem"],
                    set_ = {
                        "ds_url": row["DS_URL"],
                        "tipo_rede_social": row["TIPO_REDE_SOCIAL"],
                    }
            )
            session.execute(statement)

        session.commit()
        print(f"{len(df_total)} redes sociais carregadas com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar redes sociais: {ex}")

    finally:
        session.close()

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_redes_sociais(data_dir)
