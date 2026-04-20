import shutil
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

BASE = Path(__file__).parent / "data" / "raw"
STORAGE_DIR = Path(__file__).parent / "data" / "storage"

TSE_CDN = "https://cdn.tse.jus.br/estatistica/sead/odsele"
TSE_BASE = "https://cdn.tse.jus.br/estatistica/sead"


def _default_url(dataset: str, ano: int) -> str:
    return f"{TSE_CDN}/{dataset}/{dataset}_{ano}.zip"


def _csv_br_filter(name: str) -> bool:
    return name.upper().endswith("_BR.CSV")


def _prestacao_filter(name: str) -> bool:
    return "candidato" in name.lower() and not name.endswith("/")


def _any_filter(_name: str) -> bool:
    return True


# Overrides por dataset: (url_builder, member_filter)
def _flat_extract(z: zipfile.ZipFile, members: list[str], destino: Path) -> None:
    """Extrai cada membro diretamente em destino/, sem preservar subpastas."""
    for m in members:
        nome = Path(m).name
        if not nome:
            continue
        with z.open(m) as src, (destino / nome).open("wb") as dst:
            shutil.copyfileobj(src, dst)


def _prestacao_extract(z: zipfile.ZipFile, members: list[str], destino: Path) -> None:
    """Extrai apenas files sob candidato/ do BR (ou sem UF), descartando componente UF.

    Layout alvo: destino/candidato/<arquivo>
    """
    alvo_dir = destino / "candidato"
    alvo_dir.mkdir(parents=True, exist_ok=True)
    for m in members:
        partes = [p for p in m.split("/") if p]
        # Precisa começar com 'candidato'
        if not partes or partes[0].lower() != "candidato":
            continue
        # Se houver UF entre candidato e o arquivo, aceita só BR
        if len(partes) >= 3:
            uf = partes[1]
            if uf.upper() != "BR":
                continue
        nome = partes[-1]
        with z.open(m) as src, (alvo_dir / nome).open("wb") as dst:
            shutil.copyfileobj(src, dst)


# Overrides por dataset: (url_builder, member_filter, extractor)
DATASET_OVERRIDES = {
    "consulta_candidato": (
        lambda ano: f"{TSE_CDN}/consulta_cand/consulta_cand_{ano}.zip",
        _csv_br_filter,
        _flat_extract,
    ),
    "propostas": (
        lambda ano: f"{TSE_CDN}/proposta_governo/proposta_governo_{ano}_BR.zip",
        _any_filter,
        _flat_extract,
    ),
    "foto_candidato": (
        lambda ano: f"{TSE_BASE}/eleicoes/eleicoes{ano}/fotos/foto_cand{ano}_BR_div.zip",
        _any_filter,
        _flat_extract,
    ),
    "prestacao_contas": (
        lambda ano: {
            2010: f"{TSE_CDN}/prestacao_contas/prestacao_contas_2010.zip",
            2014: f"{TSE_CDN}/prestacao_contas/prestacao_final_2014.zip",
            2018: f"{TSE_CDN}/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_2018.zip",
            2022: f"{TSE_CDN}/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_2022.zip",
        }[ano],
        _prestacao_filter,
        _prestacao_extract,
    ),
    "certidoes_criminais_candidato": (
        lambda ano: f"{TSE_CDN}/certidao_criminal/certidao_criminal_{ano}_BR.zip",
        _any_filter,
        _flat_extract,
    ),
    "nota_fiscal_candidato": (
        lambda ano: f"{TSE_CDN}/nota_fiscal_candidato/nota_fiscal_candidato_{ano}_BR.zip",
        _csv_br_filter,
        _flat_extract,
    ),
    "rede_social_candidato": (
        lambda ano: f"{TSE_CDN}/consulta_cand/rede_social_candidato_{ano}_BR.zip",
        _csv_br_filter,
        _flat_extract,
    ),
}

DATASETS_POR_ANO: dict[int, list[str]] = {
    2010: [
        "bem_candidato",
        "consulta_candidato",
        "consulta_coligacao",
        "prestacao_contas",
        "propostas",
        "votacao_candidato_munzona",
        "foto_candidato",
    ],
    2014: [
        "bem_candidato",
        "consulta_candidato",
        "consulta_coligacao",
        "prestacao_contas",
        "motivo_cassacao",
        "propostas",
        "votacao_candidato_munzona",
        "foto_candidato",
    ],
    2018: [
        "bem_candidato",
        "consulta_candidato",
        "certidoes_criminais_candidato",
        "consulta_coligacao",
        "prestacao_contas",
        "motivo_cassacao",
        "nota_fiscal_candidato",
        "propostas",
        "votacao_candidato_munzona",
        "foto_candidato",
    ],
    2022: [
        "bem_candidato",
        "consulta_candidato",
        "certidoes_criminais_candidato",
        "consulta_coligacao",
        "prestacao_contas",
        "motivo_cassacao",
        "nota_fiscal_candidato",
        "propostas",
        "rede_social_candidato",
        "votacao_candidato_munzona",
        "foto_candidato",
    ],
}

def create_folders() -> None:
    for ano, datasets in DATASETS_POR_ANO.items():
        for ds in datasets:
            (BASE / str(ano) / ds).mkdir(parents=True, exist_ok=True)

def get_url(dataset: str, ano: int) -> str:
    override = DATASET_OVERRIDES.get(dataset)
    if override:
        return override[0](ano)
    return _default_url(dataset, ano)


def get_member_filter(dataset: str):
    override = DATASET_OVERRIDES.get(dataset)
    if override:
        return override[1]
    return _csv_br_filter


def get_extractor(dataset: str):
    override = DATASET_OVERRIDES.get(dataset)
    if override and len(override) >= 3:
        return override[2]
    return _flat_extract


def download_dataset(dataset: str, ano: int) -> Path:
    destino = BASE / str(ano) / dataset
    destino.mkdir(parents=True, exist_ok=True)

    if any(destino.iterdir()):
        print(f"  [cache] {dataset}/{ano} já existe, pulando.")
        return destino

    url = get_url(dataset, ano)
    print(f"  [download] {url}")

    filtro = get_member_filter(dataset)
    with requests.get(url, stream=True, timeout=300) as response:
        response.raise_for_status()
        total = int(response.headers.get("Content-Length", 0))

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            for chunk in response.iter_content(chunk_size=1024 * 1024 * 4):
                if chunk:
                    tmp.write(chunk)
        if total:
            print(f"  [ok baixado] {dataset}/{ano} ({total / 1_048_576:.1f} MiB)")

    extractor = get_extractor(dataset)
    try:
        with zipfile.ZipFile(tmp_path) as z:
            alvos = [n for n in z.namelist() if filtro(n)]
            if not alvos:
                raise RuntimeError(f"Nenhum arquivo correspondente encontrado em {dataset}/{ano}")
            extractor(z, alvos, destino)
    finally:
        tmp_path.unlink(missing_ok=True)

    print(f"  [ok] {dataset}/{ano} extraído em {destino}")
    return destino

avisos = []
erros = []

def download_todos(max_workers: int = 8) -> None:
    tarefas = [
        (dataset, ano)
        for ano, datasets in DATASETS_POR_ANO.items()
        for dataset in datasets
    ]

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(download_dataset, dataset, ano): (dataset, ano)
            for dataset, ano in tarefas
        }
        for fut in as_completed(futures):
            dataset, ano = futures[fut]
            try:
                fut.result()
            except requests.HTTPError as e:
                avisos.append(f"  [aviso] {dataset}/{ano} não encontrado no TSE: {e}\n")
            except Exception as e:
                erros.append(f"  [erro] {dataset}/{ano}: {e}\n")

    print("\n\n\n")
    print(avisos)
    print(erros)

def limpar_raw() -> None:
    if BASE.exists():
        shutil.rmtree(BASE)
        print(f"[limpeza] {BASE} removido.")


if __name__ == "__main__":
    create_folders()
    download_todos()
