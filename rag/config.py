"""Configuración central del prototipo RAG."""

from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent
DOCUMENTOS_DIR: Path = BASE_DIR / "repositorio_documentos"
INDICE_DIR: Path = BASE_DIR / "indice"

MODELO_EMBEDDINGS: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODELO_GENERACION: str = "google/flan-t5-base"

TAMANO_CHUNK: int = 600
TOP_K: int = 3
UMBRAL_SIMILITUD: float = 0.3
