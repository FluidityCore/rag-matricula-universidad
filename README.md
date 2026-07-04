# Prototipo RAG — Búsqueda de información en documentos universitarios

Prototipo académico que implementa la técnica de IA **RAG
(Retrieval-Augmented Generation)** para responder preguntas en lenguaje
natural sobre un repositorio de documentos universitarios (reglamentos,
requisitos de matrícula, calendario académico), como propuesta de
desarrollo de un futuro producto de software para la universidad.

## ¿Qué es RAG?

RAG combina dos etapas:
1. **Retrieval (recuperación):** ante una pregunta, se buscan en una base
   de datos vectorial los fragmentos de documentos semánticamente más
   parecidos a la pregunta (no por coincidencia exacta de palabras, sino
   por significado).
2. **Generation (generación):** esos fragmentos recuperados se entregan
   como contexto a un modelo de lenguaje, que redacta la respuesta final
   basándose únicamente en esa información, reduciendo alucinaciones y
   permitiendo citar la fuente.

## Estructura del proyecto

```
rag-matricula/
├── repositorio_documentos/   # Documentos de ejemplo (reglamento, requisitos, calendario)
├── rag/
│   ├── config.py             # Rutas y parámetros (modelo, tamaño de chunk, top_k)
│   ├── ingesta.py            # Lectura, chunking, embeddings e indexado (FAISS)
│   ├── recuperador.py        # Búsqueda semántica de fragmentos relevantes
│   └── generador.py          # Generación de la respuesta final (LLM local)
├── main.py                   # CLI: indexar / preguntar
├── requirements.txt
├── PROMPTS.md                # Prompts usados como apoyo de IA para este trabajo
└── informe/                  # Informe final en PDF
```

## Paquetes utilizados

| Paquete                | Versión  | Uso en el proyecto                                   |
|-------------------------|----------|-------------------------------------------------------|
| `sentence-transformers` | 5.6.0    | Genera embeddings semánticos multilingües de los textos |
| `faiss-cpu`              | 1.14.3   | Base de datos vectorial para búsqueda por similitud    |
| `transformers`           | 5.13.0   | Carga el modelo local de generación de texto (LLM)     |
| `torch`                  | 2.12.1   | Motor de cómputo usado por `transformers`/`sentence-transformers` |
| `numpy`                  | 2.5.0    | Manejo de vectores/matrices de embeddings             |

Modelos usados (descargados automáticamente de Hugging Face, sin costo):
- Embeddings: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- Generación: `google/flan-t5-base`

## Instalación

```bash
python -m venv .venv
.venv/Scripts/activate        # En Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
# 1. Construir el índice vectorial a partir del repositorio de documentos
python main.py indexar

# 2. Realizar una pregunta
python main.py preguntar "Requisitos para reserva de matricula"
```

## Casos resueltos / probados

1. **Pregunta directa sobre requisitos** — `"Requisitos para reserva de
   matricula"`: el retriever recupera exactamente el Artículo 11 del
   reglamento (los seis requisitos a-f) y el paso a paso del procedimiento.
   El modelo genera una respuesta que resume los requisitos citando ambas
   fuentes.
2. **Pregunta sobre plazos** — `"Hasta cuando puedo solicitar reserva de
   matricula"`: recupera el artículo sobre plazo de resolución y el
   calendario académico con las fechas exactas de inicio de clases y pago
   de tasas.
3. **Pregunta fuera del repositorio** — `"Cual es el clima en Lima
   manana"`: ningún fragmento supera el umbral de similitud coseno
   (`UMBRAL_SIMILITUD = 0.3` en `rag/config.py`), por lo que el sistema
   responde *"No se encontró información suficiente en el repositorio de
   documentos"* en lugar de inventar una respuesta (mitigación de
   alucinaciones, uno de los principales beneficios de RAG frente a un LLM
   sin contexto).

## Limitaciones observadas (para la sección de trabajo futuro)

- El modelo de generación local `flan-t5-base` es multilingüe limitado:
  produce respuestas comprensibles pero con errores menores de ortografía
  y gramática en español. En un producto real se recomienda un modelo más
  grande o una API de un LLM con mejor soporte de español.
- El umbral de similitud (0.3) se calibró de forma empírica con los
  documentos de prueba; en producción debe ajustarse con un conjunto de
  preguntas real de los estudiantes.

## Alcance y trabajo futuro

Este prototipo es la base conceptual y técnica de un futuro producto de
software institucional. Como trabajo futuro se propone: ingestar PDFs y
Word reales de la universidad, exponer el prototipo como API web,
agregar control de acceso por usuario y ampliar el modelo de generación
a uno de mayor calidad.

## Autor

Trabajo individual — repositorio con la solución completa:
`<ENLACE_GITHUB>` (se completa tras publicar el repositorio).
