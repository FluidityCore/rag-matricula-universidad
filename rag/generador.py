"""Generación de la respuesta final a partir de los fragmentos recuperados."""

from __future__ import annotations

from dataclasses import dataclass

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, PreTrainedModel, PreTrainedTokenizerBase

from rag.config import MODELO_GENERACION

PLANTILLA_PROMPT = """Responde la pregunta usando únicamente el siguiente contexto \
extraído del reglamento universitario. Si el contexto no contiene la respuesta, \
indica que no se encontró información suficiente.

Contexto:
{contexto}

Pregunta: {pregunta}
Respuesta:"""


@dataclass
class ModeloGeneracion:
    """Agrupa el tokenizador y el modelo seq2seq local usados para generar texto."""

    tokenizador: PreTrainedTokenizerBase
    modelo: PreTrainedModel


def cargar_modelo_generacion() -> ModeloGeneracion:
    """Carga el tokenizador y el modelo local seq2seq (p. ej. flan-t5) de Hugging Face."""
    tokenizador = AutoTokenizer.from_pretrained(MODELO_GENERACION)
    modelo = AutoModelForSeq2SeqLM.from_pretrained(MODELO_GENERACION)
    return ModeloGeneracion(tokenizador=tokenizador, modelo=modelo)


def construir_prompt(pregunta: str, fragmentos: list[dict[str, str]]) -> str:
    """Arma el prompt final combinando la pregunta con los fragmentos recuperados."""
    contexto = "\n---\n".join(fragmento["texto"] for fragmento in fragmentos)
    return PLANTILLA_PROMPT.format(contexto=contexto, pregunta=pregunta)


def generar_respuesta(
    pregunta: str, fragmentos: list[dict[str, str]], generador: ModeloGeneracion
) -> str:
    """Genera la respuesta final invocando el modelo local con el prompt construido."""
    prompt = construir_prompt(pregunta, fragmentos)
    entradas = generador.tokenizador(prompt, return_tensors="pt", truncation=True)
    salida = generador.modelo.generate(**entradas, max_new_tokens=200, min_new_tokens=20)
    return generador.tokenizador.decode(salida[0], skip_special_tokens=True).strip()
