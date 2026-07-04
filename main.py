"""CLI del prototipo RAG: indexa el repositorio o responde preguntas sobre él.

Uso:
    python main.py indexar
    python main.py preguntar "Requisitos para reserva de matricula"
"""

from __future__ import annotations

import sys

from rag.config import INDICE_DIR
from rag.generador import cargar_modelo_generacion, generar_respuesta
from rag.ingesta import construir_indice
from rag.recuperador import cargar_indice, cargar_modelo_embeddings, recuperar_fragmentos


def responder_pregunta(pregunta: str) -> None:
    """Ejecuta el flujo completo de RAG: recuperación + generación, y lo imprime."""
    if not (INDICE_DIR / "documentos.index").exists():
        print("No existe un índice. Ejecuta primero: python main.py indexar")
        return

    modelo_embeddings = cargar_modelo_embeddings()
    indice, metadatos = cargar_indice()
    fragmentos = recuperar_fragmentos(pregunta, modelo_embeddings, indice, metadatos)

    if not fragmentos:
        print("\nNo se encontró información suficiente en el repositorio de documentos.\n")
        return

    print("\nFragmentos recuperados:")
    for fragmento in fragmentos:
        print(f"  [{fragmento['fuente']}] {fragmento['texto'][:120]}...")

    generador = cargar_modelo_generacion()
    respuesta = generar_respuesta(pregunta, fragmentos, generador)
    print(f"\nRespuesta:\n{respuesta}\n")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        return

    comando = sys.argv[1]
    if comando == "indexar":
        construir_indice()
    elif comando == "preguntar" and len(sys.argv) > 2:
        responder_pregunta(sys.argv[2])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
