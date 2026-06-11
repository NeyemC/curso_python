# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 1 (.ipynb) sin dependencias externas."""
import json

cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

md(r"""# Sesión 1 — "Hola, Python": el entorno, los datos y el DataFrame

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Perderle el miedo a Jupyter: entender qué es una *celda* y cómo se ejecuta.
- Conocer los tipos de datos básicos pensándolos como *variables de encuesta*.
- Abrir nuestra primera base de datos real y mirarla por dentro.
- Construir el "diccionario de etiquetas" de una pregunta (las *value labels* de SPSS).

> **Cómo trabajamos:** cada vez que veas una celda gris con código, ponte sobre ella y presiona **`Shift` + `Enter`** para ejecutarla. Vamos todas a la par. No hay que memorizar nada: hay que *entender para qué sirve*.

---""")

md(r"""## 1. ¿Qué es esto? Python y Jupyter en 2 minutos

- **Python** es el lenguaje en el que le damos instrucciones al computador.
- **Jupyter Notebook** es este cuaderno: mezcla *texto* (como el que estás leyendo) con *celdas de código* que se pueden ejecutar y muestran su resultado abajo.

Piénsalo como una hoja de cálculo conversada: en vez de fórmulas escondidas en celdas, escribimos instrucciones claras, una tras otra, y vamos viendo el resultado.

**La regla de oro:** las celdas se ejecutan **de arriba hacia abajo**. El orden importa, porque lo que escribimos arriba queda "en memoria" para usarlo abajo.

Probemos. Ejecuta la siguiente celda (`Shift`+`Enter`):""")

code(r"""print("¡Hola! Si ves este mensaje abajo, Jupyter está funcionando.")""")

md(r"""La celda de arriba *imprimió* un mensaje. `print()` simplemente muestra en pantalla lo que le pongamos entre paréntesis.

Una celda también puede funcionar como **calculadora**. El resultado de la última línea se muestra solo, sin necesidad de `print`:""")

code(r"""2 + 2""")

code(r"""# Todo lo que va después de un # es un COMENTARIO: Python lo ignora.
# Sirve para dejarnos notas a nosotras mismas.
1250 * 12   # ventas mensuales por 12 meses""")

md(r"""## 2. Variables: ponerle nombre a las cosas

Una **variable** es simplemente un nombre que le ponemos a un valor para reutilizarlo. Igual que cuando en Excel nombras una celda o un rango.

Se usa el signo `=` : *"guarda esto con este nombre"*.""")

code(r"""tamano_muestra = 800
margen_error = 3.5

print("La muestra es de", tamano_muestra, "casos")
print("El margen de error es de", margen_error, "%")""")

md(r"""Una vez creada, la variable queda disponible para las celdas siguientes. Podemos operar con ella:""")

code(r"""# ¿Cuántos casos representa cada punto porcentual, aprox?
tamano_muestra / 100""")

md(r"""## 3. Tipos de datos, pensados como variables de encuesta

En una encuesta no todas las variables son iguales. Python distingue tipos, igual que SPSS distingue numéricas / cadena:

| Tipo en Python | Qué es | Ejemplo en una encuesta |
|---|---|---|
| `int` | número entero | edad: 42, casos: 800 |
| `float` | número con decimales | ponderador: 1.19 |
| `str` | texto ("string") | región: "Metropolitana" |
| `bool` | verdadero/falso | ¿es mayor de edad?: `True` |

Veámoslos:""")

code(r"""edad = 42                 # int  (entero)
ponderador = 1.19         # float (decimal)
region = "Metropolitana"  # str  (texto, SIEMPRE entre comillas)
es_mayor_de_edad = True   # bool (True / False)

# La función type() nos dice de qué tipo es cada cosa
print(type(edad))
print(type(ponderador))
print(type(region))
print(type(es_mayor_de_edad))""")

md(r"""Con texto (`str`) podemos hacer cosas útiles para limpiar datos más adelante:""")

code(r"""ciudad = "  santiago "

print(ciudad.upper())           # TODO EN MAYÚSCULAS
print(ciudad.strip())           # quita los espacios de los costados
print(ciudad.strip().title())   # encadenamos: sin espacios y con Mayúscula Inicial""")

md(r"""## 4. Listas y diccionarios: guardar varias cosas juntas

### Listas: una colección ordenada
Una **lista** guarda varios valores en orden. Útil, por ejemplo, para tener juntas las variables que queremos analizar.""")

code(r"""# Las preguntas de satisfacción de nuestro estudio
preguntas_satisfaccion = ["P1_sat_atencion", "P2_sat_tiempos", "P3_sat_app",
                          "P4_sat_sucursal", "P5_sat_general"]

print("Tenemos", len(preguntas_satisfaccion), "preguntas de satisfacción")
print("La primera es:", preguntas_satisfaccion[0])   # ¡se cuenta desde 0!
print("La última es:", preguntas_satisfaccion[-1])   # -1 = la última""")

md(r"""> ⚠️ **Ojo importantísimo:** en Python se empieza a contar desde **0**, no desde 1. El primer elemento es `[0]`, el segundo `[1]`, etc. Es la fuente de error #1 de quien viene de Excel/SPSS.

### Diccionarios: las "etiquetas de valor" de SPSS
Un **diccionario** asocia una *clave* con un *valor*: `clave: valor`. Es exactamente la idea de las **etiquetas de valor** de SPSS (1 = "Hombre", 2 = "Mujer").""")

code(r"""# El diccionario de etiquetas de la variable SEXO
etiquetas_sexo = {1: "Hombre", 2: "Mujer", 9: "Sin dato"}

# Consultamos qué significa el código 2
print("El código 2 significa:", etiquetas_sexo[2])""")

code(r"""# El diccionario de etiquetas de una pregunta Likert de satisfacción
etiquetas_satisfaccion = {
    1: "Muy insatisfecho",
    2: "Insatisfecho",
    3: "Ni satisfecho ni insatisfecho",
    4: "Satisfecho",
    5: "Muy satisfecho",
    99: "No sabe / No responde"
}

etiquetas_satisfaccion[4]""")

md(r"""Guarda bien esta idea: **estos diccionarios serán nuestra forma de recodificar** variables en las próximas sesiones. Por ahora basta con entender que existen y para qué sirven.

---

## 5. ¡La estrella del curso! Abrir una base de datos real

Hasta aquí trabajamos con valores sueltos. Ahora viene lo importante: cargar una **base de encuesta completa**.

Para esto usamos **pandas**, la herramienta central de todo el curso. Primero la *importamos* (la cargamos para poder usarla). Por convención se le pone el apodo `pd`:""")

code(r"""import pandas as pd   # importamos pandas y lo llamamos 'pd'""")

md(r"""Ahora abrimos nuestra base. Es un estudio ficticio de **satisfacción de clientes de un banco** (800 respuestas), del tipo que hacemos en consultoría.

El archivo usa `;` como separador y coma decimal (formato típico en Chile/Excel en español), así que se lo indicamos a pandas:""")

code(r"""datos = pd.read_csv("datos/encuesta_satisfaccion.csv", sep=";", decimal=",")""")

md(r"""¿No pasó nada visible? ¡Perfecto! La base quedó guardada en la variable `datos`. Esto es un **DataFrame**: el equivalente a una hoja de datos completa de SPSS (la *Vista de Datos*).

Mirémosla con `.head()`, que muestra las primeras filas:""")

code(r"""datos.head()""")

md(r"""¡Ahí está nuestra encuesta! Cada **fila** es una persona encuestada y cada **columna** es una variable (una pregunta o un dato).

Algunas preguntas naturales al recibir una base nueva:

**¿Cuántos casos y cuántas variables tengo?** → `.shape` (filas, columnas)""")

code(r"""datos.shape""")

md(r"""Eso significa: **800 filas (personas) y 15 columnas (variables)**.

**¿Cómo se llaman las variables?** → `.columns`""")

code(r"""datos.columns""")

md(r"""**¿Y las últimas filas?** → `.tail()`""")

code(r"""datos.tail()""")

md(r"""Podemos mirar **una sola variable** escribiendo su nombre entre corchetes. Por ejemplo, la pregunta de satisfacción general:""")

code(r"""datos["P5_sat_general"].head(10)""")

md(r"""Fíjate que aparecen los códigos numéricos (1 a 5, y algún 99 de "No sabe/No responde"). Aún están "crudos", sin etiquetas. **Convertir esos códigos en texto legible usando el diccionario que vimos antes será justamente lo que aprenderemos a hacer en las próximas sesiones.**

---

## 6. Conexión con SPSS (para que no te pierdas)

| Lo que hacías en SPSS | Lo que hicimos hoy en Python |
|---|---|
| Abrir el archivo `.sav` | `pd.read_csv(...)` |
| La *Vista de Datos* (la tabla completa) | El `DataFrame` (`datos`) |
| Una columna / variable | `datos["nombre_columna"]` |
| Ver el N de la base | `datos.shape` |
| La *Vista de Variables* (lista de variables) | `datos.columns` |
| Etiquetas de valor (1 = "Hombre") | Un diccionario `{1: "Hombre", ...}` |

---

## 7. Tu turno (tarea corta y opcional)

Practica antes de la próxima clase. Crea una **celda nueva** debajo de cada punto (botón `+` arriba) y resuelve:

1. Muestra las **primeras 3 filas** de la base. *(Pista: a `.head()` se le puede pasar un número.)*
2. ¿Cuántas filas y columnas tiene la base? Escribe la instrucción que lo responde.
3. Muestra solo la columna `region`.
4. Crea un diccionario llamado `etiquetas_producto` con estas equivalencias, inventando los códigos:
   `1 = "Cuenta Corriente"`, `2 = "Cuenta Vista"`, `3 = "Tarjeta de Crédito"`, `4 = "Crédito de Consumo"`.
5. Usando ese diccionario, imprime qué significa el código `3`.

> En la **Sesión 2** aprenderemos a *seleccionar y filtrar*: quedarnos solo con las columnas que nos interesan y con los casos que cumplen una condición (ej. "solo mujeres mayores de 30 de la Región Metropolitana").""")

code(r"""# Espacio para tus ejercicios 👇
""")

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.x"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open("curso/01 - Sesion 1 - Hola Python.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("Notebook creado con", len(cells), "celdas")
