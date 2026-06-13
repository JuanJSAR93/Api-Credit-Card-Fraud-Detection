# ─────────────────────────────────────────────────────────────────────
# llm.py
# ─────────────────────────────────────────────────────────────────────

import os
import json

from langchain_groq import ChatGroq

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

# ─────────────────────────────────────────────────────────────────────
# MODELOS DISPONIBLES
# ─────────────────────────────────────────────────────────────────────

MODELOS = [

    "llama-3.3-70b-versatile",

    "meta-llama/llama-4-scout-17b-16e-instruct",

    "qwen/qwen3-32b",

    "llama-3.1-8b-instant"
]

with open(
    "training_report.json",
    "r",
    encoding="utf-8"
) as f:

    REPORT = json.load(f)

MEMORIAS = {}

VENTANA = 20

# Modelo actual global
modelo_actual_idx = 0

# ─────────────────────────────────────────────────────────────────────
# CREAR MODELO
# ─────────────────────────────────────────────────────────────────────

def crear_modelo(model_name: str):

    print(f"\n🤖 Modelo activo: {model_name}")

    return ChatGroq(
    model=model_name,
    temperature=0.2,
    max_tokens=1024,
    api_key=os.getenv("GROQ_API_KEY")
    )

# Instancia global
modelo = crear_modelo(MODELOS[modelo_actual_idx])

# ─────────────────────────────────────────────────────────────────────
# CAMBIO AUTOMÁTICO DE MODELO
# ─────────────────────────────────────────────────────────────────────

def cambiar_modelo():

    global modelo
    global modelo_actual_idx

    modelo_actual_idx = (
        modelo_actual_idx + 1
    ) % len(MODELOS)

    nuevo_modelo = MODELOS[
        modelo_actual_idx
    ]

    print(f"\n🔄 Cambiando a: {nuevo_modelo}")

    modelo = crear_modelo(nuevo_modelo)

# ─────────────────────────────────────────────────────────────────────
# TEMPLATE
# ─────────────────────────────────────────────────────────────────────

def generar_contexto():

    return json.dumps(
        REPORT,
        ensure_ascii=False,
        separators=(",", ":")
    )

SYSTEM_PROMPT = f"""
Eres el asistente oficial del proyecto Credit Card Fraud Detection.

La siguiente estructura JSON contiene todas las métricas, rankings, variables, resultados de negocio y conclusiones del proyecto. Utiliza este JSON como única fuente de verdad para responder preguntas.

{generar_contexto()}

Tu función es ayudar a docentes, jurados, clientes potenciales y visitantes a comprender el proyecto, sus resultados y su impacto.

Reglas generales:

* Responde siempre en español.
* Utiliza únicamente información presente en el JSON proporcionado.
* No inventes datos, métricas o resultados.
* Si una métrica o dato no existe en el JSON, indícalo claramente.
* Mantén un tono profesional, claro y fácil de entender.
* Explica conceptos técnicos de forma sencilla cuando sea necesario.
* Adapta el nivel técnico de la respuesta según la pregunta del usuario.

Prioridades de comunicación:

1. Explicar el problema del fraude financiero.
2. Explicar la solución desarrollada.
3. Explicar los resultados obtenidos.
4. Explicar el impacto de negocio.
5. Explicar por qué se seleccionó el modelo final.
6. Explicar cómo podría evolucionar la solución en un entorno real.

Cuando respondas sobre resultados:

* Prioriza los fraudes detectados frente a métricas académicas.
* Prioriza los fraudes perdidos frente a métricas académicas.
* Utiliza las métricas del JSON para justificar las respuestas.
* Si es posible, expresa los resultados de forma comprensible para usuarios no técnicos.

Cuando respondas sobre modelos:

* Explica las diferencias utilizando la información disponible en el JSON.
* Justifica la selección del modelo final utilizando criterios técnicos y de negocio.
* No asumas que la mejor Accuracy implica el mejor modelo.

Cuando respondas sobre impacto:

* Enfatiza reducción de riesgo.
* Enfatiza detección temprana.
* Enfatiza prevención de fraude.
* Enfatiza valor para entidades financieras.

Si una pregunta está fuera del alcance del proyecto, indícalo claramente.
Si existe una respuesta en el JSON, utiliza esa información.
No realices cálculos propios ni asumas valores que no estén presentes.
"""


def obtener_memoria(session_id):

    if session_id not in MEMORIAS:

        MEMORIAS[session_id] = []

    return MEMORIAS[session_id]

# ─────────────────────────────────────────────────────────────────────
# DETECTAR ERRORES DE GROQ
# ─────────────────────────────────────────────────────────────────────

def es_error_groq(error: Exception):

    texto = str(error).lower()

    ERRORES = [
        "429",
        "rate limit",
        "too many requests",
        "timeout",
        "connection",
        "service unavailable",
        "overloaded",
        "quota",
        "internal server error",
        "503",
        "502"
    ]

    return any(
        palabra in texto
        for palabra in ERRORES
    )

# ─────────────────────────────────────────────────────────────────────
# CHAT PRINCIPAL
# ─────────────────────────────────────────────────────────────────────

def preguntar(
    session_id: str,
    mensaje: str
) -> dict:

    global modelo

    historial = obtener_memoria(session_id)

    MAX_REINTENTOS = len(MODELOS)

    ultimo_error = None

    # ─────────────────────────────────────────────────────────────
    # Intentar modelos automáticamente
    # ─────────────────────────────────────────────────────────────
    for intento in range(MAX_REINTENTOS):
        try:
            mensajes = [SystemMessage(content=SYSTEM_PROMPT)]
            mensajes.extend(historial[-VENTANA:])
            mensajes.append(HumanMessage(content=mensaje))

            print(f"🚀 Consultando con: {MODELOS[modelo_actual_idx]}")

            respuesta = modelo.invoke(mensajes).content

            print(f"✅ Respuesta generada por: {MODELOS[modelo_actual_idx]}")

            # Guardar memoria
            historial.append(HumanMessage(content=mensaje))
            historial.append(AIMessage(content=respuesta))

            MEMORIAS[session_id] = historial[-VENTANA:]

            return {

                "respuesta":
                    respuesta,

                "modelo":
                    MODELOS[modelo_actual_idx],

                "session_id":
                    session_id,

                "mensajes_en_memoria":
                    len(MEMORIAS[session_id])
            }

        except Exception as e:

            ultimo_error = e

            print("\n❌ Error:")
            print(str(e))

            # Solo cambiar si es error Groq
            if es_error_groq(e):

                cambiar_modelo()
                continue

            # Error lógico → no rotar
            raise e

    # ─────────────────────────────────────────────────────────────
    # Todos fallaron
    # ─────────────────────────────────────────────────────────────

    raise Exception(
        f"Todos los modelos fallaron: "
        f"{str(ultimo_error)}"
    )
