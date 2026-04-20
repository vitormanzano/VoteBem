"""
Pipeline ETL do VoteBem.

Uso:
    python pipeline.py                  # download + carga + limpeza dos raws
    python pipeline.py --no-clean       # mantém os arquivos raw após a carga
    python pipeline.py --skip-download  # usa raws já existentes (dev)
"""

import argparse
from pathlib import Path

from downloader import download_todos, limpar_raw
from loaders.load_eleicao import load_eleicoes
from loaders.load_partido import load_partidos
from loaders.load_candidato import load_candidatos
from loaders.load_coligacao import load_coligacoes
from loaders.load_candidatura import load_candidaturas
from loaders.load_bem_candidato import load_bens_candidato
from loaders.load_rede_social import load_redes_sociais
from loaders.load_proposta_governo import load_propostas
from loaders.load_certidao_criminal import load_certidoes
from loaders.load_motivo_cassacao import load_motivos_cassacao
from loaders.load_despesa_candidato import load_despesas
from loaders.load_nota_fiscal import load_notas_fiscais
from loaders.load_resultado_turno import load_resultados_turno


DATA_DIR = Path(__file__).parent / "data" / "raw"


def executar_loaders(data_dir: Path):
    steps = [
        ("Eleições",             load_eleicoes),
        ("Partidos",             load_partidos),
        ("Candidatos",           load_candidatos),
        ("Coligações",           load_coligacoes),
        ("Candidaturas",         load_candidaturas),
        ("Resultados por turno", load_resultados_turno),
        ("Bens de candidato",    load_bens_candidato),
        ("Redes sociais",        load_redes_sociais),
        ("Propostas de governo", load_propostas),
        ("Certidões criminais",  load_certidoes),
        ("Motivos de cassação",  load_motivos_cassacao),
        ("Despesas de candidato", load_despesas),
        ("Notas fiscais",        load_notas_fiscais),
    ]

    for nome, fn in steps:
        print(f"\n[loader] {nome}...")
        try:
            fn(data_dir)
        except Exception as ex:
            print(f"[erro] {nome}: {ex}")


def main():
    parser = argparse.ArgumentParser(description="Pipeline ETL VoteBem")
    parser.add_argument("--no-clean", action="store_true",
                        help="Não apaga os arquivos raw após a carga")
    parser.add_argument("--skip-download", action="store_true",
                        help="Pula o download (usa raws já existentes)")
    args = parser.parse_args()

    if not args.skip_download:
        print("=== Download dos dados do TSE ===")
        download_todos()

    print("\n=== Carregando no banco ===")
    executar_loaders(DATA_DIR)

    if not args.no_clean:
        print("\n=== Limpando arquivos raw ===")
        limpar_raw()
    else:
        print("\n[info] Arquivos raw mantidos em", DATA_DIR)


if __name__ == "__main__":
    main()
