# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 10 (.ipynb)."""
import json
cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

PREP = r'''import pandas as pd
import numpy as np

datos = pd.read_csv("datos/encuesta_satisfaccion.csv", sep=";", decimal=",")

# --- Limpieza + recodificación (Bloque 3) ---
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
datos["nps_grupo"] = pd.cut(datos["P6_nps"], bins=[-1, 6, 8, 10],
                            labels=["Detractor", "Pasivo", "Promotor"])
# Satisfacción resumida en 2 categorías, útil para cruces
datos["satisf_2c"] = np.where(datos["sat_general"] >= 4, "Satisfecho", "No satisfecho")
datos.loc[datos["sat_general"].isnull(), "satisf_2c"] = np.nan
datos.head(3)'''

md(r"""# Sesión 10 — Cruces: tablas de contingencia (análisis bivariado)

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Construir **tablas de contingencia** (cruces) con `pd.crosstab()`.
- Leerlas en **porcentaje por fila** o **por columna** — y no confundirlos.
- Cruzar la satisfacción contra segmentos (sexo, edad, región).

> 🔀 "¿El resultado cambia según el segmento?" es **la** pregunta de la consultoría. Los cruces son la herramienta para responderla.

---""")

md(r"""## 0. Preparamos la base""")
code(PREP)

md(r"""## 1. El cruce más simple: conteos

`pd.crosstab(filas, columnas)` cuenta cuántos casos caen en cada combinación. Crucemos **satisfacción (2 categorías) × sexo**.""")
code(r"""pd.crosstab(datos["satisf_2c"], datos["sexo_txt"])""")

md(r"""Esa tabla dice, por ejemplo, cuántas mujeres están satisfechas, cuántos hombres no lo están, etc. Útil, pero los **conteos crudos** son difíciles de comparar si los grupos tienen distinto tamaño. Por eso casi siempre usamos **porcentajes**.

## 2. Porcentajes: la decisión más importante del cruce

Un cruce se puede porcentuar de tres formas, y **elegir mal cambia la conclusión**. Se controla con `normalize`:

| `normalize=` | Los % suman 100 en... | Responde la pregunta |
|---|---|---|
| `"columns"` | cada **columna** | "dentro de cada grupo, ¿qué % está satisfecho?" |
| `"index"` | cada **fila** | "de los satisfechos, ¿qué % es hombre/mujer?" |
| `"all"` | el total | "¿qué % del total es cada celda?" |

En consultoría, lo más habitual es **porcentaje por columna**: fijamos el segmento (la columna) y vemos cómo se reparte la respuesta dentro de él.""")
code(r"""# % por columna: dentro de cada sexo, ¿qué % está satisfecho?
tabla = pd.crosstab(datos["satisf_2c"], datos["sexo_txt"], normalize="columns") * 100
tabla.round(1)""")

md(r"""Ahora sí es comparable: podemos leer directamente "el X% de las mujeres está satisfecho vs. el Y% de los hombres", **sin importar** que haya más de un grupo que de otro.

> ⚠️ **El error clásico:** confundir "% por columna" con "% por fila". No es lo mismo *"el 70% de las mujeres está satisfecho"* que *"el 55% de los satisfechos son mujeres"*. Antes de escribir una conclusión, pregúntate **sobre qué base** está el porcentaje.

## 3. Añadir los totales (márgenes)

Con `margins=True` agregamos la fila/columna de totales, muy útil para el informe.""")
code(r"""pd.crosstab(datos["satisf_2c"], datos["sexo_txt"],
            margins=True, margins_name="Total")""")

md(r"""## 4. Cruzar contra otros segmentos

La gracia es repetir el cruce contra las variables de segmentación que interesen. **Satisfacción × tramo de edad:**""")
code(r"""(pd.crosstab(datos["satisf_2c"], datos["tramo_edad"], normalize="columns") * 100).round(1)""")

md(r"""**Satisfacción × región:**""")
code(r"""(pd.crosstab(datos["satisf_2c"], datos["region"], normalize="columns") * 100).round(1)""")

md(r"""> 💡 Aquí se nota por qué limpiamos la región en la Sesión 8: si no, este cruce tendría 20+ columnas basura (`METROPOLITANA`, `  Metropolitana`...) en vez de 5 regiones limpias.

## 5. Cruzar dos variables categóricas cualesquiera

Los cruces no son solo de satisfacción. Cualquier par sirve. Por ejemplo, **producto × tramo de edad** (¿qué productos prefiere cada edad?):""")
code(r"""(pd.crosstab(datos["producto"], datos["tramo_edad"], normalize="columns") * 100).round(1)""")

md(r"""## 6. Manos a la obra: un cruce listo para el informe

Cerramos con un cruce completo, con porcentajes por columna y totales: **grupo NPS × sexo**.""")
code(r"""cruce_nps = pd.crosstab(datos["nps_grupo"], datos["sexo_txt"],
                        normalize="columns") * 100
cruce_nps.round(1)""")

md(r"""## 7. Conexión con SPSS

| En SPSS | Hoy en Python |
|---|---|
| Analizar → Tablas de contingencia (Crosstabs) | `pd.crosstab(filas, columnas)` |
| Porcentajes por columna | `normalize="columns"` |
| Porcentajes por fila | `normalize="index"` |
| Mostrar totales | `margins=True` |

---

## 8. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio.** *(Ejecuta primero la celda de preparación.)*

1. Cruza `nps_grupo` (filas) con `region` (columnas) en **conteos** (sin porcentaje).
2. Repite el cruce anterior pero en **% por columna**. ¿Qué región tiene mayor % de Promotores?
3. Cruza `satisf_2c` con `producto` en % por columna. ¿Qué producto tiene clientes más satisfechos?
4. Haz el cruce `satisf_2c` × `sexo_txt` pero en **% por fila** (`normalize="index"`) y explícale a una compañera en qué cambia la lectura respecto al % por columna.
5. **Desafío:** cruza `tramo_edad` × `producto` con `margins=True` y % por columna.""")
code("# Ejercicio 1: crosstab nps_grupo x region (conteos)\n")
code("# Ejercicio 2: mismo cruce en % por columna\n")
code("# Ejercicio 3: satisf_2c x producto en % por columna\n")
code("# Ejercicio 4: satisf_2c x sexo_txt en % por fila\n")
code("# Ejercicio 5 (desafío): tramo_edad x producto, margins + % por columna\n")

md(r"""> En la **Sesión 11** veremos `groupby` y `pivot_table`: en vez de contar categorías, calcularemos **promedios por grupo** ("satisfacción promedio por región, por producto..."). Son las tablas dinámicas, en código.""")

notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.x"}},"nbformat":4,"nbformat_minor":5}
with open("curso/10 - Sesion 10 - Cruces (tablas de contingencia).ipynb","w",encoding="utf-8") as f:
    json.dump(notebook,f,ensure_ascii=False,indent=1)
print("S10 OK", len(cells), "celdas")
