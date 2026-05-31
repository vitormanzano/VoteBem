import pandas as pd
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert

from connection import Session
from models.candidato import Candidato 

ANOS = [2010, 2014, 2018, 2022]
COLUNAS = ["SQ_CANDIDATO", "NR_CPF_CANDIDATO", "NM_CANDIDATO", "NM_SOCIAL_CANDIDATO", "NM_URNA_CANDIDATO", "DT_NASCIMENTO", "SG_UF_NASCIMENTO", "CD_GENERO", "DS_GENERO", "CD_GRAU_INSTRUCAO", "DS_GRAU_INSTRUCAO", "CD_ESTADO_CIVIL", "DS_ESTADO_CIVIL", "CD_COR_RACA", "DS_COR_RACA"]

def _cpf_valido(cpf: str) -> bool:
    return bool(cpf) and cpf.isdigit() and len(cpf) == 11 and cpf != "00000000000"

def load_candidatos(data_dir: Path):
    dfs = []

    for ano in ANOS:
        caminho = data_dir / str(ano) / "consulta_candidato" / f"consulta_cand_{ano}_BR.csv"

        df = pd.read_csv(
                caminho,
                encoding = "latin-1",
                sep = ";",
                quotechar = '"',
                usecols = COLUNAS,
                dtype={"SQ_CANDIDATO": str, "NR_CPF_CANDIDATO": str},
        )
        df["_ANO"] = ano
        dfs.append(df)


    df_total = pd.concat(dfs, ignore_index=True)
    df_total.replace(["#NULO#", "#NULO", "#NE#", "#NE"], None, inplace=True)

    df_total["SQ_CANDIDATO"] = df_total["SQ_CANDIDATO"].str.strip().astype("int64")
    df_total["NR_CPF_CANDIDATO"] = df_total["NR_CPF_CANDIDATO"].astype(str).str.strip().str.zfill(11)

    # CPF inválido → CPF sintético por SQ (provisório, pode ser substituído abaixo).
    df_total["NR_CPF_CANDIDATO"] = df_total.apply(
        lambda r: r["NR_CPF_CANDIDATO"] if _cpf_valido(r["NR_CPF_CANDIDATO"])
                  else f"SQ{str(r['SQ_CANDIDATO'])[-9:]}",
        axis=1,
    )

    # Se a mesma pessoa (nome + nascimento) tem CPF real em algum ano, usa ele em todos.
    # Isso evita que candidatos de 2014 (sem CPF) apareçam duplicados para quem tem CPF em 2018/2022.
    df_total["_CHAVE_PESSOA"] = (
        df_total["NM_CANDIDATO"].str.strip().str.upper() + "|" +
        df_total["DT_NASCIMENTO"].astype(str)
    )
    cpf_real_por_pessoa = (
        df_total[df_total["NR_CPF_CANDIDATO"].apply(_cpf_valido)]
        .groupby("_CHAVE_PESSOA")["NR_CPF_CANDIDATO"]
        .first()
    )
    df_total["NR_CPF_CANDIDATO"] = df_total.apply(
        lambda r: cpf_real_por_pessoa.get(r["_CHAVE_PESSOA"], r["NR_CPF_CANDIDATO"]),
        axis=1,
    )
    df_total.drop(columns=["_CHAVE_PESSOA"], inplace=True)

    # Para a mesma pessoa (mesmo CPF final) em vários anos, mantém o registro mais recente.
    df_total.sort_values("_ANO", inplace=True)
    df_total.drop_duplicates(subset="NR_CPF_CANDIDATO", keep="last", inplace=True)
    df_total.drop(columns=["_ANO", "SQ_CANDIDATO"], inplace=True)

    df_total["NM_CANDIDATO"] = df_total["NM_CANDIDATO"].str.strip()
    df_total["NM_SOCIAL_CANDIDATO"] = df_total["NM_SOCIAL_CANDIDATO"].str.strip()
    df_total["NM_URNA_CANDIDATO"] = df_total["NM_URNA_CANDIDATO"].str.strip()
    df_total["DT_NASCIMENTO"] = pd.to_datetime(df_total["DT_NASCIMENTO"], format = "%d/%m/%Y").dt.date
    df_total["SG_UF_NASCIMENTO"] = df_total["SG_UF_NASCIMENTO"].str.strip()
    df_total["CD_GENERO"] = df_total["CD_GENERO"].astype(int)
    df_total["DS_GENERO"] = df_total["DS_GENERO"].str.strip()
    df_total["CD_GRAU_INSTRUCAO"] = df_total["CD_GRAU_INSTRUCAO"].astype(int)
    df_total["DS_GRAU_INSTRUCAO"] = df_total["DS_GRAU_INSTRUCAO"].str.strip()
    df_total["CD_ESTADO_CIVIL"] = df_total["CD_ESTADO_CIVIL"].astype(int)
    df_total["DS_ESTADO_CIVIL"] = df_total["DS_ESTADO_CIVIL"].str.strip()
    df_total["CD_COR_RACA"] = df_total["CD_COR_RACA"].astype(int)
    df_total["DS_COR_RACA"] = df_total["DS_COR_RACA"].str.strip()

    session = Session()

    try:
        for _, row in df_total.iterrows():
            statement = insert(Candidato).values(
                    nr_cpf_candidato = row["NR_CPF_CANDIDATO"],
                    nm_candidato = row["NM_CANDIDATO"],
                    nm_social_candidato = row["NM_SOCIAL_CANDIDATO"],
                    nm_urna_candidato = row["NM_URNA_CANDIDATO"],
                    dt_nascimento = row["DT_NASCIMENTO"],
                    sg_uf_nascimento = row["SG_UF_NASCIMENTO"],
                    cd_genero = row["CD_GENERO"],
                    ds_genero = row["DS_GENERO"],
                    cd_grau_instrucao = row["CD_GRAU_INSTRUCAO"],
                    ds_grau_instrucao = row["DS_GRAU_INSTRUCAO"],
                    cd_estado_civil = row["CD_ESTADO_CIVIL"],
                    ds_estado_civil = row["DS_ESTADO_CIVIL"],
                    cd_cor_raca = row["CD_COR_RACA"],
                    ds_cor_raca = row["DS_COR_RACA"],
            ).on_conflict_do_update(
                    index_elements = ["nr_cpf_candidato"],
                    set_ = {
                        "nm_candidato": row["NM_CANDIDATO"],
                        "nm_social_candidato": row["NM_SOCIAL_CANDIDATO"],
                        "nm_urna_candidato": row["NM_URNA_CANDIDATO"],
                        "dt_nascimento": row["DT_NASCIMENTO"],
                        "sg_uf_nascimento": row["SG_UF_NASCIMENTO"],
                        "cd_genero": row["CD_GENERO"],
                        "ds_genero": row["DS_GENERO"],
                        "cd_grau_instrucao": row["CD_GRAU_INSTRUCAO"],
                        "ds_grau_instrucao": row["DS_GRAU_INSTRUCAO"],
                        "cd_estado_civil": row["CD_ESTADO_CIVIL"],
                        "ds_estado_civil": row["DS_ESTADO_CIVIL"],
                        "cd_cor_raca": row["CD_COR_RACA"],
                        "ds_cor_raca": row["DS_COR_RACA"],
                    }
            )
            session.execute(statement)

        session.commit()
        print(f"{len(df_total)} candidatos carregados com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar candidatos: {ex}")

    finally:
        session.close()

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_candidatos(data_dir)

