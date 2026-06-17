# -*- coding: utf-8 -*-
"""
Genera versiones .xlsx y .sav (SPSS) del dataset de encuesta, a partir
del CSV ya creado. El .sav incluye ETIQUETAS DE VARIABLE y DE VALOR,
para poder demostrar en la Sesion 3 como pyreadstat las recupera.
"""
import pandas as pd
import pyreadstat

# Partimos del CSV ya generado
df = pd.read_csv("curso/datos/encuesta_satisfaccion.csv", sep=";", decimal=",")

# ----------------------------------------------------------------------
# 1) Version Excel (.xlsx)
# ----------------------------------------------------------------------
df.to_excel("curso/datos/encuesta_satisfaccion.xlsx", index=False, sheet_name="Respuestas")

# ----------------------------------------------------------------------
# 2) Version SPSS (.sav) con etiquetas
# ----------------------------------------------------------------------
# Etiquetas de VARIABLE (descripcion de cada columna, como en SPSS)
column_labels = {
    "id": "Identificador del caso",
    "sexo": "Sexo del encuestado",
    "edad": "Edad en anios cumplidos",
    "region": "Region de residencia",
    "ciudad": "Ciudad de residencia (texto abierto)",
    "producto": "Producto principal contratado",
    "antiguedad_anios": "Antiguedad como cliente (anios)",
    "P1_sat_atencion": "P1. Satisfaccion con la atencion del ejecutivo",
    "P2_sat_tiempos": "P2. Satisfaccion con los tiempos de espera",
    "P3_sat_app": "P3. Satisfaccion con la app / banca en linea",
    "P4_sat_sucursal": "P4. Satisfaccion con la sucursal",
    "P5_sat_general": "P5. Satisfaccion general con el banco",
    "P6_nps": "P6. Probabilidad de recomendar (0 a 10)",
    "comentario": "Comentario abierto",
    "ponderador": "Factor de expansion / ponderador",
}

# Etiquetas de VALOR (que significa cada codigo, como en SPSS)
likert = {1: "Muy insatisfecho", 2: "Insatisfecho",
          3: "Ni satisf. ni insatisf.", 4: "Satisfecho",
          5: "Muy satisfecho", 99: "No sabe / No responde"}

variable_value_labels = {
    "sexo": {1: "Hombre", 2: "Mujer", 9: "Sin dato"},
    "P1_sat_atencion": likert,
    "P2_sat_tiempos": likert,
    "P3_sat_app": likert,
    "P4_sat_sucursal": likert,
    "P5_sat_general": likert,
    "P6_nps": {99: "No sabe / No responde"},
}

pyreadstat.write_sav(
    df,
    "curso/datos/encuesta_satisfaccion.sav",
    column_labels=column_labels,
    variable_value_labels=variable_value_labels,
)

print("Generados:")
print(" - curso/datos/encuesta_satisfaccion.xlsx")
print(" - curso/datos/encuesta_satisfaccion.sav")

# Verificacion rapida: releer el .sav y mostrar metadatos
df2, meta = pyreadstat.read_sav("curso/datos/encuesta_satisfaccion.sav")
print("\nVerificacion .sav -> shape:", df2.shape)
print("Etiqueta de 'P5_sat_general':", meta.column_names_to_labels["P5_sat_general"])
print("Value labels de 'sexo':", meta.variable_value_labels["sexo"])
