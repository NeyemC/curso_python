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
> Cada bloque abre con un resumen y luego una lámina por sesión.

---

# Bloque 1
## Primeros pasos (Sesiones 1–2)

---

## Bloque 1 — Resumen

- 🧱 **Jupyter**: celdas que se ejecutan con `Shift`+`Enter`.
- 🔤 **Tipos de datos** como variables de encuesta; los **diccionarios** son las *etiquetas de valor* de SPSS.
- ⭐ El **DataFrame**: abrir la base y mirarla.
- 🔎 **Seleccionar** columnas y **filtrar** casos.

> Ya sabemos abrir una encuesta, apuntar a las variables y aislar subgrupos.

---

## Sesión 1 — "Hola, Python"

El primer contacto: entorno, tipos de datos y el primer DataFrame.

```python
import pandas as pd
datos = pd.read_csv("datos/encuesta_satisfaccion.csv",
                    sep=";", decimal=",")
datos.head()        # (800, 15): 800 casos, 15 variables

etiquetas_sexo = {1: "Hombre", 2: "Mujer"}  # = value labels de SPSS
```

---

## Sesión 2 — Seleccionar y filtrar

Apuntar a la variable y al caso correcto: columnas (*Series* / *DataFrame*), `loc`/`iloc` y filtros.

```python
# Filtrar: mujeres mayores de 30 (cada condición entre paréntesis)
filtro = (datos["sexo"] == 2) & (datos["edad"] > 30)
datos[filtro].shape
```

> El *Seleccionar casos* de SPSS, en una línea y reproducible.

---

# Bloque 2
## Manejar la base (Sesiones 3–5)

---

## Bloque 2 — Resumen

- 📂 Cargar datos de **verdad**: CSV, Excel y **SPSS `.sav`**.
- 🩺 El **"informe de salud"** de una base nueva.
- ✏️ **Renombrar**, ordenar y **crear variables**.

> Diagnosticamos la base *antes* de tocarla: tamaño, tipos, vacíos y rarezas.

---

## Sesión 3 — Cargar datos (CSV, Excel, SPSS)

El puente con nuestro mundo: leer un `.sav` **sin perder sus etiquetas**.

```python
import pyreadstat
datos, meta = pyreadstat.read_sav("datos/encuesta_satisfaccion.sav")

meta.column_names_to_labels   # etiquetas de variable
meta.variable_value_labels    # etiquetas de valor (1 = "Hombre"...)
```

> Sea CSV, Excel o SPSS, **todo termina en el mismo DataFrame**.

---

## Sesión 4 — Explorar y diagnosticar

El "informe de salud": `.info()`, `.describe()`, `.isnull()`, `value_counts()`.

```python
datos["edad"].max()            # 999 -> "sin dato" disfrazado de número
datos["P5_sat_general"].max()  # 99  -> "No sabe / No responde"
```

> Cazar los **códigos escondidos** ahora evita promedios falsos después.

---

## Sesión 5 — Ordenar, renombrar y crear variables

Dejar la base ordenada y con las variables que necesitamos.

```python
datos = datos.rename(columns={"P5_sat_general": "sat_general"})

# Agrupar edad en tramos
datos["tramo_edad"] = pd.cut(datos["edad"], bins=[17, 29, 44, 59, 120],
                             labels=["18-29", "30-44", "45-59", "60+"])
```

---

# Bloque 3
## Limpiar y recodificar (Sesiones 6–8)

---

## Bloque 3 — Resumen

- 🕳️ **Valores perdidos**: convertir 99/999 en `NaN` y decidir qué hacer.
- 🔁 **Recodificar**: `.map()`, `.replace()`, `np.where()`, `pd.cut()`.
- 🔤 **Limpiar texto**: estandarizar variables escritas a mano.

> Dejamos la base **limpia y confiable** para analizar.

---

## Sesión 6 — Valores perdidos

Detectar, decidir y tratar los "No sabe / No responde".

```python
# El 999 inflaba el promedio de edad -> lo vaciamos
datos["edad"] = datos["edad"].replace(999, np.nan)

datos.dropna(subset=["sat_general"])   # o fillna() para imputar
```

> pandas ignora los `NaN` en los cálculos: promedios correctos.

---

## Sesión 7 — Recodificar variables

La tarea más frecuente del análisis de encuestas.

```python
# Códigos -> etiquetas (como las value labels de SPSS)
datos["sexo_txt"] = datos["sexo"].map({1: "Hombre", 2: "Mujer"})

# Clasificación NPS
datos["nps_grupo"] = pd.cut(datos["P6_nps"], bins=[-1, 6, 8, 10],
                    labels=["Detractor", "Pasivo", "Promotor"])
```

---

## Sesión 8 — Limpiar texto y respuestas abiertas

Estandarizar variables de texto y explorar preguntas abiertas.

```python
# 20+ variantes de región -> 5 limpias
datos["region"] = datos["region"].str.strip().str.title()

# Buscar un tema en respuestas abiertas
datos["comentario"].str.contains("espera|demor", case=False, na=False)
```

---

# Bloque 4 ❤️
## Analizar la encuesta (Sesiones 9–12) — *el corazón*

---

## Bloque 4 — Resumen

- 📊 **Frecuencias** con `n` y `%` (el primer entregable).
- 🔀 **Cruces** (`crosstab`) por segmento.
- 🧮 **`groupby` / `pivot_table`**: promedios por grupo.
- ⚖️ **Ponderación**: frecuencias y promedios ponderados.

> Con esto se arma **el grueso de un informe** de encuesta.

---

## Sesión 9 — Frecuencias y descriptivos

El análisis univariado: el primer entregable de casi todo estudio.

```python
# Tabla de frecuencias con n y %
conteo = datos["nps_grupo"].value_counts()
pct = (datos["nps_grupo"].value_counts(normalize=True) * 100).round(1)
pd.DataFrame({"n": conteo, "%": pct})
```

---

## Sesión 10 — Cruces (tablas de contingencia)

El análisis bivariado: "¿el resultado cambia según el segmento?".

```python
# ¿Qué % está satisfecho DENTRO de cada segmento?
pd.crosstab(datos["satisf_2c"], datos["sexo_txt"],
            normalize="columns") * 100
```

> El error clásico a evitar: confundir **% por columna** con **% por fila**.

---

## Sesión 11 — Agrupar y resumir (`groupby`)

Las tablas dinámicas, en código: promedios por grupo.

```python
# Satisfacción promedio por región
datos.groupby("region")["sat_general"].mean()

# Tabla dinámica: región x sexo
pd.pivot_table(datos, index="region", columns="sexo_txt",
               values="sat_general", aggfunc="mean")
```

---

## Sesión 12 — Ponderación

Cuando los casos no valen todos lo mismo (factor de expansión).

```python
d = datos.dropna(subset=["sat_general"])

d["sat_general"].mean()                                # sin ponderar
np.average(d["sat_general"], weights=d["ponderador"])  # PONDERADA
```

> Ignorar el ponderador **sesga** los resultados. En opinión pública, cambia titulares.

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
