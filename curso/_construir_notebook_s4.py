# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 4 (.ipynb)."""
import json
cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

md(r"""# Sesión 4 — Explorar y diagnosticar la base: el "informe de salud"

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Hacer un **diagnóstico rápido** de una base recién llegada del terreno.
- Conocer su tamaño, sus **tipos de variable** y sus valores faltantes.
- **Detectar rarezas**: códigos extraños, categorías mal escritas, valores imposibles.

> 🩺 Antes de analizar *nada*, un buen analista siempre le toma "los signos vitales" a la base. Esta sesión es ese chequeo. Nos ahorra errores graves más adelante.

---""")

md(r"""## 0. Cargamos la base""")
code(r"""import pandas as pd

datos = pd.read_csv("datos/encuesta_satisfaccion.csv", sep=";", decimal=",")
datos.head()""")

md(r"""## 1. `.info()` — la ficha técnica de la base

`.info()` nos da, de un vistazo: cuántas filas hay, cuántas columnas, el **tipo** de cada una y **cuántos valores no-nulos** tiene.""")
code(r"""datos.info()""")

md(r"""Lee esa salida con calma. Nos dice:
- **800 entries** → 800 filas (personas).
- **15 columns** → 15 variables.
- La columna `Non-Null Count`: casi todas dicen `800 non-null`, pero **`comentario` dice mucho menos**. Ahí hay valores faltantes.
- La columna `Dtype`: el tipo de cada variable (`int64`, `float64`, `object`=texto).

## 2. `.dtypes` — ¿de qué tipo es cada variable?

A veces solo queremos los tipos. Ojo, porque los tipos revelan cosas:""")
code(r"""datos.dtypes""")

md(r"""> 🔍 **Detalle de detective:** `edad` aparece como `float64` (con decimales), cuando la edad debería ser un número entero. Eso es una **pista** de que algo raro pasa en esa columna (spoiler: hay un código `999`). Los tipos "inesperados" casi siempre esconden datos sucios.

## 3. `.describe()` — los estadísticos que delatan rarezas

`.describe()` resume las variables numéricas (media, mínimo, máximo, etc.). Más allá de los promedios, lo usamos para **cazar valores imposibles**: fíjate en los `min` y `max`.""")
code(r"""datos.describe()""")

md(r"""¡Mira dos cosas!
- En **`edad`**, el `max` es **999**. Nadie tiene 999 años: es un **código de "sin dato"** disfrazado de número.
- En las preguntas **`P1`...`P5`**, el `max` es **99**. La escala era de 1 a 5, así que ese 99 es el código de **"No sabe / No responde"**.

Estos códigos son peligrosísimos: si calculáramos el promedio de edad *sin darnos cuenta*, ¡saldría inflado por los 999! Detectarlos ahora es justamente el punto del diagnóstico.

## 4. `.isnull().sum()` — ¿dónde faltan datos?

Cuenta, por columna, cuántos valores están **realmente vacíos** (`NaN`).""")
code(r"""datos.isnull().sum()""")

md(r"""Confirmamos que **`comentario`** tiene muchos vacíos (mucha gente no dejó comentario abierto: es normal). El resto aparece completo... *pero ya sabemos que esconde perdidos como códigos (99, 999)*. Esa es la gran lección de hoy:

> ⚠️ **Faltan datos de dos maneras:** los `NaN` visibles **y** los códigos escondidos (99, 999). `.isnull()` solo ve los primeros; `.describe()` y `value_counts()` nos ayudan a cazar los segundos.

## 5. `value_counts()` — mirar las categorías una por una

Para las variables categóricas (texto o códigos), `value_counts()` lista cada valor y cuántas veces aparece. Es nuestra herramienta para **ver rarezas**.""")
code(r"""datos["sexo"].value_counts()""")

md(r"""Vemos `1` (Hombre), `2` (Mujer) y un puñado de `9` ("Sin dato"). Ahora miremos la región, que viene del terreno escrita a mano:""")
code(r"""datos["region"].value_counts()""")

md(r"""😱 ¡Un desastre típico y muy real! La misma región aparece escrita de mil formas: `Metropolitana`, `METROPOLITANA`, `metropolitana`, `  Metropolitana` (con espacios)... Para el computador son categorías **distintas**. Si hiciéramos una tabla ahora, saldría fragmentada.

> 🧹 Limpiar esto es la **Sesión 8**. Hoy solo lo *diagnosticamos*: sabemos que existe y que habrá que arreglarlo.

Veamos también una pregunta de satisfacción, para ver el código 99 en acción:""")
code(r"""datos["P5_sat_general"].value_counts().sort_index()""")

md(r"""Ahí está: además de las notas 1 a 5, hay 25 casos con código **99** (No sabe/No responde) que tendremos que tratar.

## 6. Manos a la obra: el "informe de salud" de la base

Juntemos todo en un diagnóstico rápido, como el que harías al recibir una base nueva de un estudio.""")
code(r"""print("¿Cuántos casos y variables?")
print("  ", datos.shape[0], "casos,", datos.shape[1], "variables")

print("\n¿Cuántos vacíos (NaN) hay por columna?")
faltantes = datos.isnull().sum()
print(faltantes[faltantes > 0])   # mostramos solo las que tienen vacíos

print("\n¿Valores máximos sospechosos? (posibles códigos escondidos)")
print("   edad máx:", datos["edad"].max(), "| P5 máx:", datos["P5_sat_general"].max())""")

md(r"""Con eso ya sabemos **qué terreno pisamos** y qué habrá que limpiar. Ese es el objetivo: nunca empezar a analizar a ciegas.

## 7. Conexión con SPSS

| En SPSS | Hoy en Python |
|---|---|
| Ver el N y la lista de variables | `datos.info()` |
| Analizar → Frecuencias | `datos["var"].value_counts()` |
| Analizar → Descriptivos | `datos.describe()` |
| Revisar la Vista de Variables (tipos) | `datos.dtypes` |
| Buscar perdidos y valores fuera de rango | `.isnull().sum()` + revisar `min`/`max` |

---

## 8. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio.**

1. Aplica `.info()` a la base y responde: ¿cuál es la **única** columna con valores faltantes visibles?
2. Usa `.describe()` y revisa la columna `antiguedad_anios`: ¿cuál es su valor mínimo y máximo? ¿Se ven razonables?
3. Haz un `value_counts()` de la columna `producto`. ¿Cuál es el producto más frecuente?
4. Haz un `value_counts()` de `P6_nps` ordenado por índice (`.sort_index()`). ¿Aparece el código 99?
5. **Reflexión (responde en una celda de texto):** ¿por qué es peligroso calcular `datos["edad"].mean()` tal como está la base ahora?""")
code("# Ejercicio 1: .info()\n")
code("# Ejercicio 2: describe() de antiguedad_anios\n")
code("# Ejercicio 3: value_counts de producto\n")
code("# Ejercicio 4: value_counts de P6_nps ordenado\n")
code("# Ejercicio 5: escribe tu reflexión aquí como comentario, o crea una celda de texto\n")

md(r"""> En la **Sesión 5** dejaremos la base más ordenada: **renombrar** columnas para que se entiendan, **ordenar** casos y **crear variables nuevas** (como un tramo de edad).""")

notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.x"}},"nbformat":4,"nbformat_minor":5}
with open("curso/04 - Sesion 4 - Explorar y diagnosticar.ipynb","w",encoding="utf-8") as f:
    json.dump(notebook,f,ensure_ascii=False,indent=1)
print("S4 OK", len(cells), "celdas")
