# Fraud Detection AI Assistant

## Objetivo

Este proyecto implementa una API FastAPI que expone un asistente conversacional basado en Groq.

El asistente responde preguntas sobre el proyecto universitario:

Credit Card Fraud Detection.

La API será consumida desde una landing page desplegada en GitHub Pages.

---

## Arquitectura

Frontend

* GitHub Pages
* HTML
* CSS
* JavaScript

Backend

* FastAPI
* Groq API

No utilizar:

* LangChain
* LlamaIndex
* ChromaDB
* Pinecone
* FAISS
* Bases vectoriales

Toda la información relevante del proyecto se encuentra en PROJECT_CONTEXT.md.

---

## Objetivo del asistente

Responder preguntas como:

* ¿Por qué ganó la Red Neuronal?
* ¿Qué significa Recall?
* ¿Qué variables fueron más importantes?
* ¿Qué impacto tiene la solución?
* ¿Qué modelos se compararon?

---

## Estilo de respuesta

Las respuestas deben:

* Ser claras.
* Estar en español.
* Ser comprensibles para personas no técnicas.
* Priorizar lenguaje de negocio.
* Evitar exceso de terminología académica.

---

## Enfoque comercial

La narrativa debe enfocarse en:

* Fraudes detectados.
* Riesgo mitigado.
* Impacto para entidades financieras.
* Escalabilidad.
* Inteligencia Artificial aplicada.

No centrar la conversación en Accuracy, F1 o métricas académicas salvo que el usuario lo solicite.

---

## Endpoint Principal

POST /chat

Body:

{
"question": "¿Por qué ganó la Red Neuronal?"
}

Response:

{
"answer": "..."
}
