"""
Generador del dataset de encuesta ficticio para el curso.
Estudio de satisfaccion / CX de un banco (escenario tipico de consultoria).

Crea una base realista CON SUCIEDAD INTENCIONAL (codigos 99, texto
inconsistente, algunos perdidos) para que sirva de hilo conductor en
las sesiones de limpieza y analisis.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(2024)  # semilla fija -> base reproducible
N = 800

# ----------------------------------------------------------------------
# Sociodemograficos
# ----------------------------------------------------------------------
# Sexo: 1 = Hombre, 2 = Mujer, 9 = sin dato (lo dejamos sucio a proposito)
sexo = rng.choice([1, 2, 9], size=N, p=[0.47, 0.50, 0.03])

# Edad: entre 18 y 80, con sesgo hacia adultos jovenes
edad = rng.integers(18, 81, size=N)
# algunos perdidos como 999
idx_edad_perdida = rng.choice(N, size=12, replace=False)
edad = edad.astype(float)
edad[idx_edad_perdida] = 999

# Region: nombres con inconsistencias de mayusculas/espacios a proposito
regiones_base = ["Metropolitana", "Valparaiso", "Biobio", "Coquimbo", "Araucania"]
region = rng.choice(regiones_base, size=N, p=[0.45, 0.18, 0.15, 0.12, 0.10])
# ensuciamos algunas: espacios, mayusculas, minusculas
def ensuciar_region(r):
    opciones = [r, r.upper(), r.lower(), "  " + r, r + " "]
    return rng.choice(opciones, p=[0.7, 0.1, 0.1, 0.05, 0.05])
region = np.array([ensuciar_region(r) for r in region])

# Ciudad: campo abierto, mas sucio aun (para la sesion de texto)
ciudades_map = {
    "Metropolitana": ["Santiago", "santiago", "STGO", "Santiago ", "Puente Alto"],
    "Valparaiso": ["Valparaiso", "valpo", "Vina del Mar", "Viña del Mar", "VALPARAISO"],
    "Biobio": ["Concepcion", "concepción", "Talcahuano", "Los Angeles"],
    "Coquimbo": ["La Serena", "Coquimbo", "la serena", "Ovalle"],
    "Araucania": ["Temuco", "temuco", "Padre Las Casas", "Villarrica"],
}
ciudad = np.array([rng.choice(ciudades_map[r]) for r in
                   rng.choice(regiones_base, size=N, p=[0.45, 0.18, 0.15, 0.12, 0.10])])

# ----------------------------------------------------------------------
# Bateria de satisfaccion (escala Likert 1 a 5)
# 1 = Muy insatisfecho ... 5 = Muy satisfecho ; 99 = No sabe / No responde
# ----------------------------------------------------------------------
def likert(prob_alta=0.55):
    # genera respuestas con tendencia a satisfaccion alta, mas algunos NS/NR
    base = rng.choice([1, 2, 3, 4, 5], size=N,
                      p=[0.05, 0.10, 0.20, 0.35, 0.30])
    # introducir ~4% de 99 (NS/NR)
    mask99 = rng.random(N) < 0.04
    base = base.astype(float)
    base[mask99] = 99
    return base

sat_atencion   = likert()   # satisfaccion con la atencion del ejecutivo
sat_tiempos    = likert()   # satisfaccion con los tiempos de espera
sat_app        = likert()   # satisfaccion con la app / banca en linea
sat_sucursal   = likert()   # satisfaccion con la sucursal
sat_general    = likert()   # satisfaccion general

# ----------------------------------------------------------------------
# Pregunta NPS: recomendacion 0 a 10 ; 99 = NS/NR
# ----------------------------------------------------------------------
nps = rng.choice(range(0, 11), size=N,
                 p=[0.02, 0.02, 0.03, 0.04, 0.05, 0.08, 0.10, 0.14, 0.18, 0.16, 0.18])
nps = nps.astype(float)
mask_nps99 = rng.random(N) < 0.03
nps[mask_nps99] = 99

# ----------------------------------------------------------------------
# Producto principal y antiguedad como cliente
# ----------------------------------------------------------------------
producto = rng.choice(["Cuenta Corriente", "Cuenta Vista", "Tarjeta de Credito", "Credito de Consumo"],
                      size=N, p=[0.35, 0.30, 0.20, 0.15])
antiguedad_anios = rng.integers(0, 26, size=N)  # 0 a 25 anios

# ----------------------------------------------------------------------
# Ponderador (factor de expansion) - para la sesion de ponderacion
# valores alrededor de 1, simulando ajuste muestral
# ----------------------------------------------------------------------
ponderador = np.round(rng.uniform(0.4, 2.2, size=N), 3)

# ----------------------------------------------------------------------
# Comentario abierto (opcional, muchos vacios) - para sesion de texto
# ----------------------------------------------------------------------
comentarios = [
    "Buena atencion", "Demoraron mucho en atenderme", "La app se cae seguido",
    "Excelente ejecutivo", "Muy malos los tiempos de espera", "Todo bien",
    "", "", "", "", "", "Mejorar el sitio web", "Sin comentarios",
]
comentario = rng.choice(comentarios, size=N)

# ----------------------------------------------------------------------
# Armado del DataFrame
# ----------------------------------------------------------------------
df = pd.DataFrame({
    "id": np.arange(1, N + 1),
    "sexo": sexo,
    "edad": edad,
    "region": region,
    "ciudad": ciudad,
    "producto": producto,
    "antiguedad_anios": antiguedad_anios,
    "P1_sat_atencion": sat_atencion,
    "P2_sat_tiempos": sat_tiempos,
    "P3_sat_app": sat_app,
    "P4_sat_sucursal": sat_sucursal,
    "P5_sat_general": sat_general,
    "P6_nps": nps,
    "comentario": comentario,
    "ponderador": ponderador,
})

# Guardar con separador ; y decimales con coma (formato comun en LATAM/Excel ES)
import os
os.makedirs("curso/datos", exist_ok=True)
df.to_csv("curso/datos/encuesta_satisfaccion.csv", sep=";", decimal=",",
          index=False, encoding="utf-8")

print("Base generada:", df.shape)
print(df.head())
print("\nTipos:")
print(df.dtypes)
