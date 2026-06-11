# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 2 (.ipynb) sin dependencias externas."""
import json

cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

md(r"""# Sesión 2 — Seleccionar y filtrar: apuntar a la variable y al caso correcto

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Quedarnos con **una o varias columnas** (las variables que nos interesan).
- Entender `loc` e `iloc` para apuntar a filas y columnas.
- **Filtrar casos** según condiciones (el "filtro de casos" de SPSS).
- Combinar condiciones para llegar a un subgrupo exacto (ej. *mujeres mayores de 30 de la Región Metropolitana*).

> **Antes de empezar:** recuerda que las celdas se ejecutan de arriba hacia abajo con `Shift`+`Enter`. Si abriste el notebook recién, ejecuta primero la celda que carga los datos (la de más abajo) antes de probar las demás.

---""")

md(r"""## 0. Recordatorio: cargar la base

Como es un notebook nuevo, partimos cargando otra vez la base. Esto lo haremos siempre al inicio de cada sesión.""")

code(r"""import pandas as pd

datos = pd.read_csv("datos/encuesta_satisfaccion.csv", sep=";", decimal=",")
datos.head()""")

md(r"""## 1. ¿Por qué seleccionar y filtrar?

Casi nunca trabajamos con *toda* la base de golpe. Lo normal es:
- **"Muéstrame solo la satisfacción general"** → seleccionar una **columna** (una variable).
- **"Quiero analizar solo a las mujeres"** → filtrar **filas** (casos) según una condición.

Estas dos operaciones —elegir columnas y filtrar filas— son la base de *todo* lo que viene después. Son el equivalente exacto de, en SPSS, *elegir variables* y usar *Datos → Seleccionar casos*.

---

## 2. Seleccionar columnas

### Una sola columna
Ya lo vimos en la Sesión 1: escribimos el nombre de la columna entre corchetes.""")

code(r"""datos["P5_sat_general"].head()""")

md(r"""Una sola columna es una **Series** (una variable suelta, con su índice). Compruébalo:""")

code(r"""type(datos["P5_sat_general"])""")

md(r"""### Varias columnas a la vez
Para elegir **varias** columnas, le pasamos una **lista** de nombres. Por eso aparecen **corchetes dobles** `[[ ]]`: los de afuera son "selecciona", los de adentro son la lista de columnas.""")

code(r"""datos[["sexo", "edad", "P5_sat_general"]].head()""")

md(r"""> 💡 **Truco para recordar los corchetes dobles:** los de afuera significan "quiero seleccionar de `datos`"; los de adentro son la **lista** `["sexo", "edad", ...]`. Una columna → corchetes simples (Series). Varias columnas → corchetes dobles (DataFrame).

Podemos guardar esa selección en una variable nueva para trabajar más cómodas:""")

code(r"""# Una mini-base solo con lo sociodemográfico
sociodem = datos[["sexo", "edad", "region", "producto"]]
sociodem.head()""")

md(r"""## 3. `loc` e `iloc`: apuntar a filas y columnas con precisión

A veces no queremos toda una columna, sino una **porción** (ciertas filas y ciertas columnas). Para eso pandas tiene dos herramientas que conviene no confundir:

| Herramienta | Cómo apunta | Regla mnemotécnica |
|---|---|---|
| `loc` | por **etiqueta** (el nombre/índice) | **l** de *label* (etiqueta) |
| `iloc` | por **posición** (el número de orden) | **i** de *index* numérico |

### `iloc` — por posición (como coordenadas de fila/columna)
Se lee así: `datos.iloc[filas, columnas]`. Recuerda que **se cuenta desde 0**.""")

code(r"""# La primera fila, primera columna (esquina superior izquierda)
datos.iloc[0, 0]""")

code(r"""# Las primeras 5 filas y las primeras 3 columnas
datos.iloc[0:5, 0:3]""")

md(r"""### `loc` — por etiqueta (usando nombres de columna)
Con `loc` apuntamos usando los **nombres** de las columnas, que es mucho más legible.""")

code(r"""# Filas de la 0 a la 4, eligiendo columnas POR SU NOMBRE
datos.loc[0:4, ["sexo", "edad", "P5_sat_general"]]""")

md(r"""> En la práctica diaria usarás **`loc` con nombres** casi siempre (es más claro) y `iloc` solo cuando necesites posiciones exactas. No te preocupes por dominar ambas hoy: con saber que existen y para qué sirven, basta.

---

## 4. Filtrar casos: el corazón de la sesión

Aquí está lo más útil. Queremos quedarnos solo con las filas que **cumplen una condición**. Por ejemplo: *"solo las personas mayores de 60 años"*.

El truco tiene dos pasos. Primero, una condición devuelve una columna de **Verdadero/Falso** (una por cada fila):""")

code(r"""# ¿Es la persona mayor de 60? -> True/False para cada fila
(datos["edad"] > 60).head()""")

md(r"""Segundo, metemos esa condición **dentro de los corchetes** de la base. pandas se queda solo con las filas donde el resultado fue `True`:""")

code(r"""mayores_60 = datos[datos["edad"] > 60]
mayores_60.head()""")

code(r"""# ¿Cuántas personas cumplen la condición? (filas, columnas)
mayores_60.shape""")

md(r"""¡Eso es filtrar! Lo mismo que *Seleccionar casos* en SPSS, pero en una línea y reproducible.

### ⚠️ Un detalle real: los códigos especiales se cuelan
Nuestra base tiene un código `999` en `edad` para "sin dato". Como `999` también es "mayor de 60"... ¡esas personas se colarían en el filtro! Mira:""")

code(r"""# Los valores más altos de edad: aparece el 999 (sin dato)
datos["edad"].sort_values(ascending=False).head()""")

md(r"""Por eso, en datos reales conviene **acotar el filtro por ambos lados**. Pedimos mayores de 60 *pero* con una edad razonable (menor a 120):""")

code(r"""mayores_60_ok = datos[(datos["edad"] > 60) & (datos["edad"] < 120)]
mayores_60_ok.shape""")

md(r"""> 🧹 Tranquila: limpiar estos códigos `999`/`99` de una vez (en lugar de esquivarlos a mano) es justo lo que veremos en la **Sesión 6 (valores perdidos)**. Por ahora solo nota que existen y por qué importan.

---

## 5. Combinar condiciones: `&` (y), `|` (o)

Para llegar a un subgrupo más específico, combinamos condiciones:
- `&` significa **y** (deben cumplirse *ambas*).
- `|` significa **o** (basta con *una*).

**Regla de oro:** cada condición va **entre paréntesis**. Es el error más común al empezar.""")

code(r"""# Mujeres (sexo = 2) Y mayores de 30
filtro = (datos["sexo"] == 2) & (datos["edad"] > 30) & (datos["edad"] < 120)
mujeres_30 = datos[filtro]
mujeres_30.shape""")

md(r"""Fíjate que guardamos la condición en una variable `filtro` y luego la usamos. Eso hace el código más legible cuando hay varias condiciones.

Un ejemplo con `|` (o): clientes que tienen Cuenta Corriente **o** Tarjeta de Crédito.""")

code(r"""producto_objetivo = (datos["producto"] == "Cuenta Corriente") | (datos["producto"] == "Tarjeta de Credito")
datos[producto_objetivo].shape""")

md(r"""## 6. Manos a la obra: *mujeres mayores de 30 de la Región Metropolitana*

Este es el objetivo de la sesión. Pero hay una trampa real: la variable `region` viene **sucia** (mayúsculas y espacios distintos), tal como llega del terreno. Veámoslo:""")

code(r"""datos["region"].value_counts()""")

md(r"""¿Ves el problema? "Metropolitana", "METROPOLITANA", "  Metropolitana", "Metropolitana " aparecen como categorías distintas, ¡cuando son la misma! Si filtráramos solo por `== "Metropolitana"`, dejaríamos gente afuera.

**Solución del mundo real:** emparejamos el texto quitándole espacios (`.str.strip()`) y pasándolo a minúsculas (`.str.lower()`) antes de comparar. Así "  METROPOLITANA " y "metropolitana" se vuelven iguales.""")

code(r"""region_limpia = datos["region"].str.strip().str.lower()

filtro_final = (
    (datos["sexo"] == 2) &              # mujeres
    (datos["edad"] > 30) &              # mayores de 30
    (datos["edad"] < 120) &             # ...con edad válida (esquiva el 999)
    (region_limpia == "metropolitana")  # de la RM, sin importar mayúsculas/espacios
)

mujeres_rm = datos[filtro_final]
print("Casos que cumplen todo:", mujeres_rm.shape[0])
mujeres_rm[["sexo", "edad", "region", "P5_sat_general"]].head()""")

md(r"""¡Listo! Aislamos exactamente el subgrupo que queríamos, sorteando la suciedad de los datos.

> 🧹 Igual que con el `999`, dejar la columna `region` limpia de una vez (en vez de arreglarla cada vez que filtramos) es lo que haremos en la **Sesión 8 (limpiar texto)**. Hoy lo importante es que entiendas el mecanismo de filtrar y combinar condiciones.

---

## 7. Conexión con SPSS

| Lo que hacías en SPSS | Lo que hicimos hoy en Python |
|---|---|
| Elegir variables para un análisis | `datos[["sexo", "edad"]]` |
| Datos → Seleccionar casos → "Si se cumple condición" | `datos[datos["edad"] > 60]` |
| Condición con varios criterios (Y / O) | `&` (y) y `|` (o), cada condición entre paréntesis |
| Guardar el subconjunto en otro archivo | Guardarlo en una variable: `mujeres_rm = datos[...]` |

---

## 8. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio:** haz clic en ella, escribe tu respuesta y ejecútala con `Shift`+`Enter`.

1. Selecciona solo las columnas `producto` y `antiguedad_anios` y muestra las primeras filas.
2. Filtra a las personas con **Crédito de Consumo** (`producto == "Credito de Consumo"`). ¿Cuántas son?
3. Filtra a quienes dieron **nota 9 o 10** en la pregunta NPS (`P6_nps`). *(Pista: usa `>=`.)*
4. Filtra a los **hombres** (`sexo == 1`) con **5 o más años de antigüedad**. ¿Cuántos casos hay?
5. **Desafío:** filtra a las personas de la región de **Valparaíso** (recuerda que viene sucia: usa `.str.strip().str.lower()` y compara con `"valparaiso"`).""")

code(r"""# Ejercicio 1: columnas 'producto' y 'antiguedad_anios'
""")

code(r"""# Ejercicio 2: personas con Crédito de Consumo (¿cuántas?)
""")

code(r"""# Ejercicio 3: NPS de 9 o 10
""")

code(r"""# Ejercicio 4: hombres con 5 o más años de antigüedad (¿cuántos?)
""")

code(r"""# Ejercicio 5 (desafío): personas de la región de Valparaíso
""")

md(r"""> En la **Sesión 3** daremos el salto a cargar datos de verdad en cualquier formato: CSV con sus complicaciones, Excel y —muy importante para nosotras— archivos **`.sav` de SPSS** con sus etiquetas.""")

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.x"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open("curso/02 - Sesion 2 - Seleccionar y filtrar.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("Notebook creado con", len(cells), "celdas")
