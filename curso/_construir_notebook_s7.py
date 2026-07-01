# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 7 (.ipynb)."""
import json
cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

md(r"""# Sesión 7 — Recodificar variables (el pan de cada día)

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Convertir **códigos en etiquetas** con `.map()` (1 → "Hombre").
- Reemplazar valores puntuales con `.replace()`.
- Crear variables **condicionales** con `np.where()`.
- **Agrupar** en categorías con `pd.cut()` y construir la clasificación **NPS**.

> Recodificar es, probablemente, **la tarea más frecuente** de todo el análisis de encuestas. Si dominas esta sesión, ya te defiendes solita en el día a día.

---""")

md(r"""## 0. Cargamos la base (y limpiamos los códigos, como en la Sesión 6)""")
code(r"""import pandas as pd
import numpy as np

datos = pd.read_csv("datos/encuesta_satisfaccion.csv", sep=";", decimal=",")

# Dejamos los perdidos como NaN (repaso de la sesión anterior)
datos["edad"]   = datos["edad"].replace(999, np.nan)
datos["P6_nps"] = datos["P6_nps"].replace(99, np.nan)
datos["sexo"]   = datos["sexo"].replace(9, np.nan)
datos.head(3)""")

md(r"""## 1. `.map()` — traducir códigos a etiquetas

Este es el reencuentro con los **diccionarios** de la Sesión 1. `.map()` recorre una columna y reemplaza cada código por su etiqueta, según el diccionario que le demos.""")
code(r"""etiquetas_sexo = {1: "Hombre", 2: "Mujer"}

datos["sexo_txt"] = datos["sexo"].map(etiquetas_sexo)
datos[["sexo", "sexo_txt"]].head()""")

md(r"""¡Listo! Creamos una versión legible `sexo_txt` sin perder la original. Comprobemos el reparto:""")
code(r"""datos["sexo_txt"].value_counts(dropna=False)""")

md(r"""> 💡 `.map()` con un valor que **no está** en el diccionario devuelve `NaN`. Por eso, los `NaN` de sexo (los antiguos "9") siguen como `NaN`. Es el comportamiento que queremos.

## 2. `.replace()` — cambiar valores puntuales

Cuando solo quieres cambiar **algunos** valores (y dejar el resto igual), `.replace()` es más cómodo que `.map()`. Por ejemplo, acortar los nombres de producto:""")
code(r"""datos["producto_corto"] = datos["producto"].replace({
    "Cuenta Corriente":   "CtaCte",
    "Cuenta Vista":       "CtaVista",
    "Tarjeta de Credito": "TC",
    "Credito de Consumo": "CC",
})
datos["producto_corto"].value_counts()""")

md(r"""> **`.map()` vs `.replace()`:** `map` reemplaza *todo* según el diccionario (lo que no esté, queda `NaN`); `replace` solo toca lo que nombras y **deja intacto** el resto. Para traducir una variable completa → `map`; para cambios parciales → `replace`.

## 3. `np.where()` — crear una variable condicional (sí/no)

`np.where(condición, valor_si_verdadero, valor_si_falso)` es como la función SI de Excel. Perfecta para variables binarias.""")
code(r"""# ¿Cliente "satisfecho"? (nota 4 o 5 en satisfacción general)
datos["satisfecho"] = np.where(datos["P5_sat_general"] >= 4, "Satisfecho", "No satisfecho")
datos[["P5_sat_general", "satisfecho"]].head()""")

md(r"""> ⚠️ **Ojo con los `NaN`:** `np.where` evalúa `NaN >= 4` como `False`, así que los que no respondieron caerían en "No satisfecho", lo cual sería injusto. Cuando el faltante importa, conviene un paso extra; lo vemos en el reto de abajo.

## 4. `pd.cut()` — agrupar un número en categorías

Ya lo vimos con la edad en la Sesión 5. Aquí lo usamos para lo más pedido en CX: la clasificación **NPS**.

**Recordatorio de NPS** (pregunta "¿qué tan probable es que recomiendes?", 0 a 10):
- **0 a 6** → Detractores
- **7 y 8** → Pasivos
- **9 y 10** → Promotores""")
code(r"""datos["nps_grupo"] = pd.cut(
    datos["P6_nps"],
    bins=[-1, 6, 8, 10],                          # (-1,6] , (6,8] , (8,10]
    labels=["Detractor", "Pasivo", "Promotor"]
)
datos["nps_grupo"].value_counts()""")

md(r"""Con esa clasificación ya podríamos calcular el indicador NPS (lo formalizamos en la Sesión 17). Los `NaN` de `nps` quedaron fuera de los grupos, como corresponde.

## 5. Manos a la obra: las tres recodificaciones típicas

Dejamos la base con las variables recodificadas que se usan en casi todos los estudios: sexo en texto, tramo de edad y grupo NPS.""")
code(r"""# Tramo de edad (repaso de pd.cut)
datos["tramo_edad"] = pd.cut(datos["edad"], bins=[17, 29, 44, 59, 120],
                             labels=["18-29", "30-44", "45-59", "60+"])

datos[["sexo_txt", "tramo_edad", "nps_grupo"]].head(10)""")

md(r"""## 6. Conexión con SPSS

| En SPSS | Hoy en Python |
|---|---|
| Recodificar en distintas variables (con etiquetas) | `.map({...})` |
| Recodificar algunos valores | `.replace({...})` |
| Transformar → Calcular (con condición SI) | `np.where(cond, a, b)` |
| Recodificar en rangos (agrupar) | `pd.cut(...)` |

---

## 7. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio.** *(Ejecuta primero las celdas de arriba.)*

1. Crea `nps_txt` a partir de `nps_grupo` pero solo confirma su `value_counts()`. ¿Cuántos Promotores hay?
2. Usando `.map()`, crea una variable `region_zona` que agrupe: `"Metropolitana"` → `"Centro"` y el resto de regiones que quieras. *(Puedes inventar la agrupación; lo importante es practicar el diccionario.)*
3. Con `np.where()`, crea `recomienda` que valga `"Sí"` si `P6_nps >= 9` y `"No"` en caso contrario.
4. Con `pd.cut()`, agrupa `antiguedad_anios` en `["Nuevo", "Intermedio", "Antiguo"]` usando los cortes `[-1, 2, 9, 25]`.
5. **Desafío:** crea `satisfecho_v2` con `np.where`, pero que devuelva `np.nan` cuando `P5_sat_general` sea `NaN`. *(Pista: puedes anidar dos `np.where`, o usar `.where()` de pandas.)*""")
code("# Ejercicio 1: value_counts de nps_grupo\n")
code("# Ejercicio 2: region_zona con .map()\n")
code("# Ejercicio 3: recomienda con np.where\n")
code("# Ejercicio 4: tramo de antigüedad con pd.cut\n")
code("# Ejercicio 5 (desafío): satisfecho_v2 respetando los NaN\n")

md(r"""> En la **Sesión 8** cerramos el bloque de limpieza con el **texto**: estandarizar la región (ese desastre de mayúsculas y espacios), ordenar la variable ciudad y dar los primeros pasos con respuestas abiertas.""")

notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.x"}},"nbformat":4,"nbformat_minor":5}
with open("curso/07 - Sesion 7 - Recodificar variables.ipynb","w",encoding="utf-8") as f:
    json.dump(notebook,f,ensure_ascii=False,indent=1)
print("S7 OK", len(cells), "celdas")
