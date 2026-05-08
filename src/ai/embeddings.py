from sentence_transformers import SentenceTransformer

import config

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(config.EMBED_MODEL)
    return _model


def embed(text: str):
    return get_model().encode(text, normalize_embeddings=True)


def embed_batch(texts: list[str], show_progress: bool = False):
    return get_model().encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=show_progress,
        batch_size=32,
    )
