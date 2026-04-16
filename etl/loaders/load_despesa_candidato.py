import pandas as pd
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

import unicodedata
from connection import Session
from models.candidatura import Candidatura
from models.despesa_candidato import DespesaCandidato

ANOS = [2010, 2014, 2018, 2022]

ALIASES = {
    "SQ_CANDIDATO": ["Sequencial Candidato"],
    "NR_DOCUMENTO": ["Número do documento", "Numero do documento"],
    "CPF_CNPJ_FORNECEDOR": ["CPF/CNPJ do fornecedor"],
    "NM_FORNECEDOR": ["Nome do fornecedor"],
    "DT_DESPESA": ["Data da despesa"],
    "VR_DESPESA": ["Valor despesa"],
    "DS_TIPO_DESPESA": ["Tipo despesa"],
    "DS_FONTE_RECURSO": ["Fonte recurso"],
    "DS_ESPECIE_RECURSO": ["Espécie recurso", "Especie recurso"],
    "DS_DESPESA": ["Descriçao da despesa", "Descrição da despesa", "Descricao da despesa"],
}

def _strip_or_none(valor):
    return valor.strip() if isinstance(valor, str) else None

def _normalizar_nome_coluna(nome: str) -> str:
    nome = str(nome).strip().lower()
    nome = unicodedata.normalize("NFKD", nome)
    nome = "".join(ch for ch in nome if not unicodedata.combining(ch))
    return " ".join(nome.split())

ALIASES = {
    "SQ_CANDIDATO": ["sequencial candidato"],
    "NR_DOCUMENTO": ["numero do documento"],
    "CPF_CNPJ_FORNECEDOR": ["cpf/cnpj do fornecedor"],
    "NM_FORNECEDOR": ["nome do fornecedor"],
    "DT_DESPESA": ["data da despesa"],
    "VR_DESPESA": ["valor despesa"],
    "DS_TIPO_DESPESA": ["tipo despesa"],
    "DS_FONTE_RECURSO": ["fonte recurso"],
    "DS_ESPECIE_RECURSO": ["especie recurso"],
    "DS_DESPESA": ["descricao da despesa"],
}

def _resolver_colunas(caminho: Path):
    cabecalho = pd.read_csv(
        caminho,
        encoding="latin-1",
        sep=";",
        quotechar='"',
        nrows=0,
    )

    originais = list(cabecalho.columns)
    normalizadas = {_normalizar_nome_coluna(col): col for col in originais}

    mapeamento = {}
    faltando = []

    for destino, opcoes in ALIASES.items():
        encontrada = None
        for opcao in opcoes:
            if opcao in normalizadas:
                encontrada = normalizadas[opcao]
                break

        if encontrada is None:
            faltando.append(destino)
        else:
            mapeamento[encontrada] = destino

    if faltando:
        raise ValueError(
            f"Colunas não encontradas em {caminho.name}: {faltando}. "
            f"Colunas disponíveis: {originais}"
        )

    return list(mapeamento.keys()), mapeamento

def _ler_despesas(caminho: Path) -> pd.DataFrame:
    usecols, rename_map = _resolver_colunas(caminho)

    df = pd.read_csv(
        caminho,
        encoding="latin-1",
        sep=";",
        quotechar='"',
        usecols=usecols,
        dtype={
            "Sequencial Candidato": str,
            "Número do documento": str,
            "Numero do documento": str,
            "CPF/CNPJ do fornecedor": str,
        },
    )

    df.rename(columns=rename_map, inplace=True)
    return df

def load_despesas(data_dir: Path):
    dfs = []

    for ano in ANOS:
        base = data_dir / str(ano) / "prestacao_contas" / "candidato"
        if not base.exists():
            continue
        arquivos = list(base.glob("**/DespesasCandidatos.txt")) + list(base.glob("**/despesas_candidatos_*.csv"))
        for caminho in arquivos:
            try:
                dfs.append(_ler_despesas(caminho))
            except Exception as ex:
                print(f"[aviso] falhou em {caminho}: {ex}")

    if not dfs:
        print("Nenhum arquivo de despesas encontrado.")
        return

    df = pd.concat(dfs, ignore_index=True)
    df.replace(["#NULO#", "#NULO", "#NE#", "#NE"], None, inplace=True)

    for col in [
        "SQ_CANDIDATO",
        "NR_DOCUMENTO",
        "CPF_CNPJ_FORNECEDOR",
        "NM_FORNECEDOR",
        "DS_TIPO_DESPESA",
        "DS_FONTE_RECURSO",
        "DS_ESPECIE_RECURSO",
        "DS_DESPESA",
    ]:
        df[col] = df[col].apply(_strip_or_none)

    df = df[df["SQ_CANDIDATO"].notna() & (df["SQ_CANDIDATO"] != "")]
    df["SQ_CANDIDATO"] = pd.to_numeric(df["SQ_CANDIDATO"], errors="coerce").astype("Int64")

    df["DT_DESPESA"] = pd.to_datetime(df["DT_DESPESA"], format="%d/%m/%Y", errors="coerce").dt.date
    df["VR_DESPESA"] = pd.to_numeric(
        df["VR_DESPESA"].astype(str).str.replace(",", ".", regex=False),
        errors="coerce",
    )

    df = df[df["SQ_CANDIDATO"].notna()]
    df.drop_duplicates(
        subset=["SQ_CANDIDATO", "NR_DOCUMENTO", "CPF_CNPJ_FORNECEDOR", "DT_DESPESA"],
        inplace=True,
    )

    session = Session()

    try:
        sqs_existentes = {
            int(row[0]) for row in session.execute(select(Candidatura.sq_candidato)).fetchall()
        }

        antes = len(df)
        df = df[df["SQ_CANDIDATO"].astype(int).isin(sqs_existentes)]
        ignorados = antes - len(df)

        if ignorados:
            print(f"{ignorados} despesas ignoradas (candidatura não encontrada)")

        def v(row, col):
            valor = row[col]
            return None if pd.isna(valor) else valor

        for _, row in df.iterrows():
            statement = insert(DespesaCandidato).values(
                sq_candidato=int(row["SQ_CANDIDATO"]),
                nr_documento=v(row, "NR_DOCUMENTO"),
                cpf_cnpj_fornecedor=v(row, "CPF_CNPJ_FORNECEDOR"),
                nm_fornecedor=v(row, "NM_FORNECEDOR"),
                dt_despesa=v(row, "DT_DESPESA"),
                vr_despesa=None if pd.isna(row["VR_DESPESA"]) else float(row["VR_DESPESA"]),
                ds_tipo_despesa=v(row, "DS_TIPO_DESPESA"),
                ds_fonte_recurso=v(row, "DS_FONTE_RECURSO"),
                ds_especie_recurso=v(row, "DS_ESPECIE_RECURSO"),
                ds_despesa=v(row, "DS_DESPESA"),
            ).on_conflict_do_update(
                index_elements=[
                    "sq_candidato",
                    "nr_documento",
                    "cpf_cnpj_fornecedor",
                    "dt_despesa",
                ],
                set_={
                    "nm_fornecedor": v(row, "NM_FORNECEDOR"),
                    "vr_despesa": None if pd.isna(row["VR_DESPESA"]) else float(row["VR_DESPESA"]),
                    "ds_tipo_despesa": v(row, "DS_TIPO_DESPESA"),
                    "ds_fonte_recurso": v(row, "DS_FONTE_RECURSO"),
                    "ds_especie_recurso": v(row, "DS_ESPECIE_RECURSO"),
                    "ds_despesa": v(row, "DS_DESPESA"),
                },
            )
            session.execute(statement)

        session.commit()
        print(f"{len(df)} despesas de candidatos carregadas com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar despesas: {ex}")

    finally:
        session.close()

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_despesas(data_dir)

