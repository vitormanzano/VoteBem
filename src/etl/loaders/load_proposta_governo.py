from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from connection import Session
from models.proposta_governo import PropostaGoverno
from models.candidatura import Candidatura

ANOS = [2010, 2014, 2018, 2022]

def load_propostas(data_dir: Path):
    arquivos = []

    for ano in ANOS:
        pasta = data_dir / str(ano) / "propostas"

        for arquivo in pasta.glob("*.pdf"):
            if arquivo.name == "leiame.pdf":
                continue

            # 2022BR280001600167.pdf → 280001600167
            sq_candidato = arquivo.stem.replace(f"{ano}BR", "")

            arquivos.append({
                "sq_candidato": sq_candidato,
                "nm_arquivo": arquivo.name,
                "ds_caminho_arquivo": str(arquivo),
            })

    session = Session()

    # Buscar SQ_CANDIDATO existente na tabela candidatura
    sqs_existentes = set(
        str(row[0]) for row in session.execute(select(Candidatura.sq_candidato)).fetchall()
    )

    # Filtrar apenas propostas de candidaturas existentes
    ignorados = [a for a in arquivos if a["sq_candidato"] not in sqs_existentes]
    arquivos = [a for a in arquivos if a["sq_candidato"] in sqs_existentes]

    if ignorados:
        print(f"{len(ignorados)} propostas ignoradas (candidatura não encontrada)")

    try:
        for arq in arquivos:
            statement = insert(PropostaGoverno).values(
                sq_candidato = arq["sq_candidato"],
                nm_arquivo = arq["nm_arquivo"],
                ds_caminho_arquivo = arq["ds_caminho_arquivo"],
            ).on_conflict_do_update(
                index_elements = ["sq_candidato"],
                set_ = {
                    "nm_arquivo": arq["nm_arquivo"],
                    "ds_caminho_arquivo": arq["ds_caminho_arquivo"],
                }
            )
            session.execute(statement)

        session.commit()
        print(f"{len(arquivos)} propostas de governo carregadas com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar propostas de governo: {ex}")

    finally:
        session.close()

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_propostas(data_dir)
