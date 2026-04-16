"""
Setup multiplataforma do VoteBem.

Uso:
    python3 setup.py                 # setup completo
    python3 setup.py --skip-pipeline # não roda o ETL no final
    python3 setup.py --skip-docker   # não sobe Postgres

Requer: Python ≥ 3.12, Docker + Docker Compose v2, arquivo .env na raiz.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
VENV_DIR = ROOT / ".venv"
ETL_DIR = ROOT / "etl"
REQUIREMENTS = ETL_DIR / "requirements.txt"
CONTAINER = "VoteBem"
IS_WINDOWS = os.name == "nt"

def venv_python() -> Path:
    return VENV_DIR / ("Scripts" if IS_WINDOWS else "bin") / ("python.exe" if IS_WINDOWS else "python")

def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, check=True, **kwargs)

def checar_prereqs() -> None:
    if sys.version_info < (3, 12):
        sys.exit(f"Python 3.12+ requerido (você está em {sys.version.split()[0]}).")
    if not shutil.which("docker"):
        sys.exit("Docker não encontrado no PATH.")
    if not ENV_FILE.exists():
        sys.exit(f"Arquivo .env não encontrado em {ENV_FILE}.")
    if not REQUIREMENTS.exists():
        sys.exit(f"{REQUIREMENTS} não encontrado.")

def carregar_env() -> dict[str, str]:
    valores: dict[str, str] = {}
    for linha in ENV_FILE.read_text().splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        k, v = linha.split("=", 1)
        valores[k.strip()] = v.strip().strip('"').strip("'")
    return valores

def subir_postgres(env: dict[str, str], timeout_s: int = 60) -> None:
    print("→ Subindo Postgres via Docker Compose...")
    run(["docker", "compose", "up", "-d"], cwd=ROOT)

    user = env.get("POSTGRES_USER")
    if not user:
        sys.exit("POSTGRES_USER não definido no .env.")

    print("→ Aguardando Postgres aceitar conexões...")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        r = subprocess.run(
            ["docker", "exec", CONTAINER, "pg_isready", "-U", user],
            capture_output=True,
        )
        if r.returncode == 0:
            print("  Postgres pronto.")
            return
        time.sleep(1)
    sys.exit(f"Postgres não respondeu em {timeout_s}s.")

def criar_venv() -> None:
    if VENV_DIR.exists():
        print(f"→ venv já existe em {VENV_DIR}, reusando.")
        return
    print(f"→ Criando venv em {VENV_DIR}...")
    venv.create(VENV_DIR, with_pip=True, upgrade_deps=False)

def instalar_deps() -> None:
    py = str(venv_python())
    print("→ Atualizando pip...")
    run([py, "-m", "pip", "install", "--upgrade", "pip"])
    print("→ Instalando dependências do ETL...")
    run([py, "-m", "pip", "install", "-r", str(REQUIREMENTS)])

def rodar_pipeline() -> None:
    py = str(venv_python())
    print("→ Executando pipeline ETL...")
    run([py, "pipeline.py"], cwd=ETL_DIR)

def main() -> None:
    parser = argparse.ArgumentParser(description="Setup VoteBem")
    parser.add_argument("--skip-docker", action="store_true", help="Não sobe o Postgres")
    parser.add_argument("--skip-pipeline", action="store_true", help="Não roda o ETL no final")
    args = parser.parse_args()

    checar_prereqs()
    env = carregar_env()

    if not args.skip_docker:
        subir_postgres(env)

    criar_venv()
    instalar_deps()

    if not args.skip_pipeline:
        rodar_pipeline()

    ativar = ".venv\\Scripts\\activate" if IS_WINDOWS else "source .venv/bin/activate"
    print(f"\n✓ Setup concluído. Ative o venv com: {ativar}")

if __name__ == "__main__":
    main()
