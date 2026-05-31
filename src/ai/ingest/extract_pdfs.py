"""Extrai texto dos PDFs em PROPOSTA_GOVERNO, gera chunks + embeddings
e popula PROPOSTA_CHUNK. Atualiza PROPOSTA_GOVERNO com o texto extraído
e marca st_processado=TRUE.

Idempotente: pode rodar várias vezes — limpa chunks antigos do candidato
antes de inserir os novos.
"""
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

# permite rodar tanto como script (python src/ai/ingest/extract_pdfs.py)
# quanto como módulo (python -m ingest.extract_pdfs com PYTHONPATH=src/ai)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fitz  # PyMuPDF
import numpy as np

import config
from db import get_connection
from embeddings import embed_batch

CHUNK_SIZE = 2000      # ~500 tokens
CHUNK_OVERLAP = 200    # ~50 tokens

# A extração de PDF emite um espaço espúrio logo após os glifos de ligadura
# (ﬀ ﬁ ﬂ ﬃ ﬄ ﬅ ﬆ — U+FB00..U+FB06), partindo a palavra: "deﬁ nidos".
# Removemos o espaço antes do NFKC, que depois converte a ligadura em letras.
_LIGADURA_ESPACO = re.compile(r"([ﬀ-ﬆ])[ \t]+(?=[a-zà-ÿ])")


def clean_text(s: str) -> str:
    """Normaliza unicode, remove caracteres de controle, colapsa espaços."""
    s = _LIGADURA_ESPACO.sub(r"\1", s)
    s = unicodedata.normalize("NFKC", s)
    s = "".join(
        ch for ch in s
        if ch in "\n\t" or not unicodedata.category(ch).startswith("C")
    )
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def extract_text(pdf_path: Path) -> str:
    parts = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            parts.append(page.get_text("text"))
    return clean_text("\n".join(parts))


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Divide o texto em janelas com overlap, preferindo quebra em \\n ou '. '."""
    if not text:
        return []
    if len(text) <= size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            cut = text.rfind("\n", start + size // 2, end)
            if cut == -1:
                cut = text.rfind(". ", start + size // 2, end)
            if cut != -1 and cut > start:
                end = cut + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def ano_from_nome(nm_arquivo: str) -> int:
    m = re.match(r"^(\d{4})", nm_arquivo)
    return int(m.group(1)) if m else 0


def main() -> int:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT sq_candidato, nm_arquivo, ds_caminho_arquivo
        FROM proposta_governo
        ORDER BY sq_candidato
    """)
    rows = cur.fetchall()
    print(f"Propostas a processar: {len(rows)}")

    if not rows:
        print("Nenhuma proposta encontrada em proposta_governo. Rode o ETL primeiro.")
        return 0

    print(f"Carregando modelo de embeddings: {config.EMBED_MODEL}...")
    t0 = time.time()
    # warm-up para baixar/carregar o modelo já agora
    embed_batch(["warmup"])
    print(f"  pronto em {time.time() - t0:.1f}s")

    total_chunks = 0
    processadas = 0
    falhas: list[str] = []

    for sq, nm_arquivo, caminho_rel in rows:
        ano = ano_from_nome(nm_arquivo)
        pdf_path = config.STORAGE_DIR / caminho_rel

        if not pdf_path.exists():
            print(f"  [skip] {nm_arquivo}: arquivo não encontrado em {pdf_path}")
            falhas.append(nm_arquivo)
            continue

        try:
            texto = extract_text(pdf_path)
        except Exception as e:
            print(f"  [erro] {nm_arquivo}: extração falhou ({e})")
            falhas.append(nm_arquivo)
            continue

        chunks = chunk_text(texto)
        if not chunks:
            print(f"  [skip] {nm_arquivo}: PDF sem texto extraível (imagem/scan?)")
            falhas.append(nm_arquivo)
            continue

        embeddings = embed_batch(chunks)

        cur.execute("DELETE FROM proposta_chunk WHERE sq_candidato = %s", (sq,))
        for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            cur.execute(
                """
                INSERT INTO proposta_chunk
                    (sq_candidato, ano_eleicao, idx, texto, embedding)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (sq, ano, idx, chunk, np.asarray(emb, dtype=np.float32)),
            )

        cur.execute(
            """
            UPDATE proposta_governo
            SET tx_conteudo_extraido = %s,
                st_processado = TRUE,
                dt_processamento = %s
            WHERE sq_candidato = %s
            """,
            (texto, datetime.now(timezone.utc), sq),
        )
        conn.commit()

        total_chunks += len(chunks)
        processadas += 1
        print(f"  [ok]   {nm_arquivo} (ano={ano}, sq={sq}): {len(chunks)} chunks")

    cur.close()
    conn.close()

    print()
    print(f"Concluído: {processadas} propostas, {total_chunks} chunks indexados")
    if falhas:
        print(f"Falhas/skips: {len(falhas)} → {falhas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
