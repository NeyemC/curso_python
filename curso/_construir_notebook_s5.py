# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 5 (.ipynb)."""
import json
cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

md(r"""# Sesión 5 — Ordenar, renombrar y crear variables

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- **Renombrar** columnas para que se entiendan (adiós a los `P1_sat_...`).
- **Ordenar** la base según una o más variables.
- **Crear variables nuevas** a partir de las que ya tenemos (ej. un tramo de edad).

> Las bases llegan con nombres crípticos y casi siempre necesitamos construir variables que no venían. Esto es preparar el terreno para el análisis.

---""")

md(r"""## 0. Cargamos la base""")
code(r"""import pandas as pd
import numpy as np

datos = pd.read_csv("datos/encuesta_satisfaccion.csv", sep=";", decimal=",")
datos.head(3)""")

md(r"""## 1. Renombrar columnas

Los nombres técnicos (`P5_sat_general`) sirven en el cuestionario, pero para trabajar cómodas conviene nombres claros. Usamos `rename` con un diccionario `{"nombre_viejo": "nombre_nuevo"}`.""")
code(r"""datos = datos.rename(columns={
    "P1_sat_atencion": "sat_atencion",
    "P2_sat_tiempos":  "sat_tiempos",
    "P3_sat_app":      "sat_app",
    "P4_sat_sucursal": "sat_sucursal",
    "P5_sat_general":  "sat_general",
    "P6_nps":          "nps",
})
datos.columns""")

md(r"""> 💡 Fíjate que **reasignamos** el resultado a `datos` (`datos = datos.rename(...)`). En pandas, la mayoría de las operaciones **no cambian** la base original: crean una versión modificada que hay que **guardar** en una variable. Es una diferencia importante con SPSS, donde los cambios son "en el archivo".

## 2. Ordenar la base

`sort_values` ordena las filas según una columna. Por defecto va de menor a mayor; con `ascending=False`, al revés.""")
code(r"""# Los clientes más antiguos primero
datos.sort_values("antiguedad_anios", ascending=False).head()""")

md(r"""También podemos ordenar por **varias** columnas a la vez (primero por una, y en caso de empate por la siguiente):""")
code(r"""datos.sort_values(["producto", "antiguedad_anios"], ascending=[True, False]).head()""")

md(r"""> ⚠️ Igual que antes: `sort_values` **no** modifica `datos`, solo muestra una versión ordenada. Si quisieras dejarla ordenada de verdad, tendrías que hacer `datos = datos.sort_values(...)`.

## 3. Crear una variable nueva

### Caso simple: a partir de un cálculo
Crear una columna nueva es tan fácil como "inventarle" un nombre entre corchetes y asignarle un valor. Por ejemplo, el ponderador expresado como porcentaje:""")
code(r"""datos["peso_pct"] = datos["ponderador"] * 100
datos[["ponderador", "peso_pct"]].head()""")

md(r"""### Caso útil: agrupar edad en tramos con `pd.cut`
Muy frecuente en encuestas: convertir la edad (número) en **tramos etarios** (categorías). `pd.cut` corta un rango numérico en intervalos.

Definimos los cortes (`bins`) y las etiquetas de cada tramo:""")
code(r"""datos["tramo_edad"] = pd.cut(
    datos["edad"],
    bins=[17, 29, 44, 59, 120],                 # (17-29], (29-44], (44-59], (59-120]
    labels=["18-29", "30-44", "45-59", "60+"]
)
datos[["edad", "tramo_edad"]].head(10)""")

md(r"""¿Y qué pasó con los `edad = 999` (el código de "sin dato")? Como 999 queda **fuera** del último corte (120), `pd.cut` le pone `NaN` automáticamente. ¡Justo lo que queremos! Comprobémoslo:""")
code(r"""# Cuántos casos quedaron sin tramo (los 999 y cualquier edad fuera de rango)
datos["tramo_edad"].isnull().sum()""")

md(r"""Y así se ve el reparto por tramo:""")
code(r"""datos["tramo_edad"].value_counts().sort_index()""")

md(r"""## 4. Manos a la obra: dejar la base lista

Recapitulando, dejamos la base con nombres legibles y con dos variables nuevas útiles (`tramo_edad` y `peso_pct`). Miremos el resultado:""")
code(r"""datos[["sexo", "edad", "tramo_edad", "sat_general", "nps"]].head()""")

md(r"""## 5. Conexión con SPSS

| En SPSS | Hoy en Python |
|---|---|
| Renombrar variable (Vista de Variables) | `datos.rename(columns={...})` |
| Datos → Ordenar casos | `datos.sort_values(...)` |
| Transformar → Calcular variable | `datos["nueva"] = ...` |
| Transformar → Recodificar en rangos (agrupar edad) | `pd.cut(...)` |

---

## 6. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio.**

1. Renombra la columna `antiguedad_anios` a `antiguedad` (recuerda guardar el resultado en `datos`).
2. Ordena la base por `edad` de mayor a menor y muestra las primeras filas. ¿Qué valor aparece arriba de todo y por qué?
3. Crea una variable nueva `sat_general_pct` que sea `sat_general` multiplicada por 20 (para llevar la escala 1-5 a 0-100, aprox).
4. Crea una variable `antiguo` que valga `True` si `antiguedad` es 10 o más, y `False` si no. *(Pista: `datos["antiguedad"] >= 10`.)*
5. **Desafío:** crea un tramo de antigüedad con `pd.cut` usando los cortes `[-1, 2, 9, 25]` y las etiquetas `["Nuevo", "Intermedio", "Antiguo"]`.""")
code("# Ejercicio 1: renombrar antiguedad_anios -> antiguedad\n")
code("# Ejercicio 2: ordenar por edad (mayor a menor)\n")
code("# Ejercicio 3: crear sat_general_pct\n")
code("# Ejercicio 4: crear variable booleana 'antiguo'\n")
code("# Ejercicio 5 (desafío): tramo de antigüedad con pd.cut\n")

md(r"""> En la **Sesión 6** atacamos de frente los **valores perdidos**: convertir esos códigos 99/999 en verdaderos vacíos y decidir qué hacer con ellos. ¡Empieza la limpieza en serio!""")

notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.x"}},"nbformat":4,"nbformat_minor":5}
with open("curso/05 - Sesion 5 - Ordenar, renombrar y crear variables.ipynb","w",encoding="utf-8") as f:
    json.dump(notebook,f,ensure_ascii=False,indent=1)
print("S5 OK", len(cells), "celdas")
