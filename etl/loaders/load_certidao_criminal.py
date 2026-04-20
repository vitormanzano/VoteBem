import shutil
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from connection import Session
from downloader import STORAGE_DIR
from models.certidao_criminal import CertidaoCriminal
from models.candidatura import Candidatura

ANOS = [2018, 2022]

def load_certidoes(data_dir: Path):
    arquivos = []

    for ano in ANOS:
        pasta = data_dir / str(ano) / "certidoes_criminais_candidato"
        if not pasta.exists():
            continue

        for arquivo in pasta.glob("*.pdf"):
            if arquivo.name == "leiame.pdf":
                continue

            # 2018BR280000601016_280005507601.pdf → sq=280000601016, id=280005507601
            partes = arquivo.stem.split("_")
            if len(partes) != 2:
                continue

            sq_candidato = partes[0].replace(f"{ano}BR", "")
            id_certidao = partes[1]

            dest_dir = STORAGE_DIR / "certidoes"
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(arquivo, dest_dir / arquivo.name)

            arquivos.append({
                "id_certidao": id_certidao,
                "sq_candidato": sq_candidato,
                "nm_arquivo": arquivo.name,
                "ds_caminho_arquivo": f"certidoes/{arquivo.name}",
            })

    session = Session()

    # Filtrar apenas certidões de candidaturas existentes
    sqs_existentes = set(
        str(row[0]) for row in session.execute(select(Candidatura.sq_candidato)).fetchall()
    )

    ignorados = [a for a in arquivos if a["sq_candidato"] not in sqs_existentes]
    arquivos = [a for a in arquivos if a["sq_candidato"] in sqs_existentes]

    if ignorados:
        print(f"{len(ignorados)} certidões ignoradas (candidatura não encontrada)")

    try:
        for arq in arquivos:
            statement = insert(CertidaoCriminal).values(
                id_certidao = arq["id_certidao"],
                sq_candidato = arq["sq_candidato"],
                nm_arquivo = arq["nm_arquivo"],
                ds_caminho_arquivo = arq["ds_caminho_arquivo"],
            ).on_conflict_do_update(
                index_elements = ["id_certidao"],
                set_ = {
                    "sq_candidato": arq["sq_candidato"],
                    "nm_arquivo": arq["nm_arquivo"],
                    "ds_caminho_arquivo": arq["ds_caminho_arquivo"],
                }
            )
            session.execute(statement)

        session.commit()
        print(f"{len(arquivos)} certidões criminais carregadas com sucesso!")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao carregar certidões criminais: {ex}")

    finally:
        session.close()

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    load_certidoes(data_dir)
