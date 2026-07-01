# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 11 (.ipynb)."""
import json
cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

PREP = r'''import pandas as pd
import numpy as np

datos = pd.read_csv("datos/encuesta_satisfaccion.csv", sep=";", decimal=",")

datos["edad"] = datos["edad"].replace(999, np.nan)
datos["sexo"] = datos["sexo"].replace(9, np.nan)
bateria = ["P1_sat_atencion", "P2_sat_tiempos", "P3_sat_app",
           "P4_sat_sucursal", "P5_sat_general"]
datos[bateria] = datos[bateria].replace(99, np.nan)
datos["P6_nps"] = datos["P6_nps"].replace(99, np.nan)
datos["region"] = datos["region"].str.strip().str.title()

datos["sat_general"] = datos["P5_sat_general"]
datos["sexo_txt"]  = datos["sexo"].map({1: "Hombre", 2: "Mujer"})
datos["tramo_edad"] = pd.cut(datos["edad"], bins=[17, 29, 44, 59, 120],
                             labels=["18-29", "30-44", "45-59", "60+"])
datos.head(3)'''

md(r"""# Sesión 11 — Agrupar y resumir con `groupby` (tablas dinámicas en código)

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Calcular **promedios (y otros resúmenes) por grupo** con `groupby()`.
- Agrupar por **dos variables** a la vez.
- Armar **tablas dinámicas** con `pivot_table()`.

> "¿Cuál es la satisfacción promedio por región? ¿Y por producto?" — este tipo de tabla es el pan de cada día de un informe. Aquí la producimos en una línea.

---""")

md(r"""## 0. Preparamos la base""")
code(PREP)

md(r"""## 1. La idea de `groupby`: *dividir → calcular → juntar*

`groupby` hace tres cosas: **divide** la base en grupos (según una variable), **calcula** algo en cada grupo, y **junta** los resultados en una tabla. En SPSS es la lógica de "dividir el archivo" o de las tablas personalizadas.

Empecemos simple: la **satisfacción promedio por región**.""")
code(r"""datos.groupby("region")["sat_general"].mean().round(2)""")

md(r"""Léelo así: *agrupa por región → toma la satisfacción general → calcula el promedio de cada grupo*. En una línea tenemos el indicador por segmento.

## 2. Otros resúmenes: `count`, `median`, `std`...

No solo promedios. Podemos pedir el conteo (cuántos casos hay por grupo), la mediana, etc.""")
code(r"""# ¿Cuántos casos hay por producto?
datos.groupby("producto")["sat_general"].count()""")

md(r"""### Varios estadísticos a la vez con `.agg()`
`.agg()` permite pedir varias medidas de una sola pasada. Ideal para una tabla resumen.""")
code(r"""datos.groupby("region")["sat_general"].agg(["mean", "median", "count"]).round(2)""")

md(r"""> 💡 Puedes renombrar las columnas para que queden más claras: `.agg(promedio="mean", mediana="median", n="count")`.

## 3. Agrupar por DOS variables

Aquí `groupby` se vuelve potente. Podemos cruzar dos segmentos y ver el promedio en cada combinación: **satisfacción promedio por región y sexo**.""")
code(r"""datos.groupby(["region", "sexo_txt"])["sat_general"].mean().round(2)""")

md(r"""Esa tabla "apilada" tiene toda la información, pero se lee mejor si la **desdoblamos** para que el sexo quede en columnas. Eso es exactamente lo que hace `pivot_table`.

## 4. `pivot_table`: la tabla dinámica de Excel, en código

`pivot_table` es la versión "tabla dinámica" de `groupby`. Le decimos: qué va en las **filas** (`index`), qué en las **columnas** (`columns`), qué **valor** resumir (`values`) y **cómo** (`aggfunc`).""")
code(r"""pd.pivot_table(
    datos,
    index="region",        # filas
    columns="sexo_txt",    # columnas
    values="sat_general",  # qué resumimos
    aggfunc="mean"         # cómo lo resumimos
).round(2)""")

md(r"""¡Idéntico a una tabla dinámica! Satisfacción promedio con región en las filas y sexo en las columnas. Podemos cambiar cualquier pieza para responder otra pregunta.

**Ejemplo:** satisfacción promedio por producto (filas) y tramo de edad (columnas):""")
code(r"""pd.pivot_table(datos, index="producto", columns="tramo_edad",
               values="sat_general", aggfunc="mean").round(2)""")

md(r"""### Totales en el pivote
Igual que en los cruces, `margins=True` agrega los totales (aquí, el promedio general de cada fila/columna).""")
code(r"""pd.pivot_table(datos, index="region", values="sat_general",
               aggfunc="mean", margins=True, margins_name="Total").round(2)""")

md(r"""## 5. `groupby` no es solo promedios de satisfacción

Sirve para resumir cualquier cosa. Por ejemplo, la **antigüedad promedio** y la **edad promedio** por producto, juntas:""")
code(r"""datos.groupby("producto")[["antiguedad_anios", "edad"]].mean().round(1)""")

md(r"""## 6. Manos a la obra: indicador por segmento y zona

Cerramos con la tabla típica de un informe de satisfacción: **promedio de satisfacción por región y sexo**, redondeado y ordenado.""")
code(r"""tabla = pd.pivot_table(datos, index="region", columns="sexo_txt",
                       values="sat_general", aggfunc="mean").round(2)
tabla.sort_values("Mujer", ascending=False)""")

md(r"""## 7. Conexión con SPSS

| En SPSS | Hoy en Python |
|---|---|
| Datos → Dividir archivo + un análisis | `groupby("var")[...]` |
| Medias por grupo (Analizar → Medias) | `groupby("var")["y"].mean()` |
| Tablas personalizadas / Tabla dinámica | `pivot_table(...)` |
| Varios estadísticos a la vez | `.agg([...])` |

---

## 8. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio.** *(Ejecuta primero la celda de preparación.)*

1. Calcula la satisfacción promedio (`sat_general`) por `producto`.
2. Calcula el promedio de `P3_sat_app` por `tramo_edad`. ¿Qué edad está más satisfecha con la app?
3. Con `.agg()`, muestra promedio, mediana y n de `P6_nps` por `region`.
4. Arma un `pivot_table` con `producto` en filas, `sexo_txt` en columnas y el promedio de `antiguedad_anios`.
5. **Desafío:** arma un `pivot_table` de la satisfacción promedio por `tramo_edad` (filas) y `region` (columnas), con totales (`margins=True`).""")
code("# Ejercicio 1: sat_general promedio por producto\n")
code("# Ejercicio 2: P3_sat_app promedio por tramo_edad\n")
code("# Ejercicio 3: agg (promedio, mediana, n) de P6_nps por region\n")
code("# Ejercicio 4: pivot_table antiguedad por producto x sexo\n")
code("# Ejercicio 5 (desafío): pivot_table satisfacción por tramo_edad x region con totales\n")

md(r"""> En la **Sesión 12** cerramos el bloque de análisis con la **ponderación**: cuando los casos no valen todos lo mismo (factor de expansión). Recalcularemos frecuencias y promedios **ponderados** y veremos cuánto cambian los resultados.""")

notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.x"}},"nbformat":4,"nbformat_minor":5}
with open("curso/11 - Sesion 11 - Agrupar y resumir (groupby).ipynb","w",encoding="utf-8") as f:
    json.dump(notebook,f,ensure_ascii=False,indent=1)
print("S11 OK", len(cells), "celdas")
