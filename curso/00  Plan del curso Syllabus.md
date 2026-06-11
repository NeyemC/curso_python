# Python para Análisis de Encuestas
## Plan del curso — Syllabus general

> **Para quién es este curso:** equipo de consultoría (sociología, ciencias sociales, ingeniería) dedicado a estudios de mercado, experiencia de cliente (CX), opinión pública y estudios sociales. El hilo conductor es **el flujo de trabajo real de un estudio de encuesta**: desde que llega la base de datos hasta que entregamos tablas, gráficos, modelos y conclusiones.

---

## 1. Filosofía del curso

Las chicas pidieron **un enfoque práctico, sin descuidar la teoría**. Por eso cada sesión sigue la misma lógica:

```
┌─────────────────────────────────────────────────────────┐
│  1. ¿Por qué? (5-10 min)                                  │
│     Un problema real de un estudio: "tengo esta base y    │
│     necesito el % de satisfacción por segmento".          │
│                                                            │
│  2. La idea (10-15 min)                                    │
│     El concepto mínimo necesario, SIEMPRE conectado con   │
│     lo que ya saben de Excel o SPSS.                       │
│                                                            │
│  3. Manos a la obra (30-50 min)                            │
│     Hacemos el ejercicio juntos, en vivo, sobre datos     │
│     de encuesta de verdad.                                 │
│                                                            │
│  4. Tu turno (tarea corta, opcional)                      │
│     Un mini-reto para afianzar antes de la próxima clase. │
└─────────────────────────────────────────────────────────┘
```

**Principio rector:** *nunca enseñamos un concepto de Python sin mostrar para qué sirve en un estudio.* Las variables, los bucles y las funciones aparecen cuando se necesitan para resolver un problema concreto, no como una lista de temas a memorizar.

### Analogías permanentes con Excel / SPSS

Como el equipo viene de Excel y SPSS, todo el curso traduce conceptos:

| En Excel / SPSS | En Python (pandas) |
|---|---|
| Una hoja de cálculo | Un `DataFrame` |
| Una columna / variable | Una `Series` |
| Recodificar (Transformar → Recodificar) | `.map()`, `.replace()`, `np.where()` |
| Etiquetas de valor (1 = "Hombre") | Diccionarios de recodificación |
| Tabla dinámica | `groupby()` / `pivot_table()` |
| Tablas de frecuencia | `value_counts()` |
| Tablas de contingencia (Crosstabs) | `pd.crosstab()` |
| Ponderar casos | Columna de pesos + agregaciones ponderadas |
| Filtrar (Datos → Filtro) | Filtros booleanos (`df[df["edad"] > 18]`) |
| BUSCARV / VLOOKUP | `merge()` |
| Gráfico dinámico | `matplotlib` / `seaborn` |
| Correlaciones / Regresión / Factorial | `scipy`, `statsmodels`, `scikit-learn` |

---

## 2. Formato y logística

- **Frecuencia:** 1 sesión por semana.
- **Duración:** 1 hora a 1 hora y media por sesión.
- **Modalidad:** en vivo, todas con el notebook abierto, escribiendo código a la par.
- **Herramienta:** Jupyter Notebook (instalación local con Miniconda/Anaconda), igual que el material base del curso anterior.
- **Material por sesión:** un notebook `.ipynb` listo para ejecutar + un set de datos de encuesta + una tarea breve opcional.
- **Datos:** usamos datasets de encuesta realistas (satisfacción, opinión, sociodemográficos). Cuando se pueda, adaptamos a bases reales anonimizadas de la consultora.

> **Recomendación de ritmo:** el curso está pensado modular. Las primeras ~9 sesiones son el **núcleo imprescindible** (cargar, limpiar, analizar y graficar una encuesta de principio a fin). De ahí en adelante son **módulos de profundización** — visualización, automatización y estadística avanzada — que se pueden tomar, reordenar o saltar según el interés del equipo.

---

## 3. Mapa del curso (visión de pájaro)

```
BLOQUE 0  ·  Preparación                  → Antes de empezar
BLOQUE 1  ·  Primeros pasos               → Sesiones 1-2
BLOQUE 2  ·  Manejar la base              → Sesiones 3-5
BLOQUE 3  ·  Limpiar y recodificar        → Sesiones 6-8
BLOQUE 4  ·  Analizar la encuesta         → Sesiones 9-12    ← el corazón del curso
BLOQUE 5  ·  Visualizar resultados        → Sesiones 13-14
BLOQUE 6  ·  Automatizar el reporte       → Sesiones 15-16
BLOQUE 7  ·  Estadística avanzada         → Sesiones 17-21   ← correlacional y multivariada
PROYECTO  ·  Estudio de punta a punta     → Sesión 22
```

---

## 4. Detalle de sesiones

### BLOQUE 0 · Preparación (no es una sesión, es un instructivo previo)

Objetivo: que todas lleguen a la Sesión 1 con el entorno funcionando.
- Instalar Miniconda/Anaconda.
- Abrir Jupyter Notebook (o VS Code con la extensión de Jupyter).
- Descargar/clonar la carpeta de materiales del curso.
- Verificar que `import pandas` funciona.

> Entregable: una **guía de instalación con capturas** (paso a paso, a prueba de errores) + un canal de ayuda para resolver dudas antes de la primera clase.

---

### BLOQUE 1 · Primeros pasos

#### Sesión 1 — "Hola, Python": el entorno, los datos y el DataFrame
- **¿Por qué?** Pasar de hacer todo a mano en Excel a un proceso reproducible y rápido.
- **Contenidos:**
  - Qué es Python y qué es Jupyter (sin tecnicismos). La celda: escribir, ejecutar (Shift+Enter), el orden importa.
  - Tipos de datos pensando en variables de encuesta: números (`int`, `float`), texto (`str`), booleanos; listas y diccionarios como "la forma natural de guardar opciones de respuesta y sus etiquetas".
  - Abrir nuestra primera base con `pd.read_csv()`; `.head()`, `.shape`, `.columns`: "¿qué tengo entre manos?".
- **Manos a la obra:** cargar una base de satisfacción, mirarla, y construir el "diccionario de etiquetas" de una pregunta (ej. `{1: "Muy en desacuerdo", ..., 5: "Muy de acuerdo"}`).
- **Analogía:** abrir el archivo y mirar Vista de Datos + Vista de Variables de SPSS; los diccionarios = las etiquetas de valor.

> *Nota: esta sesión fusiona los fundamentos de Python y la primera mirada al DataFrame, que para un equipo que ya usa SPSS no necesitan tres clases separadas.*

#### Sesión 2 — Seleccionar y filtrar: apuntar a la variable y al caso correcto
- **¿Por qué?** Antes de analizar hay que saber "apuntar" a la variable o al grupo de casos que queremos.
- **Contenidos:**
  - Seleccionar una columna (`df["P1"]`) y varias (`df[["P1","P2"]]`).
  - `loc` e `iloc` (etiqueta vs. posición) explicado simple.
  - Filtrar casos con condiciones y combinarlas (`df[(df["edad"]>=18) & (df["sexo"]=="Mujer")]`).
- **Manos a la obra:** "quiero solo las mujeres mayores de 30 de la región metropolitana" → primer filtro combinado.
- **Analogía:** seleccionar columnas = elegir variables; filtrar = el filtro de casos de SPSS/Excel.

---

### BLOQUE 2 · Manejar la base

#### Sesión 3 — Cargar datos de verdad: CSV, Excel y archivos SPSS (.sav)
- **¿Por qué?** Los datos llegan en mil formatos. Hay que saber abrirlos todos.
- **Contenidos:**
  - `read_csv` con separadores, codificación (acentos/ñ), decimales con coma.
  - `read_excel` (hojas, rangos).
  - **Leer `.sav` de SPSS con `pyreadstat`** — y recuperar etiquetas de variable y de valor. (Clave para este equipo.)
- **Manos a la obra:** abrir la misma encuesta desde 3 formatos distintos y comparar.
- **Analogía:** "el puente entre el mundo SPSS y el mundo Python".

#### Sesión 4 — Explorar y diagnosticar la base
- **¿Por qué?** Antes de analizar hay que saber qué tan sucia/completa está la base.
- **Contenidos:**
  - `.info()`, `.describe()`, `.dtypes`.
  - Conteo de nulos (`.isnull().sum()`).
  - `value_counts()` para ver categorías y detectar rarezas (un "99", un "Mujre" mal escrito).
- **Manos a la obra:** "informe de salud" de una base recién recibida del terreno.

#### Sesión 5 — Ordenar, renombrar y crear variables
- **¿Por qué?** Las bases vienen con nombres horribles (`P1_A_1`) y casi siempre hay que crear variables nuevas.
- **Contenidos:**
  - Renombrar columnas (`rename`).
  - Ordenar (`sort_values`).
  - Crear una columna nueva (ej. `grupo_edad` a partir de `edad`).
- **Manos a la obra:** dejar la base con nombres legibles y crear una variable de tramo etario.

---

### BLOQUE 3 · Limpiar y recodificar

#### Sesión 6 — Valores perdidos: detectar, decidir, tratar
- **¿Por qué?** Toda encuesta tiene "No sabe / No responde", saltos y casos incompletos.
- **Contenidos:**
  - Identificar NS/NR y códigos especiales (88, 99) y convertirlos en `NaN`.
  - Decidir: ¿eliminar caso, imputar, o dejar como categoría?
  - `dropna`, `fillna`.
- **Manos a la obra:** limpiar los perdidos de una batería de preguntas de opinión.

#### Sesión 7 — Recodificar variables (el pan de cada día)
- **¿Por qué?** Recodificar es, probablemente, **la tarea más frecuente** en análisis de encuestas.
- **Contenidos:**
  - `.map()` con diccionario (1 → "Hombre", 2 → "Mujer").
  - `.replace()`.
  - `np.where()` y `pd.cut()` para agrupar (ej. edad → tramos; escala 1-10 → "Detractor/Pasivo/Promotor" para NPS).
- **Manos a la obra:** recodificar sexo, tramo etario y construir la clasificación NPS.
- **Analogía:** esto es Transformar → Recodificar de SPSS, pero reproducible y documentado.

#### Sesión 8 — Limpiar texto y respuestas abiertas
- **¿Por qué?** Casi siempre hay una pregunta abierta y campos con mayúsculas/espacios inconsistentes.
- **Contenidos:**
  - Métodos `.str` (minúsculas, quitar espacios, reemplazar).
  - Estandarizar categorías mal escritas.
  - Una primera mirada a contar palabras / categorizar a mano respuestas abiertas.
- **Manos a la obra:** limpiar una variable "ciudad" llena de inconsistencias.

---

### BLOQUE 4 · Analizar la encuesta · *(el corazón del curso)*

#### Sesión 9 — Frecuencias y descriptivos: el análisis univariado
- **¿Por qué?** El primer entregable de casi todo estudio es "las frecuencias".
- **Contenidos:**
  - Tablas de frecuencia con `value_counts()` (conteo y porcentaje).
  - Descriptivos de variables numéricas (media, mediana, desviación).
  - Frecuencias bien presentadas (ordenadas, con %).
- **Manos a la obra:** generar la tabla de frecuencias de las principales preguntas del estudio.

#### Sesión 10 — Cruces: tablas de contingencia (análisis bivariado)
- **¿Por qué?** "¿La satisfacción cambia según el segmento?" es *la* pregunta de consultoría.
- **Contenidos:**
  - `pd.crosstab()` (conteos y porcentajes por fila/columna).
  - Cruces de satisfacción × sexo, × tramo etario, × región.
  - Interpretación correcta de los porcentajes (¿base fila o columna?).
- **Manos a la obra:** tabla de doble entrada satisfacción × segmento, lista para el informe.
- **Analogía:** los Crosstabs de SPSS.

#### Sesión 11 — Agrupar y resumir con `groupby` (tablas dinámicas en código)
- **¿Por qué?** "Promedio de satisfacción por sucursal / por segmento" — el pan de cada día.
- **Contenidos:**
  - `groupby()` + `mean`, `count`, `median`.
  - `pivot_table()` como tabla dinámica.
  - Agrupar por dos variables a la vez.
- **Manos a la obra:** indicador promedio por segmento y por zona en una sola tabla.

#### Sesión 12 — Ponderación: cuando los casos no valen todos lo mismo
- **¿Por qué?** En estudios de opinión y de mercado casi siempre hay **factor de expansión / ponderador**. Ignorarlo da resultados mal sesgados.
- **Contenidos:**
  - Qué es un ponderador y por qué existe.
  - Frecuencias y promedios **ponderados**.
  - Comparar resultados con y sin ponderar.
- **Manos a la obra:** recalcular las frecuencias de la Sesión 9 aplicando el ponderador y ver cómo cambian.
- **Nota:** módulo especialmente relevante para opinión pública y muestras complejas.

---

### BLOQUE 5 · Visualizar resultados

#### Sesión 13 — Gráficos básicos para entender los datos
- **¿Por qué?** Un gráfico vale más que mil tablas para explorar y para presentar.
- **Contenidos:**
  - Barras (categóricas), histogramas (numéricas), líneas (tendencias).
  - `matplotlib` lo justo + `pandas .plot()`.
  - Errores comunes (gráfico de torta abusado, ejes engañosos).
- **Manos a la obra:** graficar las frecuencias principales del estudio.

#### Sesión 14 — Gráficos presentables para el informe del cliente
- **¿Por qué?** El gráfico que va al PPT necesita título, colores de marca, % y orden.
- **Contenidos:**
  - `seaborn` para gráficos más lindos con menos código.
  - Barras apiladas/agrupadas para cruces.
  - Colores corporativos, etiquetas de datos, exportar a imagen.
- **Manos a la obra:** convertir una tabla de cruce en un gráfico listo para presentación.

---

### BLOQUE 6 · Automatizar el reporte

#### Sesión 15 — Funciones y bucles: deja de copiar y pegar
- **¿Por qué?** Si calculas la misma tabla para 20 preguntas, no debes escribirla 20 veces.
- **Contenidos:**
  - Definir funciones (`def`) — "mi función de tabla de frecuencias con %".
  - Bucles `for` sobre una lista de variables.
  - Aplicar la misma rutina a una batería de preguntas.
- **Manos a la obra:** una función que recibe una variable y devuelve su tabla formateada; aplicarla a todas las preguntas de una batería.

#### Sesión 16 — Exportar resultados a Excel y reportes automáticos
- **¿Por qué?** El entregable suele ser un Excel con muchas pestañas o un set de tablas.
- **Contenidos:**
  - Exportar a Excel/CSV (`to_excel`, varias hojas).
  - Dar formato básico al Excel de salida.
  - Idea de "libro de tablas" generado automáticamente.
- **Manos a la obra:** generar de un tirón un Excel con todas las frecuencias y cruces del estudio.

---

### BLOQUE 7 · Estadística avanzada · *(correlacional y multivariada)*

> Este bloque es el "salto de nivel" pedido por el equipo. El enfoque sigue siendo aplicado: el objetivo es **saber cuándo usar cada técnica, cómo correrla e interpretarla bien**, no la demostración matemática. Apoyo conceptual + código reproducible.

#### Sesión 17 — Escalas, índices y NPS
- **¿Por qué?** Muchos estudios construyen índices (satisfacción global, NPS, escalas Likert promediadas).
- **Contenidos:**
  - Promediar baterías de ítems (índices).
  - Calcular NPS correctamente (% Promotores − % Detractores).
  - Fiabilidad de una escala: **alfa de Cronbach** (consistencia interna) e interpretación.
- **Manos a la obra:** construir el índice de satisfacción, el NPS y evaluar la fiabilidad de una batería Likert.

#### Sesión 18 — Correlación: medir la asociación entre variables
- **¿Por qué?** "¿La satisfacción se relaciona con la antigüedad como cliente?".
- **Contenidos:**
  - Correlación de **Pearson** (numéricas) y **Spearman** (ordinales/Likert) — cuándo cada una.
  - Matriz de correlaciones y su **mapa de calor** (`heatmap`).
  - Interpretación honesta: fuerza, dirección, significancia y el clásico "correlación ≠ causalidad".
- **Manos a la obra:** matriz de correlaciones de las baterías del estudio + lectura de resultados.

#### Sesión 19 — Diferencias y regresión lineal: ¿qué explica el resultado?
- **¿Por qué?** "¿La diferencia entre segmentos es real?" y "¿qué variables predicen la satisfacción?".
- **Contenidos:**
  - Significancia: idea intuitiva, **chi-cuadrado** (categóricas) y **comparación de medias** (t-test / ANOVA).
  - **Regresión lineal** con `statsmodels`: leer coeficientes, R², p-valores e interpretarlos en lenguaje de negocio.
  - Variables dummy para meter categóricas al modelo.
- **Manos a la obra:** modelo que explica la satisfacción a partir de variables sociodemográficas y de servicio.

#### Sesión 20 — Reducción de dimensiones: análisis factorial y PCA
- **¿Por qué?** Las baterías Likert tienen muchos ítems que en realidad miden pocas "dimensiones latentes". Reducirlas es central en estudios de actitudes e imagen.
- **Contenidos:**
  - Idea de variable latente / dimensión.
  - **Análisis de Componentes Principales (PCA)** y noción de **análisis factorial** (exploratorio).
  - Cuántos factores retener, cargas factoriales, interpretación y nombramiento de dimensiones.
- **Manos a la obra:** reducir una batería de 15 ítems de imagen a 3-4 dimensiones interpretables.

#### Sesión 21 — Segmentación: clustering y regresión logística
- **¿Por qué?** "Quiero segmentar a los clientes en perfiles" y "¿qué predice que alguien recomiende?".
- **Contenidos:**
  - **Clustering K-means** para construir segmentos a partir de variables actitudinales.
  - Perfilar y nombrar los segmentos resultantes.
  - **Regresión logística** para un desenlace binario (recomienda / no recomienda) e interpretación de probabilidades.
- **Manos a la obra:** segmentar la muestra en perfiles y caracterizarlos; modelo logístico de recomendación.
- **Nota:** introducción aplicada; abre la puerta a un eventual módulo futuro de machine learning.

---

### PROYECTO FINAL

#### Sesión 22 — Un estudio de encuesta de punta a punta
- Cada participante (o en duplas) toma una base de encuesta y produce:
  1. Carga y limpieza.
  2. Recodificaciones.
  3. Tabla de frecuencias de las preguntas clave.
  4. Al menos dos cruces relevantes (con ponderador si aplica).
  5. Un análisis multivariado a elección (correlaciones, factorial o segmentación).
  6. Dos gráficos presentables.
  7. Un Excel de salida con todo.
- **Cierre:** breve presentación de resultados al equipo. El objetivo es que cada una salga con **una plantilla reutilizable** para sus próximos estudios reales.

---

## 5. Resultado esperado al terminar el curso

Al final, el equipo podrá, **sin depender de Excel/SPSS para todo**:

- Abrir cualquier base de encuesta (CSV, Excel, SPSS).
- Limpiarla y recodificarla de forma documentada y reproducible.
- Producir frecuencias, cruces y promedios (ponderados si corresponde).
- Construir índices, NPS y evaluar la fiabilidad de escalas.
- Aplicar e **interpretar** técnicas correlacionales y multivariadas (correlación, regresión, factorial/PCA, clustering, logística).
- Generar gráficos presentables y un libro de tablas en Excel.
- Reutilizar su propio código en los siguientes estudios, ahorrando horas en cada proyecto.

---

## 6. Qué reutilizamos del curso anterior

El material existente (`ejemplos/Clase 01 - jupyter notebooks/`) es una buena base teórica. Lo aprovechamos así:

| Material previo | Cómo lo usamos ahora |
|---|---|
| Notebooks 01-02 (fundamentos Python) | Fuente para Sesiones 1-2, pero **reescritos con ejemplos de encuesta**. |
| Notebook 03 (NumPy) | Lo mínimo de NumPy se integra dentro de pandas; no una sesión aparte. |
| Notebook 04 (Pandas) | Base de los Bloques 2-4. |
| Notebooks 05-06 (limpieza) | Base del Bloque 3. |
| `matricula2019.csv` | Excelente dataset real (educación, Chile) para varios ejercicios. |
| Ejercicios 07-08 | Banco de tareas opcionales para quienes quieran más práctica. |

**Cambio de enfoque principal:** el curso anterior iba *concepto → ejemplo*. Este va *problema de un estudio → concepto necesario para resolverlo*. Más práctico, como pidió el equipo, pero sin saltarse la teoría: la teoría aparece *justo cuando se necesita*, que es cuando mejor se aprende.

---

## 7. Herramientas estadísticas por bloque (referencia)

| Bloque | Librerías principales |
|---|---|
| 1-6 (datos) | `pandas`, `numpy` |
| Visualización | `matplotlib`, `seaborn` |
| Correlación / regresión / tests | `scipy.stats`, `statsmodels`, `pingouin` (opcional) |
| Factorial / PCA | `scikit-learn`, `factor_analyzer` |
| Clustering / logística | `scikit-learn` |
| Lectura SPSS | `pyreadstat` |

---

*Próximo paso sugerido: con este plan aprobado, construimos el notebook completo de la **Sesión 1** (listo para dictar) y la **guía de instalación** del Bloque 0.*
