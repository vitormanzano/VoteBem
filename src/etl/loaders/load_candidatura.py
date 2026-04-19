import pandas as pd
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert

from connection import Session
from models.candidatura import Candidatura

ANOS = [2010, 2014, 2018, 2022]

COLUNAS_BASE = [
    "ANO_ELEICAO", "SQ_CANDIDATO", "NR_CPF_CANDIDATO", "CD_ELEICAO", "NR_TURNO",
    "NR_PARTIDO", "SQ_COLIGACAO", "NM_URNA_CANDIDATO",
    "CD_CARGO", "DS_CARGO", "SG_UF", "NR_CANDIDATO",
    "CD_SITUACAO_CANDIDATURA", "DS_SITUACAO_CANDIDATURA",
    "CD_OCUPACAO", "DS_OCUPACAO",
]

# só existem em alguns anos (ex: 2010)
COLUNAS_OPCIONAIS = ["VR_DESPESA_MAX_CAMPANHA", "ST_REELEICAO"]


def _montar_foto_url(ano: int, sq_candidato: str, fotos_dir: Path) -> str | None:
    # caminho relativo da foto se ela existir.
    # 2010, 2014 : BR{sq}_div.{jpg|jpeg}
    # 2018, 2022 : FBR{sq}_div.{jpg|jpeg}
    prefixo = "FBR" if ano >= 2018 else "BR"
    for ext in ("jpg", "jpeg"):
        nome = f"{prefixo}{sq_candidato}_div.{ext}"
        caminho = fotos_dir / nome
        if caminho.exists():
            return f"{ano}/foto_candidato/{nome}"
    return None


def _ler_csv_candidato(caminho: Path) -> pd.DataFrame:
    # Lê o consulta_cand do ano, pegando só colunas que existirem. 
    cabecalho = pd.read_csv(caminho, encoding="latin-1", sep=";", quotechar='"', nrows=0)
    colunas_presentes = list(cabecalho.columns)

    usecols = [c for c in COLUNAS_BASE if c in colunas_presentes]
    for c in COLUNAS_OPCIONAIS:
        if c in colunas_presentes:
            usecols.append(c)

    df = pd.read_csv(
        caminho,
        encoding="latin-1",
        sep=";",
        quotechar='"',
        usecols=usecols,
        dtype={
            "SQ_CANDIDATO": str,
            "SQ_COLIGACAO": str,
            "NR_CPF_CANDIDATO": str,
        },
    )

    for c in COLUNAS_OPCIONAIS:
        if c not in df.columns:
            df[c] = None

    return df


def load_candidaturas(data_dir: Path):
    dfs_cand = []

    for ano in ANOS:
        caminho_cand = data_dir / str(ano) / "consulta_candidato" / f"consulta_cand_{ano}_BR.csv"
        df = _ler_csv_candidato(caminho_cand)
        dfs_cand.append(df)

    df_total = pd.concat(dfs_cand, ignore_index=True)
    df_total.replace(["#NULO#", "#NULO", "#NE#", "#NE"], None, inplace=True)

    df_total["SQ_CANDIDATO"]     = df_total["SQ_CANDIDATO"].str.strip()
    df_total["NR_CPF_CANDIDATO"] = df_total["NR_CPF_CANDIDATO"].str.strip().str.zfill(11)
    df_total["CD_ELEICAO"]       = df_total["CD_ELEICAO"].astype(int)
    df_total["NR_TURNO"]         = df_total["NR_TURNO"].astype(int)
    df_total["NR_PARTIDO"]       = df_total["NR_PARTIDO"].astype(int)
    df_total["CD_CARGO"]         = df_total["CD_CARGO"].astype(int)
    df_total["NR_CANDIDATO"]     = df_total["NR_CANDIDATO"].astype(int)
    df_total["ANO_ELEICAO"]      = df_total["ANO_ELEICAO"].astype(int)

    df_total["SQ_COLIGACAO"]            = pd.to_numeric(df_total["SQ_COLIGACAO"], errors="coerce").astype("Int64")
    df_total["CD_SITUACAO_CANDIDATURA"] = pd.to_numeric(df_total["CD_SITUACAO_CANDIDATURA"], errors="coerce").astype("Int64")
    df_total["CD_OCUPACAO"]             = pd.to_numeric(df_total["CD_OCUPACAO"], errors="coerce").astype("Int64")

    df_total["VR_DESPESA_MAX_CAMPANHA"] = pd.to_numeric(
        df_total["VR_DESPESA_MAX_CAMPANHA"].astype(str).str.replace(",", ".", regex=False),
        errors="coerce",
    )

    for col in ["NM_URNA_CANDIDATO", "DS_CARGO", "SG_UF",
                "DS_SITUACAO_CANDIDATURA", "DS_OCUPACAO", "ST_REELEICAO"]:
        df_total[col] = df_total[col].where(df_total[col].notna(), None)
        df_total[col] = df_total[col].apply(lambda x: x.strip() if isinstance(x, str) else None)

    df_total.loc[df_total["SQ_COLIGACAO"].isin([-1, -3, -4]), "SQ_COLIGACAO"] = pd.NA

    df_total = df_total[df_total["SQ_CANDIDATO"].notna() & (df_total["SQ_CANDIDATO"] != "")]
    df_total["SQ_CANDIDATO"] = df_total["SQ_CANDIDATO"].astype("int64")

    df_cand = df_total.sort_values(["SQ_CANDIDATO", "NR_TURNO"]).drop_duplicates(
        subset="SQ_CANDIDATO", keep="last"
    )

    # foto_url
    def _foto(row):
        fotos_dir = data_dir / str(row["ANO_ELEICAO"]) / "foto_candidato"
        return _montar_foto_url(row["ANO_ELEICAO"], str(row["SQ_CANDIDATO"]), fotos_dir)

    df_cand["FOTO_URL"] = df_cand.apply(_foto, axis=1)

    session = Session()
    try:
        def v(row, col):
            val = row[col]
            return None if pd.isna(val) else val

        for _, row in df_cand.iterrows():
            statement = insert(Candidatura).values(
                sq_candidato            = int(row["SQ_CANDIDATO"]),
                nr_cpf_candidato        = row["NR_CPF_CANDIDATO"],
                cd_eleicao              = int(row["CD_ELEICAO"]),
                nr_partido              = int(row["NR_PARTIDO"]),
                sq_coligacao            = None if pd.isna(row["SQ_COLIGACAO"]) else int(row["SQ_COLIGACAO"]),
                nm_urna_candidato       = v(row, "NM_URNA_CANDIDATO"),
                cd_cargo                = int(row["CD_CARGO"]),
                ds_cargo                = v(row, "DS_CARGO"),
                sg_uf                   = v(row, "SG_UF"),
                nr_candidato            = int(row["NR_CANDIDATO"]),
                cd_situacao_candidatura = None if pd.isna(row["CD_SITUACAO_CANDIDATURA"]) else int(row["CD_SITUACAO_CANDIDATURA"]),
                ds_situacao_candidatura = v(row, "DS_SITUACAO_CANDIDATURA"),
                cd_ocupacao             = None if pd.isna(row["CD_OCUPACAO"]) else int(row["CD_OCUPACAO"]),
                ds_ocupacao             = v(row, "DS_OCUPACAO"),
                foto_url                = row["FOTO_URL"],
                st_reeleicao            = v(row, "ST_REELEICAO"),
                vr_despesa_max_campanha = None if pd.isna(row["VR_DESPESA_MAX_CAMPANHA"]) else float(row["VR_DESPESA_MAX_CAMPANHA"]),
            ).on_conflict_do_update(
                index_elements=["sq_candidato"],
                set_={
                    "nr_cpf_candidato":        row["NR_CPF_CANDIDATO"],
                    "cd_eleicao":              int(row["CD_ELEICAO"]),
                    "nr_partido":              int(row["NR_PARTIDO"]),
                    "sq_coligacao":            None if pd.isna(row["SQ_COLIGACAO"]) else int(row["SQ_COLIGACAO"]),
                    "nm_urna_candidato":       v(row, "NM_URNA_CANDIDATO"),
                    "cd_cargo":                int(row["CD_CARGO"]),
                    "ds_cargo":                v(row, "DS_CARGO"),
                    "sg_uf":                   v(row, "SG_UF"),
                    "nr_candidato":            int(row["NR_CANDIDATO"]),
                    "cd_situacao_candidatura": None if pd.isna(row["CD_SITUACAO_CANDIDATURA"]) else int(row["CD_SITUACAO_CANDIDATURA"]),
                    "ds_situacao_candidatura": v(row, "DS_SITUACAO_CANDIDATURA"),
                    "cd_ocupacao":             None if pd.isna(row["CD_OCUPACAO"]) else int(row["CD_OCUPACAO"]),
                    "ds_ocupacao":             v(row, "DS_OCUPACAO"),
                    "foto_url":                row["FOTO_URL"],
                    "st_reeleicao":            v(row, "ST_REELEICAO"),
                    "vr_despesa_max_campanha": None if pd.isna(row["VR_DESPESA_MAX_CAMPANHA"]) else float(row["VR_DESPESA_MAX_CAMPANHA"]),
                },
            )
            session.execute(statement)

        session.commit()
        print(f"{len(df_cand)} candidaturas carregadas com sucesso!")

        sem_foto = df_cand["FOTO_URL"].isna().sum()
        if sem_foto:
            print(f"{sem_foto} candidaturas ficaram sem foto_url (arquivo não encontrado).")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar candidaturas: {ex}")

    finally:
        session.close()


if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_candidaturas(data_dir)
