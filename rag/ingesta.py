"""Ingesta del repositorio: lee documentos, los fragmenta y construye el índice vectorial."""

from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from rag.config import DOCUMENTOS_DIR, INDICE_DIR, MODELO_EMBEDDINGS, TAMANO_CHUNK


def leer_documentos(directorio: Path) -> list[tuple[str, str]]:
    """Lee todos los .txt de un directorio y devuelve pares (nombre_archivo, contenido)."""
    documentos = []
    for archivo in sorted(directorio.glob("*.txt")):
        contenido = archivo.read_text(encoding="utf-8")
        documentos.append((archivo.name, contenido))
    return documentos


def dividir_en_chunks(texto: str, tamano: int = TAMANO_CHUNK) -> list[str]:
    """Agrupa párrafos consecutivos en fragmentos de hasta `tamano` caracteres,
    evitando cortar oraciones a la mitad."""
    parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    chunks = []
    actual = ""
    for parrafo in parrafos:
        candidato = f"{actual}\n\n{parrafo}".strip() if actual else parrafo
        if len(candidato) > tamano and actual:
            chunks.append(actual)
            actual = parrafo
        else:
            actual = candidato
    if actual:
        chunks.append(actual)
    return chunks


def preparar_fragmentos(documentos: list[tuple[str, str]]) -> list[dict[str, str]]:
    """Convierte cada documento en fragmentos con metadatos de origen."""
    metadatos = []
    for nombre_archivo, contenido in documentos:
        for chunk in dividir_en_chunks(contenido):
            metadatos.append({"fuente": nombre_archivo, "texto": chunk})
    return metadatos


def construir_indice(
    documentos_dir: Path = DOCUMENTOS_DIR, indice_dir: Path = INDICE_DIR
) -> None:
    """Genera embeddings de todos los fragmentos y persiste el índice FAISS en disco."""
    modelo = SentenceTransformer(MODELO_EMBEDDINGS)
    documentos = leer_documentos(documentos_dir)
    metadatos = preparar_fragmentos(documentos)

    textos = [item["texto"] for item in metadatos]
    embeddings = modelo.encode(textos, convert_to_numpy=True, normalize_embeddings=True)

    indice = faiss.IndexFlatIP(embeddings.shape[1])
    indice.add(embeddings.astype(np.float32))

    indice_dir.mkdir(parents=True, exist_ok=True)
    faiss.write_index(indice, str(indice_dir / "documentos.index"))
    (indice_dir / "metadatos.json").write_text(
        json.dumps(metadatos, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Índice construido: {len(textos)} fragmentos de {len(documentos)} documentos.")


if __name__ == "__main__":
    construir_indice()
