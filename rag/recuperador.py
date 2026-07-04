"""Recuperación semántica: busca en el índice FAISS los fragmentos más relevantes."""

from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from rag.config import INDICE_DIR, MODELO_EMBEDDINGS, TOP_K, UMBRAL_SIMILITUD


def cargar_indice(indice_dir: Path = INDICE_DIR) -> tuple[faiss.Index, list[dict[str, str]]]:
    """Carga desde disco el índice FAISS y los metadatos de fragmentos asociados."""
    indice = faiss.read_index(str(indice_dir / "documentos.index"))
    metadatos = json.loads((indice_dir / "metadatos.json").read_text(encoding="utf-8"))
    return indice, metadatos


def recuperar_fragmentos(
    pregunta: str,
    modelo: SentenceTransformer,
    indice: faiss.Index,
    metadatos: list[dict[str, str]],
    top_k: int = TOP_K,
    umbral: float = UMBRAL_SIMILITUD,
) -> list[dict[str, str]]:
    """Embebe la pregunta y devuelve los top_k fragmentos más similares del índice,
    descartando los que queden por debajo del umbral de similitud coseno."""
    embedding_pregunta = modelo.encode(
        [pregunta], convert_to_numpy=True, normalize_embeddings=True
    )
    similitudes, posiciones = indice.search(embedding_pregunta.astype(np.float32), top_k)
    return [
        metadatos[i]
        for i, similitud in zip(posiciones[0], similitudes[0])
        if i != -1 and similitud >= umbral
    ]


def cargar_modelo_embeddings() -> SentenceTransformer:
    """Carga el modelo de embeddings usado tanto en ingesta como en consulta."""
    return SentenceTransformer(MODELO_EMBEDDINGS)
