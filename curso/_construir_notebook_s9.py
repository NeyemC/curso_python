# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 9 (.ipynb)."""
import json
cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

PREP = r'''import pandas as pd
import numpy as np

datos = pd.read_csv("datos/encuesta_satisfaccion.csv", sep=";", decimal=",")

# --- Limpieza (lo aprendido en el Bloque 3) ---
datos["edad"] = datos["edad"].replace(999, np.nan)
datos["sexo"] = datos["sexo"].replace(9, np.nan)
bateria = ["P1_sat_atencion", "P2_sat_tiempos", "P3_sat_app",
           "P4_sat_sucursal", "P5_sat_general"]
datos[bateria] = datos[bateria].replace(99, np.nan)
datos["P6_nps"] = datos["P6_nps"].replace(99, np.nan)
datos["region"] = datos["region"].str.strip().str.title()

# --- Recodificación ---
datos["sat_general"] = datos["P5_sat_general"]           # nombre corto y legible
datos["sexo_txt"]  = datos["sexo"].map({1: "Hombre", 2: "Mujer"})
datos["tramo_edad"] = pd.cut(datos["edad"], bins=[17, 29, 44, 59, 120],
                             labels=["18-29", "30-44", "45-59", "60+"])
datos["nps_grupo"] = pd.cut(datos["P6_nps"], bins=[-1, 6, 8, 10],
                            labels=["Detractor", "Pasivo", "Promotor"])

datos.head(3)'''

md(r"""# Sesión 9 — Frecuencias y descriptivos: el análisis univariado

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Producir **tablas de frecuencia** con conteo y **porcentaje**.
- Calcular **descriptivos** de variables numéricas (media, mediana, desviación).
- Presentar las frecuencias de forma **ordenada y lista para el informe**.

> 📊 Las frecuencias son, casi siempre, el **primer entregable** de un estudio: "¿qué porcentaje respondió cada cosa?". Hoy aprendemos a producirlas bien.

---""")

md(r"""## 0. Preparamos la base

Desde aquí en adelante empezaremos cada sesión de análisis dejando la base **limpia y recodificada**, aplicando todo lo del Bloque 3. Ejecuta esta celda primero.""")
code(PREP)

md(r"""## 1. Frecuencias con `value_counts()`

Ya lo conocemos de sesiones anteriores. Para una variable categórica, cuenta cuántas veces aparece cada valor.""")
code(r"""datos["sexo_txt"].value_counts()""")

md(r"""### Frecuencias en porcentaje
Con `normalize=True` obtenemos **proporciones** (que multiplicamos por 100 para tener %).""")
code(r"""(datos["sexo_txt"].value_counts(normalize=True) * 100).round(1)""")

md(r"""## 2. Una tabla de frecuencias presentable (conteo + %)

En un informe queremos **las dos cosas juntas**: el `n` y el `%`. Las combinamos en una tabla con `pd.DataFrame`.""")
code(r"""conteo = datos["nps_grupo"].value_counts()
porcentaje = (datos["nps_grupo"].value_counts(normalize=True) * 100).round(1)

tabla = pd.DataFrame({"n": conteo, "%": porcentaje})
tabla""")

md(r"""¡Esa tabla ya se puede pegar en un informe! Muestra, para cada grupo NPS, cuántos casos hay y qué porcentaje representan.

> 💡 **Sobre los porcentajes y los perdidos:** por defecto, `value_counts` **ignora los `NaN`**, así que el % es "sobre los que respondieron" (porcentaje válido). Si quisieras incluir los perdidos como una categoría, agrega `dropna=False`.""")
code(r"""# Comparación: incluyendo los que NO respondieron NPS
datos["nps_grupo"].value_counts(dropna=False)""")

md(r"""## 3. Descriptivos de variables numéricas

Para variables numéricas (edad, satisfacción como escala, antigüedad) el resumen son los **estadísticos**: media, mediana, desviación, etc.""")
code(r"""# Un resumen completo de la satisfacción general (escala 1-5)
datos["sat_general"].describe()""")

md(r"""O podemos pedir estadísticos puntuales, que es lo habitual en un informe:""")
code(r"""print("Satisfacción general (escala 1 a 5)")
print("  Promedio :", round(datos["sat_general"].mean(), 2))
print("  Mediana  :", datos["sat_general"].median())
print("  Desv. típ:", round(datos["sat_general"].std(), 2))
print("  N válido :", datos["sat_general"].notnull().sum())""")

md(r"""> 🧭 Recuerda: como ya limpiamos los `99`, estos promedios son **correctos** (ignoran a quienes no respondieron). Si no hubiéramos hecho el Bloque 3, estarían inflados.

## 4. Frecuencias de una variable numérica agrupada

A veces conviene ver una variable de escala **como frecuencias**. Por ejemplo, el reparto de notas de satisfacción, ordenado de 1 a 5:""")
code(r"""notas = datos["sat_general"].value_counts().sort_index()
notas_pct = (datos["sat_general"].value_counts(normalize=True) * 100).round(1).sort_index()
pd.DataFrame({"n": notas, "%": notas_pct})""")

md(r"""## 5. Manos a la obra: las frecuencias del estudio

Producimos de un tirón las frecuencias de las principales variables de perfil, tal como abrirían el informe de resultados.""")
code(r"""for var in ["sexo_txt", "tramo_edad", "region"]:
    print("=" * 40)
    print("Variable:", var)
    tab = pd.DataFrame({
        "n": datos[var].value_counts(),
        "%": (datos[var].value_counts(normalize=True) * 100).round(1)
    })
    print(tab)
    print()""")

md(r"""> Ese `for` que repite la misma tabla para varias variables es un anticipo de la **Sesión 15 (automatizar)**, donde aprenderemos a empaquetar esto en una función reutilizable.

## 6. Conexión con SPSS

| En SPSS | Hoy en Python |
|---|---|
| Analizar → Frecuencias | `datos["var"].value_counts()` |
| Frecuencias con porcentaje válido | `value_counts(normalize=True) * 100` |
| Analizar → Descriptivos / Explorar | `datos["var"].describe()` |
| Media, mediana, desviación | `.mean()`, `.median()`, `.std()` |

---

## 7. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio.** *(Ejecuta primero la celda de preparación.)*

1. Haz la tabla de frecuencias (n y %) de la variable `producto`.
2. ¿Cuál es la **satisfacción promedio** con la app (`P3_sat_app`)? ¿Y con la sucursal (`P4_sat_sucursal`)?
3. Muestra la mediana y la desviación de `antiguedad_anios`.
4. Haz la tabla de frecuencias de `nps_grupo` **incluyendo** los perdidos (`dropna=False`). ¿Qué porcentaje del total no contestó?
5. **Desafío:** calcula qué porcentaje de la muestra son **Promotores** (grupo NPS). *(Pista: usa `value_counts(normalize=True)` y quédate con "Promotor".)*""")
code("# Ejercicio 1: frecuencias de producto\n")
code("# Ejercicio 2: satisfacción promedio de app y sucursal\n")
code("# Ejercicio 3: mediana y desviación de antiguedad_anios\n")
code("# Ejercicio 4: frecuencias de nps_grupo con dropna=False\n")
code("# Ejercicio 5 (desafío): % de Promotores\n")

md(r"""> En la **Sesión 10** damos el salto al **análisis bivariado**: los **cruces** (tablas de contingencia). "¿La satisfacción cambia según el segmento?" es *la* pregunta de la consultoría, y la responderemos con `pd.crosstab()`.""")

notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.x"}},"nbformat":4,"nbformat_minor":5}
with open("curso/09 - Sesion 9 - Frecuencias y descriptivos.ipynb","w",encoding="utf-8") as f:
    json.dump(notebook,f,ensure_ascii=False,indent=1)
print("S9 OK", len(cells), "celdas")
