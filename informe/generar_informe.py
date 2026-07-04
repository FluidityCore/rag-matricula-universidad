"""Genera el informe académico en PDF sobre el prototipo RAG.

Uso:
    python generar_informe.py
"""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

SALIDA: Path = Path(__file__).resolve().parent / "Informe_RAG_Matricula.pdf"
REPO_URL = "https://github.com/FluidityCore/rag-matricula-universidad"


def construir_estilos() -> dict[str, ParagraphStyle]:
    """Define los estilos de párrafo, título y código usados en el informe."""
    base = getSampleStyleSheet()
    estilos = {
        "titulo": base["Title"],
        "h1": ParagraphStyle("h1", parent=base["Heading1"], spaceBefore=14, spaceAfter=8),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], spaceBefore=10, spaceAfter=6),
        "cuerpo": ParagraphStyle("cuerpo", parent=base["BodyText"], spaceAfter=8, leading=15),
        "cita": ParagraphStyle(
            "cita", parent=base["BodyText"], leftIndent=14, textColor=colors.HexColor("#333333"),
            spaceAfter=10, leading=14,
        ),
        "codigo": ParagraphStyle(
            "codigo", fontName="Courier", fontSize=7.5, leading=9.5,
            backColor=colors.HexColor("#f2f2f2"), spaceAfter=10,
        ),
        "portada_sub": ParagraphStyle("portada_sub", parent=base["Normal"], fontSize=13, spaceAfter=10, alignment=1),
    }
    return estilos


def bloque_codigo(texto: str, estilo: ParagraphStyle, ancho: int = 92) -> Paragraph:
    """Convierte un fragmento de código en un Paragraph monoespaciado con saltos de línea."""
    lineas = []
    for linea in texto.strip("\n").split("\n"):
        lineas.extend(wrap(linea, ancho) or [""])
    html = "<br/>".join(l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") for l in lineas)
    return Paragraph(html, estilo)


def portada(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph("UNIVERSIDAD", e["portada_sub"]))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "Propuesta de Sistema de Búsqueda de Información en Documentos "
        "Universitarios usando la Técnica de IA RAG (Retrieval-Augmented Generation)",
        e["titulo"],
    ))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("Trabajo individual — Investigación aplicada", e["portada_sub"]))
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("Autor: [Completar: nombre del estudiante]", e["cuerpo"]))
    story.append(Paragraph("Curso / Docente: [Completar]", e["cuerpo"]))
    story.append(Paragraph("Fecha: 03 de julio de 2026", e["cuerpo"]))
    story.append(Paragraph(f"Repositorio con la solución: {REPO_URL}", e["cuerpo"]))
    story.append(PageBreak())


def introduccion(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph("1. Introducción", e["h1"]))
    story.append(Paragraph(
        "La universidad requiere un programa que permita a los estudiantes buscar "
        "información dentro de un repositorio de documentos institucionales "
        "(reglamentos, requisitos, calendarios) formulando preguntas en lenguaje "
        "natural, por ejemplo: <i>“Requisitos para reserva de matrícula”</i>. "
        "Como propuesta de solución y línea base para un futuro producto de "
        "software institucional, se investigó y desarrolló un prototipo funcional "
        "basado en la técnica de inteligencia artificial conocida como "
        "<b>RAG (Retrieval-Augmented Generation)</b>.", e["cuerpo"],
    ))
    story.append(Paragraph(
        "Este informe documenta el marco teórico de RAG, la metodología y "
        "arquitectura del prototipo, los paquetes de software utilizados, los "
        "prompts empleados como apoyo de IA durante el desarrollo, los casos de "
        "prueba resueltos y las conclusiones, junto con el enlace al repositorio "
        "que contiene la solución completa en Python.", e["cuerpo"],
    ))


def marco_teorico(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph("2. Marco teórico: ¿qué es RAG?", e["h1"]))
    story.append(Paragraph(
        "RAG (Retrieval-Augmented Generation, «generación aumentada por "
        "recuperación») es una técnica de IA que combina un sistema de "
        "recuperación de información con un modelo de lenguaje generativo (LLM), "
        "en lugar de depender únicamente del conocimiento memorizado por el "
        "modelo durante su entrenamiento. Consta de dos etapas:", e["cuerpo"],
    ))
    story.append(Paragraph(
        "<b>Retrieval (recuperación):</b> el repositorio de documentos se divide "
        "en fragmentos (<i>chunks</i>), y cada fragmento se convierte en un vector "
        "numérico (<i>embedding</i>) que representa su significado. Estos vectores "
        "se almacenan en una base de datos vectorial. Ante una pregunta del "
        "usuario, esta también se convierte en un embedding y se buscan los "
        "fragmentos más parecidos por similitud semántica (no por coincidencia "
        "exacta de palabras).", e["cita"],
    ))
    story.append(Paragraph(
        "<b>Generation (generación):</b> los fragmentos recuperados se entregan "
        "como contexto a un modelo de lenguaje, que redacta la respuesta final "
        "basándose en esa información. Esto reduce las «alucinaciones» (respuestas "
        "inventadas) y permite trazar la respuesta hasta su fuente documental.", e["cita"],
    ))
    story.append(Paragraph(
        "RAG es especialmente adecuado para el caso de la universidad porque el "
        "reglamento y los procedimientos cambian con cada periodo académico: en "
        "lugar de re-entrenar un modelo, basta con actualizar los documentos del "
        "repositorio y reconstruir el índice vectorial.", e["cuerpo"],
    ))


def metodologia(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph("3. Metodología y arquitectura del prototipo", e["h1"]))
    story.append(Paragraph(
        "Se optó por una implementación 100% local y gratuita (sin API de pago), "
        "adecuada para un prototipo académico reproducible. El flujo implementado es:",
        e["cuerpo"],
    ))
    pasos = [
        "1. <b>Ingesta:</b> se leen los documentos .txt del repositorio "
        "(<font face='Courier'>repositorio_documentos/</font>).",
        "2. <b>Chunking:</b> cada documento se agrupa por párrafos en fragmentos "
        "de hasta 600 caracteres, evitando cortar oraciones a la mitad.",
        "3. <b>Embeddings:</b> cada fragmento se convierte en un vector con el "
        "modelo <font face='Courier'>paraphrase-multilingual-MiniLM-L12-v2</font>.",
        "4. <b>Indexado:</b> los vectores se almacenan en un índice FAISS "
        "(<font face='Courier'>IndexFlatIP</font>) para búsqueda por similitud coseno.",
        "5. <b>Recuperación:</b> ante una pregunta, se embebe y se buscan los 3 "
        "fragmentos más similares que superen un umbral mínimo de similitud.",
        "6. <b>Generación:</b> los fragmentos recuperados se insertan en una "
        "plantilla de prompt y se envían al modelo local "
        "<font face='Courier'>google/flan-t5-base</font>, que redacta la respuesta final.",
    ]
    for paso in pasos:
        story.append(Paragraph(paso, e["cita"]))
    story.append(Paragraph(
        "Estructura de archivos del proyecto: <font face='Courier'>repositorio_documentos/</font> "
        "(fuentes), <font face='Courier'>rag/ingesta.py</font>, "
        "<font face='Courier'>rag/recuperador.py</font>, "
        "<font face='Courier'>rag/generador.py</font>, "
        "<font face='Courier'>rag/config.py</font> y "
        "<font face='Courier'>main.py</font> como interfaz de línea de comandos.",
        e["cuerpo"],
    ))


def paquetes(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph("4. Paquetes y tecnologías utilizadas", e["h1"]))
    story.append(Paragraph(
        "Todos los paquetes son de código abierto y gratuitos. Las versiones "
        "exactas quedan fijadas en <font face='Courier'>requirements.txt</font> "
        "del repositorio.", e["cuerpo"],
    ))
    datos = [
        ["Paquete", "Version", "Uso en el proyecto"],
        ["sentence-transformers", "5.6.0", "Generacion de embeddings semanticos multilingues"],
        ["faiss-cpu", "1.14.3", "Base de datos vectorial (busqueda por similitud)"],
        ["transformers", "5.13.0", "Carga del modelo local de generacion de texto (LLM)"],
        ["torch", "2.12.1", "Motor de computo para los modelos anteriores"],
        ["numpy", "2.5.0", "Manejo de vectores y matrices de embeddings"],
    ]
    tabla = Table(datos, colWidths=[4.2 * cm, 2.3 * cm, 8.5 * cm])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f3e57")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
    ]))
    story.append(tabla)
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        "Modelos de Hugging Face empleados (descarga automatica, sin costo): "
        "embeddings <font face='Courier'>sentence-transformers/paraphrase-multilingual-"
        "MiniLM-L12-v2</font> y generacion <font face='Courier'>google/flan-t5-base</font>.",
        e["cuerpo"],
    ))


def prompts_usados(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph("5. Prompts usados como apoyo de IA", e["h1"]))
    story.append(Paragraph(
        "El prototipo se diseño con el apoyo del asistente de IA Claude Code "
        "(Anthropic). A continuacion se listan los prompts principales usados "
        "durante el desarrollo (el detalle completo esta tambien en "
        "<font face='Courier'>PROMPTS.md</font> del repositorio).", e["cuerpo"],
    ))
    prompts = [
        ("Prompt 1 - Enunciado del trabajo", "Enunciado original entregado por la "
         "universidad sobre el sistema de busqueda de informacion y la propuesta de RAG."),
        ("Prompt 2 - Alcance tecnico", "“Ayudame a construir un prototipo en Python que "
         "implemente RAG para responder preguntas sobre un repositorio de documentos "
         "universitarios... 100% local y gratuito... con chunking, embeddings, indice "
         "vectorial, recuperacion y generacion... buenas practicas: type hints, "
         "pathlib.Path, funciones cortas de una sola responsabilidad.”"),
        ("Prompt 3 - Seleccion de librerias", "“¿Que combinacion de librerias Python "
         "recomiendas para implementar RAG de forma local y gratuita, sin depender de "
         "OpenAI ni Anthropic para los embeddings?”"),
        ("Prompt 4 - Estructura del codigo", "“Genera el codigo dividido en modulos: "
         "ingesta.py, recuperador.py, generador.py y main.py como CLI.”"),
        ("Prompt 5 - Documentos de ejemplo", "“No tengo acceso a los reglamentos reales "
         "de mi universidad. Genera 2 o 3 documentos de ejemplo realistas sobre reserva "
         "de matricula, requisitos y calendario academico.”"),
        ("Prompt 6 - Validacion", "“Ejecuta el flujo completo (indexar y preguntar) y "
         "muestrame los fragmentos recuperados y la respuesta generada.”"),
        ("Prompt 6b - Correccion de caso limite", "“Al preguntar algo fuera del "
         "repositorio, el sistema inventa una respuesta. Corrige el retriever para que "
         "aplique un umbral de similitud y, si nada lo supera, informe que no hay "
         "informacion suficiente.”"),
        ("Prompt 7 - Redaccion del informe", "“Con base en el codigo y los resultados, "
         "redacta el informe en PDF con introduccion, marco teorico, metodologia, "
         "paquetes, prompts, codigo, pruebas, conclusiones y el enlace al repositorio.”"),
    ]
    for titulo, texto in prompts:
        story.append(Paragraph(f"<b>{titulo}</b>", e["cuerpo"]))
        story.append(Paragraph(texto, e["cita"]))


CODIGO_RECUPERADOR = '''def recuperar_fragmentos(
    pregunta: str,
    modelo: SentenceTransformer,
    indice: faiss.Index,
    metadatos: list[dict[str, str]],
    top_k: int = TOP_K,
    umbral: float = UMBRAL_SIMILITUD,
) -> list[dict[str, str]]:
    """Embebe la pregunta y devuelve los top_k fragmentos mas similares
    del indice, descartando los que queden por debajo del umbral."""
    embedding_pregunta = modelo.encode(
        [pregunta], convert_to_numpy=True, normalize_embeddings=True
    )
    similitudes, posiciones = indice.search(
        embedding_pregunta.astype(np.float32), top_k
    )
    return [
        metadatos[i]
        for i, similitud in zip(posiciones[0], similitudes[0])
        if i != -1 and similitud >= umbral
    ]'''

CODIGO_GENERADOR = '''def generar_respuesta(
    pregunta: str, fragmentos: list[dict[str, str]], generador: ModeloGeneracion
) -> str:
    """Genera la respuesta final invocando el modelo local con el
    prompt construido a partir de los fragmentos recuperados."""
    prompt = construir_prompt(pregunta, fragmentos)
    entradas = generador.tokenizador(prompt, return_tensors="pt", truncation=True)
    salida = generador.modelo.generate(
        **entradas, max_new_tokens=200, min_new_tokens=20
    )
    return generador.tokenizador.decode(salida[0], skip_special_tokens=True).strip()'''


def implementacion(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph("6. Implementacion (evidencia en archivos .py)", e["h1"]))
    story.append(Paragraph(
        "El codigo completo esta anexado en el repositorio de GitHub "
        "(seccion 10) en los archivos <font face='Courier'>rag/ingesta.py</font>, "
        "<font face='Courier'>rag/recuperador.py</font>, "
        "<font face='Courier'>rag/generador.py</font>, "
        "<font face='Courier'>rag/config.py</font> y "
        "<font face='Courier'>main.py</font>. A continuacion se muestran los dos "
        "fragmentos mas representativos de la tecnica RAG: la recuperacion "
        "semantica con umbral de similitud, y la generacion de la respuesta final.",
        e["cuerpo"],
    ))
    story.append(Paragraph("rag/recuperador.py (recuperacion semantica)", e["h2"]))
    story.append(bloque_codigo(CODIGO_RECUPERADOR, e["codigo"]))
    story.append(Paragraph("rag/generador.py (generacion de la respuesta)", e["h2"]))
    story.append(bloque_codigo(CODIGO_GENERADOR, e["codigo"]))


CASO_1_SALIDA = '''$ python main.py preguntar "Requisitos para reserva de matricula"

Fragmentos recuperados:
  [reglamento_matricula.txt] Articulo 11.- Requisitos para reserva de
  matricula: a) Ser estudiante regular con matricula vigente o haber
  estado matri...
  [requisitos_reserva_procedimiento.txt] Paso 4: Adjuntar los documentos
  requeridos segun el motivo de la reserva: - Motivo laboral: carta de
  la empresa o con...
  [reglamento_matricula.txt] Articulo 12.- La solicitud de reserva de
  matricula sera evaluada por la Oficina de Registros Academicos en un
  plazo maxi...

Respuesta generada por el modelo (se conservan sus imperfecciones de
ortografia y gramatica, ver seccion 8 - Limitaciones):
Paso 4: Adjuntar documentos requeridos por reserva: a) ser estudiante
regular con reserva vigente o adquirir estado matriculado en el ao
anterior. b) Presentar la solicitud de reserva a traves del portal
virtual de tramites, dentro de los plazos establecidos en el calendario
academico. c) No registrar deudas en concepto de pensiones o derechos
academicos al momento de la solicitud. d) Adjuntar el pago de la tasa
administrativa por derecho de reserva.'''

CASO_3_SALIDA = '''$ python main.py preguntar "Cual es el clima en Lima manana"

No se encontro informacion suficiente en el repositorio de documentos.'''


def pruebas(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph("7. Casos de prueba y resultados", e["h1"]))
    story.append(Paragraph(
        "<b>Caso 1 - Pregunta directa del enunciado.</b> El retriever recupera "
        "exactamente el articulo del reglamento con los requisitos y el paso a "
        "paso del procedimiento; el modelo genera una respuesta que resume los "
        "requisitos citando ambas fuentes.", e["cuerpo"],
    ))
    story.append(bloque_codigo(CASO_1_SALIDA, e["codigo"]))
    story.append(Paragraph(
        "<b>Caso 2 - Pregunta sobre plazos.</b> La pregunta “Hasta cuando "
        "puedo solicitar reserva de matricula” recupera el articulo sobre el "
        "plazo de resolucion (5 dias habiles) y el calendario academico con las "
        "fechas exactas de matricula e inicio de clases.", e["cuerpo"],
    ))
    story.append(Paragraph(
        "<b>Caso 3 - Pregunta fuera del repositorio.</b> Ante una pregunta sin "
        "relacion con los documentos (por ejemplo, sobre el clima), ningun "
        "fragmento supera el umbral de similitud configurado "
        "(<font face='Courier'>UMBRAL_SIMILITUD = 0.3</font>), por lo que el "
        "sistema informa que no encontro informacion suficiente en lugar de "
        "inventar una respuesta. Esta es una de las principales ventajas de RAG "
        "frente a un LLM sin contexto: reduce las alucinaciones.", e["cuerpo"],
    ))
    story.append(bloque_codigo(CASO_3_SALIDA, e["codigo"]))


def limitaciones(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph("8. Limitaciones y trabajo futuro", e["h1"]))
    items = [
        "El modelo local de generacion (<font face='Courier'>flan-t5-base</font>) "
        "tiene soporte multilingue limitado: produce respuestas comprensibles pero "
        "con errores menores de ortografia y gramatica en espanol. En un producto "
        "real se recomienda un modelo mas grande o una API de un LLM con mejor "
        "soporte de espanol.",
        "El repositorio de prueba usa documentos de ejemplo (no los reglamentos "
        "reales de la universidad); el siguiente paso es ingestar los PDF/Word "
        "oficiales.",
        "El umbral de similitud (0.3) se calibro de forma empirica; en produccion "
        "debe ajustarse con un conjunto real de preguntas de los estudiantes.",
        "Como producto futuro se propone exponer el prototipo como una API web, "
        "agregar autenticacion de usuarios, un panel para que la oficina de "
        "registros actualice el repositorio, y metricas de las preguntas mas "
        "frecuentes.",
    ]
    for item in items:
        story.append(Paragraph(f"- {item}", e["cita"]))


def conclusiones(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph("9. Conclusiones", e["h1"]))
    story.append(Paragraph(
        "Se disenio, implemento y probo un prototipo funcional de busqueda de "
        "informacion sobre documentos universitarios usando la tecnica RAG, "
        "cumpliendo el requerimiento de responder preguntas en lenguaje natural "
        "como “Requisitos para reserva de matricula” con informacion "
        "extraida directamente del repositorio de documentos.", e["cuerpo"],
    ))
    story.append(Paragraph(
        "La combinacion de recuperacion semantica (embeddings + FAISS) con un "
        "umbral de similitud y un modelo generativo local demuestra, con un stack "
        "100% gratuito, los principios centrales de RAG: respuestas basadas en "
        "evidencia documental y mitigacion de alucinaciones ante preguntas fuera "
        "de alcance. Este prototipo constituye la base tecnica y conceptual para "
        "el desarrollo de un futuro producto de software institucional de "
        "atencion a consultas academicas.", e["cuerpo"],
    ))


def referencias_y_enlace(story: list, e: dict[str, ParagraphStyle]) -> None:
    story.append(Paragraph("10. Referencias y enlace de la solucion", e["h1"]))
    referencias = [
        "Lewis, P. et al. (2020). Retrieval-Augmented Generation for "
        "Knowledge-Intensive NLP Tasks. NeurIPS.",
        "Documentacion de sentence-transformers: https://www.sbert.net",
        "Documentacion de FAISS: https://faiss.ai",
        "Documentacion de Hugging Face Transformers: "
        "https://huggingface.co/docs/transformers",
        "Modelo flan-t5-base: https://huggingface.co/google/flan-t5-base",
    ]
    for ref in referencias:
        story.append(Paragraph(f"- {ref}", e["cita"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        f"<b>Repositorio con la solucion completa (codigo .py, documentos de "
        f"ejemplo, README y PROMPTS.md):</b><br/>{REPO_URL}", e["cuerpo"],
    ))


def main() -> None:
    doc = SimpleDocTemplate(
        str(SALIDA), pagesize=LETTER,
        topMargin=2.2 * cm, bottomMargin=2.2 * cm, leftMargin=2.2 * cm, rightMargin=2.2 * cm,
    )
    estilos = construir_estilos()
    story: list = []

    portada(story, estilos)
    introduccion(story, estilos)
    marco_teorico(story, estilos)
    metodologia(story, estilos)
    paquetes(story, estilos)
    prompts_usados(story, estilos)
    story.append(PageBreak())
    implementacion(story, estilos)
    pruebas(story, estilos)
    limitaciones(story, estilos)
    conclusiones(story, estilos)
    referencias_y_enlace(story, estilos)

    doc.build(story)
    print(f"Informe generado en: {SALIDA}")


if __name__ == "__main__":
    main()
