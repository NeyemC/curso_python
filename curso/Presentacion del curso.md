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

# ✅ Lo que ya construimos
## Un recorrido por las Sesiones 1 a 12

> Ya tenemos el flujo completo: **cargar → limpiar → recodificar → analizar**.

---

# Bloque 1
## Primeros pasos (Sesiones 1–2)

---

## Bloque 1 — Qué logramos

- 🧱 **Jupyter**: celdas que se ejecutan con `Shift`+`Enter`.
- 🔤 **Tipos de datos** como variables de encuesta; los **diccionarios** son las *etiquetas de valor* de SPSS.
- ⭐ El **DataFrame**: abrir la base y mirarla (`.head()`, `.shape`, `.columns`).
- 🔎 **Seleccionar** columnas y **filtrar** casos (el *Seleccionar casos* de SPSS).

> Ya sabemos abrir una encuesta, apuntar a las variables y aislar subgrupos.

---

## Bloque 1 — En código

```python
import pandas as pd
datos = pd.read_csv("datos/encuesta_satisfaccion.csv",
                    sep=";", decimal=",")

# Filtrar: mujeres mayores de 30 (cada condición entre paréntesis)
filtro = (datos["sexo"] == 2) & (datos["edad"] > 30)
datos[filtro].shape
```

---

# Bloque 2
## Manejar la base (Sesiones 3–5)

---

## Bloque 2 — Qué logramos

- 📂 Cargar datos de **verdad**: CSV (`sep`, `decimal`, `encoding`), Excel y **SPSS `.sav`**.
- 🩺 El **"informe de salud"** de una base nueva: `.info()`, `.describe()`, `.isnull()`.
- ✏️ **Renombrar**, ordenar y **crear variables** (ej. tramos de edad con `pd.cut`).

> Diagnosticamos la base *antes* de tocarla: tamaño, tipos, vacíos y rarezas.

---

## Bloque 2 — El puente con SPSS

Leer un `.sav` **sin perder sus etiquetas**:

```python
import pyreadstat
datos, meta = pyreadstat.read_sav("datos/encuesta_satisfaccion.sav")

meta.column_names_to_labels   # etiquetas de variable
meta.variable_value_labels    # etiquetas de valor (1 = "Hombre"...)
```

> Sea CSV, Excel o SPSS, **todo termina en el mismo DataFrame**.

---

## Bloque 2 — Cazar rarezas

`.describe()` delató los **códigos escondidos**:

```python
datos["edad"].max()            # 999 -> "sin dato" disfrazado de número
datos["P5_sat_general"].max()  # 99  -> "No sabe / No responde"
```

> Detectar esto **ahora** evita promedios falsos después.

---

# Bloque 3
## Limpiar y recodificar (Sesiones 6–8)

---

## Bloque 3 — Qué logramos

- 🕳️ **Valores perdidos**: convertir 99/999 en `NaN` y decidir (eliminar / imputar / dejar).
- 🔁 **Recodificar**: `.map()`, `.replace()`, `np.where()`, `pd.cut()` → clasificación NPS.
- 🔤 **Limpiar texto**: estandarizar la región sucia con métodos `.str`.

> Dejamos la base **limpia y confiable** para analizar.

---

## Bloque 3 — En código

```python
# Perdidos: el 999 inflaba el promedio de edad
datos["edad"] = datos["edad"].replace(999, np.nan)

# Recodificar códigos a etiquetas (como las value labels de SPSS)
datos["sexo_txt"] = datos["sexo"].map({1: "Hombre", 2: "Mujer"})

# Texto: 20+ variantes de región -> 5 limpias
datos["region"] = datos["region"].str.strip().str.title()
```

---

# Bloque 4 ❤️
## Analizar la encuesta (Sesiones 9–12) — *el corazón*

---

## Bloque 4 — Qué logramos

- 📊 **Frecuencias** con `n` y `%` (el primer entregable de un estudio).
- 🔀 **Cruces** (`crosstab`): satisfacción × segmento, con % por columna.
- 🧮 **`groupby` / `pivot_table`**: promedios por grupo (tablas dinámicas en código).
- ⚖️ **Ponderación**: frecuencias y promedios **ponderados**.

> Con esto se arma **el grueso de un informe** de encuesta.

---

## Bloque 4 — Cruces y grupos

```python
# ¿Qué % está satisfecho DENTRO de cada segmento?
pd.crosstab(datos["satisf_2c"], datos["sexo_txt"],
            normalize="columns") * 100

# Satisfacción promedio por región
datos.groupby("region")["sat_general"].mean()
```

> El error clásico a evitar: confundir **% por columna** con **% por fila**.

---

## Bloque 4 — Ponderar bien

```python
d = datos.dropna(subset=["sat_general"])

d["sat_general"].mean()                                # sin ponderar
np.average(d["sat_general"], weights=d["ponderador"])  # PONDERADA
```

> Ignorar el ponderador entrega resultados **sesgados**. En opinión pública, puede cambiar titulares.

---

## Próximos pasos

- 🎨 **Bloque 5:** visualizar — gráficos claros y presentables para el cliente.
- 🤖 **Bloque 6:** automatizar el reporte — funciones y exportar a Excel.
- 📈 **Bloque 7:** estadística avanzada — correlación, regresión, factorial y segmentación.
- 🏁 **Proyecto final:** un estudio de encuesta de punta a punta.

---

<!-- _paginate: false -->

# ¡Empecemos! 🚀

**Antes de la Sesión 1:** sigan la *Guía de instalación* (Anaconda + Jupyter).

Dudas → canal de ayuda del curso.
