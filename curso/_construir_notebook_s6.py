# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 6 (.ipynb)."""
import json
cells = []
def md(t):  cells.append({"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)})
def code(t):cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                          "outputs": [], "source": t.splitlines(keepends=True)})

md(r"""# Sesión 6 — Valores perdidos: detectar, decidir, tratar

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Convertir los **códigos escondidos** (99, 999) en verdaderos vacíos (`NaN`).
- **Decidir** qué hacer con los faltantes: eliminar, imputar o dejar como categoría.
- Usar `dropna` y `fillna` con criterio.

> Toda encuesta tiene "No sabe / No responde", preguntas con salto y casos incompletos. Tratarlos bien es lo que separa un análisis serio de uno que engaña.

---""")

md(r"""## 0. Cargamos la base""")
code(r"""import pandas as pd
import numpy as np

datos = pd.read_csv("datos/encuesta_satisfaccion.csv", sep=";", decimal=",")
datos.head(3)""")

md(r"""## 1. El problema: perdidos disfrazados de números

En la Sesión 4 lo diagnosticamos: los faltantes están escondidos como **códigos**.
- `edad = 999` → "sin dato"
- Baterías de satisfacción `= 99` → "No sabe / No responde"
- `nps = 99` → "No sabe / No responde"
- `sexo = 9` → "Sin dato"

El peligro es tratarlos como números reales. Míralo con la edad:""")
code(r"""# Promedio de edad SIN tratar el 999: sale inflado y es FALSO
print("Media de edad (con los 999):", round(datos["edad"].mean(), 1))""")

md(r"""Ese promedio está contaminado por los `999`. El primer paso es **convertir esos códigos en `NaN`** (el vacío oficial de pandas), para que los cálculos los ignoren.

## 2. Convertir códigos a `NaN` con `.replace()`

`replace` cambia unos valores por otros. Para "vaciar" un código, lo reemplazamos por `np.nan`.""")
code(r"""# La edad: 999 pasa a ser vacío
datos["edad"] = datos["edad"].replace(999, np.nan)

# Ahora el promedio es correcto (pandas ignora los NaN automáticamente)
print("Media de edad (ya limpia):", round(datos["edad"].mean(), 1))""")

md(r"""¡Cambió! Ahora el promedio es real. Hagamos lo mismo con el **99** en la batería de satisfacción. Como son varias columnas, las tratamos todas juntas.""")
code(r"""bateria = ["P1_sat_atencion", "P2_sat_tiempos", "P3_sat_app",
           "P4_sat_sucursal", "P5_sat_general"]

# En esas columnas, el 99 pasa a NaN
datos[bateria] = datos[bateria].replace(99, np.nan)

# También el nps (99) y el sexo (9 = sin dato)
datos["P6_nps"] = datos["P6_nps"].replace(99, np.nan)
datos["sexo"]   = datos["sexo"].replace(9, np.nan)

datos[bateria].describe()""")

md(r"""Fíjate que ahora el `max` de las preguntas es **5** (ya no 99): los códigos desaparecieron de los cálculos.

> 💡 **Truco:** también se puede hacer al **cargar** el archivo, con `pd.read_csv(..., na_values=[99, 999])`. Es cómodo, pero ojo: vaciaría *todos* los 99 y 999 de *todas* las columnas, lo que no siempre es lo que quieres (imagina una variable donde 99 es una respuesta válida). Por eso aquí lo hicimos columna por columna, con control.

## 3. ¿Cuántos faltantes tenemos ahora?

Recontemos los `NaN`. Ahora sí reflejan todos los perdidos, visibles y antes escondidos.""")
code(r"""datos.isnull().sum()""")

md(r"""## 4. Decidir qué hacer: eliminar, imputar o dejar

No hay una regla única. Depende del análisis:

| Estrategia | Cuándo | Cómo |
|---|---|---|
| **Dejar como `NaN`** | Para frecuencias y promedios (pandas ya los ignora). Es lo más honesto. | No hacer nada |
| **Eliminar el caso** | Cuando faltan datos clave y necesitas casos completos. | `dropna` |
| **Imputar** (rellenar) | Con cuidado y justificación (ej. rellenar con la mediana). | `fillna` |

## 5. `dropna` — eliminar casos incompletos

`dropna` elimina filas que tengan `NaN`. Puedes acotarlo a ciertas columnas con `subset`.""")
code(r"""# Casos que respondieron la satisfacción general (sin NaN en esa columna)
con_sat = datos.dropna(subset=["sat_general"] if "sat_general" in datos.columns else ["P5_sat_general"])
print("Casos originales:", datos.shape[0])
print("Casos con satisfacción general respondida:", con_sat.shape[0])""")

md(r"""> ⚠️ **Cuidado con `dropna` sin `subset`:** si lo aplicas a toda la base, elimina cualquier fila con *algún* vacío. Como `comentario` está casi siempre vacío, ¡borrarías casi toda la muestra! Casi siempre conviene usar `subset` para apuntar solo a las columnas que importan.

## 6. `fillna` — rellenar (imputar) con criterio

`fillna` reemplaza los `NaN` por un valor. Un ejemplo defendible: rellenar la edad faltante con la **mediana** (más robusta que la media).""")
code(r"""mediana_edad = datos["edad"].median()
print("Mediana de edad:", mediana_edad)

# Creamos una versión con la edad imputada (sin pisar la original)
datos["edad_imputada"] = datos["edad"].fillna(mediana_edad)

# Comprobamos que ya no quedan vacíos en la versión imputada
datos["edad_imputada"].isnull().sum()""")

md(r"""> 🧭 **Regla de oro:** imputar cambia los datos, así que hazlo solo cuando tenga sentido, déjalo **documentado** (por eso creamos `edad_imputada` en vez de pisar `edad`) y menciónalo en el informe. Para la mayoría de las tablas de una encuesta, *dejar los `NaN`* es la opción más honesta.

## 7. Manos a la obra: limpiar la batería de opinión

Ya lo hicimos paso a paso. El resultado: una base donde los perdidos son `NaN` de verdad y los promedios son correctos. Verifiquémoslo comparando antes/después de la satisfacción general (que ahora ignora los NS/NR):""")
code(r"""col = "P5_sat_general"
print("Promedio satisfacción general (ignorando NS/NR):", round(datos[col].mean(), 2))
print("N que respondió (no NaN):", datos[col].notnull().sum())""")

md(r"""## 8. Conexión con SPSS

| En SPSS | Hoy en Python |
|---|---|
| Definir "valores perdidos" (99, 999) | `replace(99, np.nan)` |
| Que los análisis ignoren los perdidos | pandas ignora los `NaN` solo |
| Seleccionar casos válidos | `dropna(subset=[...])` |
| Reemplazar perdidos por la media/mediana | `fillna(...)` |

---

## 9. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio.** *(Ejecuta primero las celdas de arriba para tener la base ya limpia.)*

1. ¿Cuántos `NaN` tiene ahora la columna `P6_nps`? *(Pista: `.isnull().sum()`.)*
2. Calcula el promedio de `P1_sat_atencion` ya limpia. Compáralo mentalmente con lo que habría dado con los 99 dentro.
3. Crea `datos_completos` eliminando los casos con `NaN` en `sat_general` (o `P5_sat_general`). ¿Cuántos casos quedan?
4. Crea una columna `nps_imputado` rellenando los `NaN` de `P6_nps` con la **mediana** de esa variable.
5. **Reflexión:** ¿por qué es mejor crear `edad_imputada` en vez de reemplazar directamente la columna `edad`?""")
code("# Ejercicio 1: NaN en P6_nps\n")
code("# Ejercicio 2: promedio de P1_sat_atencion\n")
code("# Ejercicio 3: datos_completos con dropna(subset=...)\n")
code("# Ejercicio 4: nps_imputado con fillna(mediana)\n")
code("# Ejercicio 5: escribe tu reflexión\n")

md(r"""> En la **Sesión 7** haremos lo contrario de esconder datos: **recodificar** para que se entiendan. Convertiremos códigos en etiquetas (1 → "Hombre"), agruparemos categorías y construiremos la clasificación de **NPS** (Detractor / Pasivo / Promotor).""")

notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.x"}},"nbformat":4,"nbformat_minor":5}
with open("curso/06 - Sesion 6 - Valores perdidos.ipynb","w",encoding="utf-8") as f:
    json.dump(notebook,f,ensure_ascii=False,indent=1)
print("S6 OK", len(cells), "celdas")
