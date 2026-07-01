# -*- coding: utf-8 -*-
"""Construye el notebook de la Sesion 12 (.ipynb)."""
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

md(r"""# Sesión 12 — Ponderación: cuando los casos no valen todos lo mismo

### Curso: Python para Análisis de Encuestas

**Objetivos de hoy**
- Entender **qué es un ponderador** (factor de expansión) y por qué existe.
- Calcular **frecuencias y promedios ponderados**.
- **Comparar** los resultados con y sin ponderar, y ver cuánto cambian.

> ⚖️ En estudios de opinión y de mercado casi siempre hay un ponderador. Ignorarlo entrega resultados **sesgados**. Esta sesión es clave para que los números que entregamos sean correctos.

---""")

md(r"""## 0. Preparamos la base""")
code(PREP)

md(r"""## 1. ¿Qué es un ponderador y por qué existe?

Imagina que en la población hay 50% de hombres y 50% de mujeres, pero en tu muestra quedaron 40% de hombres y 60% de mujeres (pasa siempre). Si sacas resultados "tal cual", las mujeres pesan de más.

El **ponderador** (o *factor de expansión*) corrige eso: le da a cada caso un "peso" para que la muestra se parezca a la población.
- Un caso con ponderador **2.0** cuenta como **dos** personas.
- Un caso con ponderador **0.5** cuenta como **media** persona.

Nuestra base trae la columna `ponderador`. Mírala:""")
code(r"""datos["ponderador"].describe().round(3)""")

md(r"""La suma de los ponderadores es el "tamaño expandido" de la muestra. Con valores en torno a 1, se parece al N real.""")
code(r"""print("N real (casos):", len(datos))
print("N ponderado (suma de pesos):", round(datos["ponderador"].sum(), 1))""")

md(r"""## 2. Frecuencias ponderadas

Sin ponderar, una frecuencia **cuenta casos** (cada uno vale 1). Ponderada, **suma pesos** (cada uno vale su ponderador).

Comparemos el reparto por sexo. Primero **sin ponderar** (lo de la Sesión 9):""")
code(r"""sin_ponderar = (datos["sexo_txt"].value_counts(normalize=True) * 100).round(1)
sin_ponderar""")

md(r"""Ahora **ponderado**: en vez de contar, sumamos los pesos de cada grupo y los dividimos por el peso total.""")
code(r"""pesos_grupo = datos.groupby("sexo_txt")["ponderador"].sum()
con_ponderar = (pesos_grupo / datos["ponderador"].sum() * 100).round(1)
con_ponderar""")

md(r"""Pongámoslos lado a lado para ver la diferencia:""")
code(r"""pd.DataFrame({"% sin ponderar": sin_ponderar, "% ponderado": con_ponderar})""")

md(r"""> 📌 Las diferencias pueden parecer pequeñas en este dataset de ejemplo, pero en estudios reales de opinión pública **cambian titulares**: un candidato puede subir o bajar varios puntos según se pondere o no. Por eso nunca se omite.

## 3. Promedios ponderados

Para un promedio, la versión ponderada es la **media ponderada**: en vez de sumar los valores y dividir por N, se pondera cada valor por su peso.

La fórmula es: **Σ(valor × peso) / Σ(peso)**. La forma más directa en Python es con `np.average`, indicándole los pesos. Ojo: hay que **quitar los `NaN`** primero (satisfacción no respondida).""")
code(r"""# Trabajamos solo con quienes respondieron satisfacción
d = datos.dropna(subset=["sat_general"])

media_simple = d["sat_general"].mean()
media_ponderada = np.average(d["sat_general"], weights=d["ponderador"])

print("Satisfacción promedio SIN ponderar:", round(media_simple, 3))
print("Satisfacción promedio PONDERADA  :", round(media_ponderada, 3))""")

md(r"""## 4. Promedio ponderado **por grupo**

En la Sesión 11 vimos el promedio por región. Su versión ponderada aplica la misma fórmula **dentro de cada grupo**: sumamos (valor × peso) por región y lo dividimos por la suma de pesos de esa región.""")
code(r"""d = datos.dropna(subset=["sat_general"])

# Numerador: suma de (satisfacción * peso) por región
num = (d["sat_general"] * d["ponderador"]).groupby(d["region"]).sum()
# Denominador: suma de pesos por región
den = d["ponderador"].groupby(d["region"]).sum()

promedio_ponderado = (num / den).round(2)
promedio_ponderado""")

md(r"""Comparémoslo con el promedio simple por región (el de la Sesión 11):""")
code(r"""promedio_simple = d.groupby("region")["sat_general"].mean().round(2)
pd.DataFrame({"promedio simple": promedio_simple,
              "promedio ponderado": promedio_ponderado})""")

md(r"""## 5. Manos a la obra: NPS ponderado (adelanto)

Un caso concreto y muy pedido: el reparto ponderado de los grupos NPS. Recodificamos NPS y calculamos su distribución ponderada.""")
code(r"""datos["nps_grupo"] = pd.cut(datos["P6_nps"], bins=[-1, 6, 8, 10],
                            labels=["Detractor", "Pasivo", "Promotor"])

d2 = datos.dropna(subset=["nps_grupo"])
reparto = d2.groupby("nps_grupo", observed=True)["ponderador"].sum()
reparto_pct = (reparto / d2["ponderador"].sum() * 100).round(1)
reparto_pct""")

md(r"""> Con ese reparto ponderado ya casi tenemos el indicador NPS (% Promotores − % Detractores). Lo formalizamos en la **Sesión 17**.

## 6. Conexión con SPSS

| En SPSS | Hoy en Python |
|---|---|
| Datos → Ponderar casos (por una variable) | usar la columna `ponderador` en los cálculos |
| Frecuencias ponderadas | `groupby(...)["ponderador"].sum()` en vez de contar |
| Media ponderada | `np.average(x, weights=peso)` |

---

## 7. Tu turno (tarea corta y opcional)

**Abajo dejé una celda vacía para cada ejercicio.** *(Ejecuta primero la celda de preparación.)*

1. Calcula el reparto **ponderado** (%) de la variable `region`. Compáralo con el sin ponderar.
2. Calcula el promedio **ponderado** de `P3_sat_app` (recuerda quitar los `NaN` con `dropna`).
3. Compara, para `producto`, el reparto sin ponderar vs. ponderado en una sola tabla.
4. Calcula el promedio ponderado de `sat_general` **por tramo de edad** (usa la fórmula num/den por grupo).
5. **Reflexión:** ¿en qué tipo de estudios de tu trabajo crees que la ponderación importa más? ¿Por qué?""")
code("# Ejercicio 1: reparto ponderado de region\n")
code("# Ejercicio 2: promedio ponderado de P3_sat_app\n")
code("# Ejercicio 3: producto, sin ponderar vs ponderado\n")
code("# Ejercicio 4: promedio ponderado de sat_general por tramo_edad\n")
code("# Ejercicio 5: escribe tu reflexión\n")

md(r"""> 🎉 **¡Cerramos el Bloque 4, el corazón del curso!** Ya sabes producir frecuencias, cruces, promedios por grupo y ponderar. Con esto puedes armar el grueso de un informe de encuesta. En la **Sesión 13** empezamos a **visualizar**: convertir estas tablas en gráficos claros.""")

notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.x"}},"nbformat":4,"nbformat_minor":5}
with open("curso/12 - Sesion 12 - Ponderacion.ipynb","w",encoding="utf-8") as f:
    json.dump(notebook,f,ensure_ascii=False,indent=1)
print("S12 OK", len(cells), "celdas")
