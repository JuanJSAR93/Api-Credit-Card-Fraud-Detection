# Credit Card Fraud Detection

## Resumen Ejecutivo

Este proyecto desarrolla una solución de Inteligencia Artificial para detección de fraude financiero.

El objetivo es identificar transacciones fraudulentas antes de que generen pérdidas económicas.

La solución fue evaluada desde una perspectiva técnica y de negocio.

---

# Escala del Problema

Dataset original:

21.000.000 transacciones

Dataset de trabajo:

164.820 transacciones

Fraudes:

27.470

Legítimas:

137.350

Ratio utilizado:

5:1

---

# Variables Utilizadas

* step
* type
* amount
* oldbalanceOrg
* newbalanceOrig
* oldbalanceDest
* newbalanceDest

---

# Modelos Evaluados

1. Logistic Regression
2. Random Forest
3. XGBoost
4. Red Neuronal

---

# Modelo Seleccionado

Red Neuronal

Fue el mejor modelo tanto desde el punto de vista técnico como desde el impacto de negocio.

---

# Resultados Principales

Recall:

83.16%

Fraudes Detectados:

4569

Fraudes Perdidos:

925

Business Score:

-1190.75

La solución logró detectar aproximadamente 5 fraudes por cada fraude que logró pasar desapercibido.

---

# Comparativa de Modelos

Red Neuronal

* Recall: 83.16%
* F1: 0.2790
* Fraudes detectados: 4569

Logistic Regression

* Recall: 48.43%
* Fraudes detectados: 2661

XGBoost

* Recall: 39.50%
* Fraudes detectados: 2170

Random Forest

* Recall: 28.80%
* Fraudes detectados: 1582

---

# Variables Más Importantes

1. oldbalanceDest
2. newbalanceOrig
3. oldbalanceOrg
4. newbalanceDest
5. amount

Los saldos antes y después de la transacción fueron los factores más relevantes para detectar fraude.

---

# Hallazgos

* El balance de datos mejoró el aprendizaje.
* La Red Neuronal obtuvo el mejor resultado.
* No se detectó overfitting.
* Los balances de cuenta fueron los predictores más importantes.
* Detectar fraude es más importante que minimizar falsas alarmas.

---

# Regla de Negocio

Business Score:

TP − (FP × 0.05) − (FN × 5)

Perder un fraude tiene un costo mucho mayor que generar una revisión adicional.

---

# Instrucciones para el Asistente

Siempre responder en español.

Priorizar lenguaje de negocio.

Explicar conceptos técnicos de manera sencilla.

Si una pregunta no está relacionada con el proyecto, indicarlo claramente.

Cuando sea posible, enfatizar:

* Fraudes detectados.
* Impacto económico.
* Beneficios para entidades financieras.
* Escalabilidad futura.
