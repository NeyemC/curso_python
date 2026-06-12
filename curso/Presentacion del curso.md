---
marp: true
title: Python para Análisis de Encuestas
author: Equipo de Consultoría
paginate: true
theme: default
---

<!-- _paginate: false -->

# 🐍 Python para Análisis de Encuestas

### Curso interno del equipo

De la base de datos al informe: limpiar, analizar y presentar resultados de encuestas con Python.

---

## ¿Por qué este curso?

- Somos un equipo de consultoría: **estudios de mercado, CX, opinión pública** y estudios sociales.
- Casi todos nuestros proyectos pasan por una **encuesta** y su análisis.
- Hoy lo resolvemos con **Excel y SPSS** — herramientas potentes, pero con límites: trabajo manual, poco reproducible, difícil de auditar y repetir.

> La idea no es reemplazar lo que sabemos, sino **sumar una herramienta** que nos ahorre horas y nos dé control total sobre el análisis.

---

## La gran idea

| Hoy (clic a clic) | Con Python |
|---|---|
| Recodifico a mano cada vez | Lo escribo **una vez** y lo reutilizo |
| Difícil repetir el análisis | **Reproducible**: mismo código, mismo resultado |
| Tablas y gráficos manuales | **Automatizados** para todo el estudio |
| El "cómo lo hice" se pierde | Queda **documentado** en el código |

**El objetivo final:** que cada una termine con una *plantilla reutilizable* para sus próximos estudios.

---

## Objetivos del curso

Al terminar, el equipo podrá:

- 📂 Abrir cualquier base de encuesta (**CSV, Excel, SPSS**).
- 🧹 **Limpiar y recodificar** de forma documentada.
- 📊 Producir **frecuencias, cruces y promedios** (ponderados si corresponde).
- 📈 Construir **índices, NPS** y aplicar técnicas **multivariadas**.
- 🎨 Generar **gráficos presentables** y un libro de tablas en Excel.

---

## Cómo trabajamos

- 🗓️ **Una sesión por semana**, de 1 a 1½ hora, en vivo y con el cuaderno abierto.
- 🎯 Enfoque **práctico**: partimos de un *problema real de un estudio* y recién ahí aparece el concepto de Python que lo resuelve.
- 🔗 Todo se traduce a lo que **ya conocemos** de Excel y SPSS.
- 🧩 Curso **modular**: las primeras ~9 sesiones son el núcleo; luego, módulos de profundización.

---

## El hilo conductor: el flujo de un estudio

```
  Llega la base
       │
       ▼
   Cargar  →  Limpiar  →  Recodificar
                                │
                                ▼
   Frecuencias  →  Cruces  →  Ponderar
                                │
                                ▼
   Visualizar  →  Automatizar  →  Estadística
                                │
                                ▼
                          📑 Informe
```

Cada sesión avanza un paso de este flujo, siempre sobre **el mismo estudio de ejemplo**.

---

## Mapa del curso

| Bloque | Tema |
|---|---|
| **0** | Preparación (instalación) |
| **1** | Primeros pasos *(Sesiones 1–2)* |
| **2** | Manejar la base |
| **3** | Limpiar y recodificar |
| **4** | **Analizar la encuesta** ← el corazón |
| **5** | Visualizar resultados |
| **6** | Automatizar el reporte |
| **7** | Estadística avanzada (correlacional y multivariada) |
| **Final** | Proyecto: un estudio de punta a punta |

---

## Del mundo SPSS al mundo Python

| En Excel / SPSS | En Python (pandas) |
|---|---|
| Una hoja de datos | Un `DataFrame` |
| Una variable / columna | Una `Series` |
| Etiquetas de valor (1 = "Hombre") | Un diccionario `{1: "Hombre"}` |
| Recodificar | `.map()`, `.replace()` |
| Seleccionar casos (filtro) | `datos[datos["edad"] > 30]` |
| Tabla dinámica | `groupby()` / `pivot_table()` |
| Tablas de contingencia | `pd.crosstab()` |

---

## El dataset del curso

Un estudio **ficticio pero realista**: satisfacción de clientes de un banco (CX), **800 respuestas**.

- Sociodemográficos: sexo, edad, región, ciudad.
- Batería de satisfacción tipo **Likert** (1–5).
- Pregunta de recomendación (**NPS**, 0–10).
- **Ponderador** (factor de expansión).
- Y... **"suciedad" intencional** (códigos 99/999, texto inconsistente) para practicar limpieza con datos como los de verdad.

---

# Sesión 1
## "Hola, Python": el entorno, los datos y el DataFrame

---

## Sesión 1 — Lo que vemos

- 🧱 Qué es **Jupyter** y cómo se ejecuta una celda (`Shift`+`Enter`).
- 🔤 **Tipos de datos** pensados como variables de encuesta (números, texto, booleanos).
- 📋 **Listas y diccionarios** → los diccionarios son las *etiquetas de valor* de SPSS.
- ⭐ Abrir nuestra **primera base real** con `pd.read_csv()` y mirarla: `.head()`, `.shape`, `.columns`.

**Resultado:** perderle el miedo a la herramienta y entender qué es un DataFrame.

---

## Sesión 1 — Un vistazo al código

```python
import pandas as pd

# Abrir la base de la encuesta
datos = pd.read_csv("datos/encuesta_satisfaccion.csv",
                    sep=";", decimal=",")

datos.head()        # primeras filas
datos.shape         # (800, 15) -> 800 casos, 15 variables

# Las "etiquetas de valor", como en SPSS
etiquetas_sexo = {1: "Hombre", 2: "Mujer", 9: "Sin dato"}
```

---

# Sesión 2
## Seleccionar y filtrar: apuntar a la variable y al caso correcto

---

## Sesión 2 — Lo que vemos

- 🎯 Quedarnos con **una o varias columnas** (las variables que interesan).
- 📍 `loc` e `iloc`: apuntar a filas y columnas por nombre o por posición.
- 🔎 **Filtrar casos** con condiciones — el *Seleccionar casos* de SPSS.
- ➕ **Combinar criterios** con `&` (y) / `|` (o).

**Reto de la sesión:** aislar a las *mujeres mayores de 30 de la Región Metropolitana*... sorteando la suciedad real de los datos.

---

## Sesión 2 — Un vistazo al código

```python
# Una condición devuelve Verdadero/Falso por fila
datos[datos["edad"] > 60]

# Combinar criterios (¡cada uno entre paréntesis!)
filtro = (datos["sexo"] == 2) & (datos["edad"] > 30)
mujeres_30 = datos[filtro]

mujeres_30.shape   # cuántos casos cumplen
```

> Y de paso aprendemos a esquivar los códigos `999` y a emparejar texto inconsistente.

---

## Próximos pasos

- **Sesión 3:** cargar datos de verdad — CSV, Excel y archivos **`.sav` de SPSS** con sus etiquetas.
- Luego: limpiar, recodificar y entrar al **análisis** (frecuencias, cruces, ponderación).
- Más adelante: visualización, automatización de reportes y **estadística multivariada**.

---

<!-- _paginate: false -->

# ¡Empecemos! 🚀

**Antes de la Sesión 1:** sigan la *Guía de instalación* (Anaconda + Jupyter).

Dudas → canal de ayuda del curso.
