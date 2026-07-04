# Prompts usados como apoyo para generar el prototipo RAG

Este documento registra los prompts (instrucciones) que se usaron con el
asistente de IA (Claude, de Anthropic, vía Claude Code) para diseñar,
generar y depurar el prototipo de búsqueda de información con RAG.

## Prompt 1 — Enunciado original del trabajo (punto de partida)

> UNIVERSIDAD requiere un programa que permita realizar búsqueda de
> información en documentos que se encuentran en un repositorio, el usuario
> debe ingresar una pregunta como por ejemplo: Requisitos para reserva de
> matricula, y debe mostrar información sobre el tema. Como propuesta usar
> técnica de IA denominada RAG, esto debe estar incluido en su informe como
> parte de desarrollo de futuro producto software.

## Prompt 2 — Definición del alcance técnico

> Ayúdame a construir un prototipo en Python que implemente la técnica RAG
> (Retrieval-Augmented Generation) para responder preguntas sobre un
> repositorio de documentos universitarios (reglamentos, requisitos de
> matrícula, calendario académico). El prototipo debe:
> - Usar un enfoque 100% local y gratuito (sin API de pago).
> - Dividir los documentos en fragmentos (chunking) con solapamiento.
> - Generar embeddings semánticos de cada fragmento.
> - Indexarlos en una base vectorial para búsqueda por similitud.
> - Recuperar los fragmentos más relevantes ante una pregunta del usuario.
> - Generar una respuesta final en lenguaje natural a partir de esos
>   fragmentos, usando un modelo de lenguaje local.
> - Cumplir buenas prácticas: type hints, pathlib.Path, funciones cortas de
>   una sola responsabilidad, sin abstracciones innecesarias.

## Prompt 3 — Selección de librerías

> ¿Qué combinación de librerías Python recomiendas para implementar RAG de
> forma local y gratuita, sin depender de OpenAI ni Anthropic para la parte
> de embeddings? Necesito algo liviano, reproducible y bien documentado
> para un trabajo académico.

Resultado de este prompt: se optó por `sentence-transformers` (modelo
`paraphrase-multilingual-MiniLM-L12-v2`, con soporte de español) para los
embeddings, `faiss-cpu` como base de datos vectorial, y `transformers` con
el modelo `google/flan-t5-base` como generador local de la respuesta final.

## Prompt 4 — Estructura del código

> Genera el código dividido en módulos: uno para la ingesta y construcción
> del índice (`ingesta.py`), uno para la recuperación semántica
> (`recuperador.py`), uno para la generación de la respuesta
> (`generador.py`), y un `main.py` como CLI que permita indexar el
> repositorio o hacer una pregunta desde la terminal.

## Prompt 5 — Documentos de ejemplo

> No tengo acceso a los reglamentos reales de mi universidad. Genera 2 o 3
> documentos de ejemplo, realistas, sobre "reserva de matrícula",
> "requisitos de matrícula" y "calendario académico", para usarlos como
> repositorio de prueba del sistema RAG.

## Prompt 6 — Validación y pruebas

> Ejecuta el flujo completo (indexar y luego preguntar
> "Requisitos para reserva de matricula") y muéstrame los fragmentos
> recuperados y la respuesta generada, para comprobar que el prototipo
> funciona correctamente antes de documentarlo en el informe.

## Prompt 6b — Corrección de un caso límite detectado en las pruebas

> Al probar con una pregunta fuera del repositorio (por ejemplo, sobre el
> clima), el sistema igual recupera fragmentos irrelevantes y el modelo
> inventa una respuesta. Corrige el retriever para que aplique un umbral
> de similitud coseno y, si ningún fragmento lo supera, el programa
> informe que no encontró información suficiente en lugar de generar una
> respuesta con el LLM.

Resultado: se agregó `UMBRAL_SIMILITUD` en `rag/config.py` y el filtrado
correspondiente en `recuperar_fragmentos` (`rag/recuperador.py`), evitando
alucinaciones ante preguntas fuera de alcance.

## Prompt 7 — Redacción del informe

> Con base en el código y los resultados obtenidos, redacta el informe en
> PDF que incluya: introducción, marco teórico de la técnica RAG,
> metodología, paquetes utilizados, los prompts de este documento, capturas
> del funcionamiento, casos resueltos, conclusiones y el enlace al
> repositorio de GitHub con la solución completa.

---

**Nota:** todos los prompts anteriores fueron usados como apoyo de diseño
y generación de código; el prototipo resultante, las pruebas y la
documentación fueron revisados y validados por el autor antes de la
entrega, en cumplimiento de la condición de trabajo individual.
