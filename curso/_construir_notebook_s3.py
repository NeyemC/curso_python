# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 3 (.ipynb) sin dependencias externas."""
import json

cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

md(r"""# Sesión 3 — Cargar datos de verdad: CSV, Excel y archivos SPSS (.sav)

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Cargar un **CSV** con sus complicaciones reales: separador, decimales con coma, acentos.
- Abrir archivos **Excel** (`.xlsx`), eligiendo la hoja.
- Leer archivos **`.sav` de SPSS** y —lo más importante— **recuperar sus etiquetas** de variable y de valor.
- Entender que, sea cual sea el formato, todo termina en el mismo objeto: un **DataFrame**.

> 💡 Esta sesión es "el puente" entre el mundo SPSS/Excel en el que trabajamos y el mundo Python. Lo que aprendamos aquí lo usarás al inicio de **todos** tus estudios.

---""")

md(r"""## 1. ¿Por qué dedicarle una sesión entera a "abrir un archivo"?

Porque en la práctica, **abrir bien los datos es la mitad de los problemas**. Los datos llegan:
- en **CSV** exportados de distintos sistemas (cada uno con su separador y formato de números),
- en **Excel**, a veces con varias hojas,
- en **`.sav` de SPSS**, con sus etiquetas que no queremos perder.

Si la carga queda mal, *todo lo demás sale mal*. Así que vale la pena hacerlo bien una vez.

Partimos importando pandas, como siempre:""")

code(r"""import pandas as pd""")

md(r"""## 2. CSV: el formato más común (y más traicionero)

Un CSV es un archivo de texto donde los valores van separados por un carácter. El problema: **no todos usan el mismo**. En países de habla hispana es muy frecuente que:
- el separador de columnas sea **`;`** (punto y coma), no la coma,
- el separador decimal sea la **coma** (`3,5` en vez de `3.5`).

Veamos qué pasa si abrimos nuestro CSV **sin avisarle a pandas** de esto:""")

code(r"""# Carga "ingenua": pandas asume separador = coma
mal = pd.read_csv("datos/encuesta_satisfaccion.csv")
mal.shape""")

md(r"""¿Ves el problema? Dice que hay **una sola columna**. Como nuestro archivo usa `;`, pandas no encontró comas para separar y metió todo en una sola columna. Míralo:""")

code(r"""mal.head(2)""")

md(r"""Todo quedó apretujado. Ahora carguémoslo **bien**, indicándole el separador y el decimal correctos:""")

code(r"""datos = pd.read_csv(
    "datos/encuesta_satisfaccion.csv",
    sep=";",        # las columnas van separadas por punto y coma
    decimal=","     # los decimales usan coma (ej. el ponderador: 1,19)
)
datos.head()""")

code(r"""# Ahora sí: 800 filas y 15 columnas bien separadas
datos.shape""")

md(r"""### Los parámetros de `read_csv` que más usarás

| Parámetro | Para qué sirve | Ejemplo |
|---|---|---|
| `sep` | separador de columnas | `sep=";"` |
| `decimal` | separador decimal | `decimal=","` |
| `encoding` | codificación (acentos y ñ) | `encoding="latin-1"` |
| `na_values` | qué tratar como vacío | `na_values=[99, 999]` |

> 🔤 **Sobre `encoding`:** si al abrir un archivo ves los acentos rotos (`Valpara\xedso`, `Concepci贸n`), casi siempre se arregla agregando `encoding="latin-1"` (o `encoding="utf-8"`). Es el problema #1 con archivos que vienen de sistemas antiguos.

> 🧹 Fíjate en `na_values`: ¡desde la carga podríamos decirle que `99` y `999` son "vacío"! Lo veremos a fondo en la Sesión 6; por ahora solo nota que existe.

---

## 3. Excel (.xlsx)

Muchas veces el cliente nos manda directamente un Excel. Se abre con `read_excel`. Si el libro tiene varias hojas, indicamos cuál con `sheet_name`.""")

code(r"""datos_excel = pd.read_excel(
    "datos/encuesta_satisfaccion.xlsx",
    sheet_name="Respuestas"   # el nombre de la pestaña
)
datos_excel.head()""")

md(r"""> 💡 Si no sabes cómo se llaman las hojas, puedes abrir el archivo así: `libro = pd.ExcelFile("archivo.xlsx")` y luego mirar `libro.sheet_names`.

Y para **exportar** a Excel (lo veremos en detalle en la Sesión 16) la idea es simétrica: `datos.to_excel("salida.xlsx", index=False)`.

---

## 4. SPSS (.sav): ¡el puente con nuestro mundo!

Aquí está lo más valioso para nosotras. pandas por sí solo no lee `.sav`, así que usamos una librería llamada **`pyreadstat`**.

Probablemente no la tengas instalada (no viene con Anaconda). Se instala **una sola vez** ejecutando la siguiente celda (luego puedes borrarla o dejarla comentada):""")

code(r"""%pip install pyreadstat""")

md(r"""Ahora la importamos y leemos el archivo. Ojo a algo nuevo: `read_sav` devuelve **dos cosas** a la vez — los datos *y* los metadatos (las etiquetas). Por eso escribimos dos nombres a la izquierda: `datos_sav, meta`.""")

code(r"""import pyreadstat

datos_sav, meta = pyreadstat.read_sav("datos/encuesta_satisfaccion.sav")
datos_sav.head()""")

md(r"""Los datos se ven igual que antes. Pero la magia está en `meta`, que guarda las **etiquetas** que pusimos en SPSS.

### Etiquetas de VARIABLE (qué mide cada columna)""")

code(r"""meta.column_names_to_labels""")

md(r"""¡Ahí están las descripciones! `P5_sat_general` → *"P5. Satisfacción general con el banco"*. Esto es lo que en SPSS ves en la columna "Etiqueta" de la Vista de Variables.

### Etiquetas de VALOR (qué significa cada código)""")

code(r"""meta.variable_value_labels""")

md(r"""Estas son las *value labels*: para `sexo`, `1 = "Hombre"`, `2 = "Mujer"`, `9 = "Sin dato"`. Justo los diccionarios que armamos a mano en la Sesión 1... ¡pero aquí vienen incluidos en el archivo!

### Truco: cargar los datos ya "traducidos"
`pyreadstat` puede reemplazar automáticamente los códigos por sus etiquetas de texto al cargar, con `apply_value_formats=True`:""")

code(r"""datos_etiquetado, meta = pyreadstat.read_sav(
    "datos/encuesta_satisfaccion.sav",
    apply_value_formats=True
)
datos_etiquetado[["sexo", "P5_sat_general", "P6_nps"]].head()""")

md(r"""¡Mira la diferencia! Ahora `sexo` dice "Hombre"/"Mujer" y la satisfacción dice "Satisfecho"/"Muy satisfecho" en vez de números. Según lo que necesites harás una u otra:
- **con códigos** (números) → mejor para calcular promedios, índices, correlaciones.
- **con etiquetas** (texto) → mejor para tablas y gráficos legibles.

Aprenderemos a movernos entre ambos mundos en la sesión de recodificación.

---

## 5. Manos a la obra: la misma encuesta, tres formatos

La gracia: **no importa el formato de entrada, siempre llegamos a un DataFrame**. Comprobemos que las tres cargas tienen el mismo tamaño:""")

code(r"""print("CSV  :", datos.shape)
print("Excel:", datos_excel.shape)
print("SPSS :", datos_sav.shape)""")

md(r"""Las tres dicen `(800, 15)`. Son la misma encuesta. A partir de aquí, todo lo que aprendimos en las Sesiones 1 y 2 (mirar, seleccionar, filtrar) funciona **igual**, sin importar de dónde vinieron los datos.""")

code(r"""# Por ejemplo, filtrar funciona idéntico sobre el DataFrame venga de donde venga
datos_excel[datos_excel["edad"] < 120]["edad"].mean()""")

md(r"""## 6. Conexión con SPSS

| Lo que hacías en SPSS | Lo que hicimos hoy en Python |
|---|---|
| Abrir / Importar un `.sav` | `pyreadstat.read_sav(...)` |
| Importar un texto/CSV con un asistente | `pd.read_csv(...)` con `sep`, `decimal` |
| Importar un Excel | `pd.read_excel(...)` |
| Columna "Etiqueta" de la Vista de Variables | `meta.column_names_to_labels` |
| Etiquetas de valor (1 = "Hombre") | `meta.variable_value_labels` |
| Ver los datos con etiquetas en vez de códigos | `apply_value_formats=True` |

---

## 7. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio:** haz clic en ella, escribe tu respuesta y ejecútala con `Shift`+`Enter`.

1. Carga el CSV de nuevo, pero esta vez agregándole el parámetro `na_values=[99, 999]`. Guárdalo en una variable `datos_limpio` y mira su `.head()`. ¿Notas algún `NaN` donde antes había 99 o 999?
2. Del archivo `.sav`, muestra solo la **etiqueta de variable** de la columna `P6_nps`. *(Pista: `meta.column_names_to_labels["P6_nps"]`.)*
3. Del archivo `.sav`, muestra las **etiquetas de valor** de la variable `P1_sat_atencion`.
4. Carga el Excel y calcula cuántas filas tiene (`.shape`).
5. **Desafío:** carga el `.sav` con `apply_value_formats=True` y muestra las primeras filas de las columnas `region` y `producto`.""")

code(r"""# Ejercicio 1: cargar el CSV con na_values=[99, 999]
""")

code(r"""# Ejercicio 2: etiqueta de variable de P6_nps
""")

code(r"""# Ejercicio 3: etiquetas de valor de P1_sat_atencion
""")

code(r"""# Ejercicio 4: filas del Excel
""")

code(r"""# Ejercicio 5 (desafío): .sav etiquetado, columnas region y producto
""")

md(r"""> En la **Sesión 4** haremos el "informe de salud" de una base recién llegada: cuántos casos, qué tipos de variable, cuántos vacíos y dónde están las rarezas. Es el primer paso antes de analizar cualquier estudio.""")

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.x"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open("curso/03 - Sesion 3 - Cargar datos (CSV, Excel, SPSS).ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("Notebook creado con", len(cells), "celdas")
