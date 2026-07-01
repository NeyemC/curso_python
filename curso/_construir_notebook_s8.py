# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 8 (.ipynb)."""
import json
cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

md(r"""# Sesión 8 — Limpiar texto y respuestas abiertas

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Usar los **métodos `.str`** para estandarizar texto (mayúsculas, espacios, reemplazos).
- Ordenar de una vez ese desastre de la variable **`region`**.
- Dar los **primeros pasos** con respuestas abiertas: buscar, contar y categorizar.

> Casi todo estudio trae una pregunta abierta y variables de texto escritas a mano. Estandarizarlas es lo que permite, después, contarlas y cruzarlas bien.

---""")

md(r"""## 0. Cargamos la base""")
code(r"""import pandas as pd
import numpy as np

datos = pd.read_csv("datos/encuesta_satisfaccion.csv", sep=";", decimal=",")
datos[["region", "ciudad", "comentario"]].head()""")

md(r"""## 1. El problema del texto sucio

Recordemos el diagnóstico de la Sesión 4: la región viene escrita de mil formas.""")
code(r"""datos["region"].value_counts()""")

md(r"""`Metropolitana`, `METROPOLITANA`, `  Metropolitana`, `metropolitana`... son **la misma** región, pero el computador las cuenta por separado. Si hiciéramos una tabla así, saldría partida en pedazos y los porcentajes estarían mal.

## 2. Los métodos `.str`: nuestra caja de herramientas de texto

pandas trae un conjunto de funciones de texto que se aplican a toda la columna con `.str`. Las más útiles para limpiar:

| Método | Qué hace | Ejemplo |
|---|---|---|
| `.str.strip()` | quita espacios al inicio/final | `"  RM " → "RM"` |
| `.str.lower()` | todo a minúsculas | `"METRO" → "metro"` |
| `.str.upper()` | todo a mayúsculas | `"metro" → "METRO"` |
| `.str.title()` | Mayúscula Inicial En Cada Palabra | `"la serena" → "La Serena"` |
| `.str.replace(a, b)` | reemplaza texto | `"S. A." → "SA"` |
| `.str.contains(x)` | ¿contiene x? (Verdadero/Falso) | buscar palabras |

Probémoslos sobre la región. Primero, quitar espacios y unificar mayúsculas:""")
code(r"""# Paso a paso: primero sin espacios, luego con formato de título
ejemplo = datos["region"].str.strip().str.title()
ejemplo.value_counts()""")

md(r"""¡Enorme mejora! Con solo `.strip()` (quitar espacios) y `.title()` (Mayúscula Inicial), las 20+ variantes colapsaron a las 5 regiones reales. Eso es estandarizar.

## 3. Estandarizar la región de verdad

Guardamos la versión limpia en la propia columna (ahora sí queremos dejarla arreglada):""")
code(r"""datos["region"] = datos["region"].str.strip().str.title()
datos["region"].value_counts()""")

md(r"""Ahora `region` está limpia y lista para tablas y cruces. **Este es el momento** que anticipábamos en las Sesiones 2 y 4: ya no hay que esquivar la suciedad al filtrar, porque la arreglamos en la fuente.

## 4. Estandarizar la ciudad (más sucia aún)

La ciudad es texto abierto y trae más variantes. Apliquémosle el mismo tratamiento base:""")
code(r"""datos["ciudad"] = datos["ciudad"].str.strip().str.title()
datos["ciudad"].value_counts().head(12)""")

md(r"""Fíjate que `.title()` no lo arregla *todo*: por ejemplo, "Stgo" y "Santiago" siguen siendo distintos, o "Valpo" y "Valparaiso". Esos casos de **sinónimos/abreviaturas** se resuelven con un diccionario de reemplazos, tal como recodificamos en la Sesión 7:""")
code(r"""datos["ciudad"] = datos["ciudad"].replace({
    "Stgo":  "Santiago",
    "Valpo": "Valparaiso",
})
datos["ciudad"].value_counts().head(12)""")

md(r"""> 🧭 **Regla práctica:** primero **normaliza el formato** (`strip` + `lower`/`title`); recién después arregla **sinónimos** puntuales con `replace`. En ese orden ahorras muchísimo trabajo.

## 5. Primeros pasos con respuestas abiertas

La columna `comentario` es una pregunta abierta (mucha gente la dejó vacía = `NaN`). Veamos qué se puede hacer sin técnicas complejas.

**¿Cuántos dejaron comentario?**""")
code(r"""print("Total de casos:", len(datos))
print("Con comentario:", datos["comentario"].notnull().sum())
print("Sin comentario (NaN):", datos["comentario"].isnull().sum())""")

md(r"""**Buscar un tema con `.str.contains()`**: por ejemplo, ¿cuántos comentarios mencionan la palabra "espera" o "demora"? Muy útil para una primera categorización manual.""")
code(r"""# na=False evita errores con los comentarios vacíos (NaN)
menciona_espera = datos["comentario"].str.contains("espera|demor", case=False, na=False)
print("Comentarios que mencionan espera/demora:", menciona_espera.sum())

datos.loc[menciona_espera, "comentario"].head()""")

md(r"""> 🔎 Ese `"espera|demor"` es una **expresión regular** sencilla: la barra `|` significa "o". Con eso capturamos "espera", "esperar", "demora", "demoraron"... No hace falta dominar expresiones regulares hoy; basta saber que existen para buscar temas.

**Categorizar a mano con `np.where`**: podemos crear una variable de tema a partir de la búsqueda.""")
code(r"""datos["tema_espera"] = np.where(menciona_espera, "Menciona espera", "No menciona")
datos["tema_espera"].value_counts()""")

md(r"""## 6. Manos a la obra: la columna `ciudad`, limpia

Ya recorrimos el flujo completo sobre `ciudad`: normalizar formato y arreglar abreviaturas. El resultado es una variable lista para analizar. Ese es exactamente el trabajo que, en un estudio real, te ahorra horas de cuadrar tablas a mano.

## 7. Conexión con SPSS

| En SPSS | Hoy en Python |
|---|---|
| Limpiar cadenas (funciones de texto / sintaxis) | métodos `.str....` |
| `LOWER`, `UPCASE`, `LTRIM`/`RTRIM` | `.str.lower()`, `.str.upper()`, `.str.strip()` |
| Recodificar cadenas (unificar categorías) | `.str.title()` + `.replace({...})` |
| Buscar una subcadena | `.str.contains(...)` |

---

## 8. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio.** *(Ejecuta primero las celdas de arriba.)*

1. Comprueba con `value_counts()` que `region` ya quedó en 5 categorías limpias.
2. Crea una variable `region_mayus` que tenga la región TODA EN MAYÚSCULAS. *(Pista: `.str.upper()`.)*
3. ¿Cuántos comentarios mencionan la palabra "app" o "web"? *(Pista: `.str.contains("app|web", case=False, na=False)`.)*
4. Crea una variable `largo_comentario` con la cantidad de caracteres de cada comentario. *(Pista: `.str.len()`.)*
5. **Desafío:** crea una variable `tema` que diga `"Tiempos"` si el comentario menciona espera/demora, `"Digital"` si menciona app/web, y `"Otro"` en el resto. *(Pista: encadena dos `np.where`.)*""")
code("# Ejercicio 1: value_counts de region\n")
code("# Ejercicio 2: region_mayus con .str.upper()\n")
code("# Ejercicio 3: comentarios que mencionan app/web\n")
code("# Ejercicio 4: largo_comentario con .str.len()\n")
code("# Ejercicio 5 (desafío): variable 'tema' con dos np.where anidados\n")

md(r"""> 🎉 **¡Cerramos el Bloque 3!** Ya sabes cargar, diagnosticar, limpiar y recodificar una encuesta. En la **Sesión 9** empieza lo más esperado: el **análisis**. Arrancamos con las **frecuencias y descriptivos** — el primer entregable de casi todo estudio.""")

notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.x"}},"nbformat":4,"nbformat_minor":5}
with open("curso/08 - Sesion 8 - Limpiar texto y respuestas abiertas.ipynb","w",encoding="utf-8") as f:
    json.dump(notebook,f,ensure_ascii=False,indent=1)
print("S8 OK", len(cells), "celdas")
