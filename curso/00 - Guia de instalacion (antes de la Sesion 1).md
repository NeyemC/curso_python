# Guía de instalación — Antes de la Sesión 1

> **Objetivo:** que llegues a la primera clase con Python y Jupyter funcionando, sin perder tiempo de clase en instalaciones. Sigue los pasos en orden. Si algo falla, escribe en el canal de ayuda del curso **antes** de la sesión.
>
> ⏱️ Tiempo estimado: 20-30 minutos (la descarga es lo más lento).
> 💻 Esta guía es para **Windows**. Si usas Mac, avísanos y te pasamos las indicaciones equivalentes.

---

## ¿Qué vamos a instalar?

Una sola cosa: **Anaconda**. Es un paquete que instala de un viaje todo lo que necesitamos:
- **Python** (el lenguaje).
- **Jupyter Notebook** (el cuaderno donde trabajaremos).
- **pandas**, **numpy**, **matplotlib** y el resto de librerías del curso, ya incluidas.

No necesitas saber qué es cada cosa todavía. Solo instálalo y listo.

---

## Paso 1 · Descargar Anaconda

1. Entra a 👉 **https://www.anaconda.com/download**
2. Puede pedirte un correo (puedes usar el de trabajo o saltarlo con la opción *"Skip registration"* / "Omitir").
3. Descarga el instalador para **Windows** (botón verde). Es un archivo de ~900 MB, puede demorar unos minutos.

> 📸 *(Aquí irá una captura de la página de descarga.)*

---

## Paso 2 · Instalar Anaconda

1. Abre el archivo descargado (`Anaconda3-....exe`).
2. Ve apretando **Next** / **I Agree** en las primeras pantallas.
3. Cuando pregunte *"Install for"*, deja la opción recomendada: **"Just Me"**.
4. Deja la carpeta de instalación que viene por defecto. Apreta **Next**.
5. En la pantalla de *"Advanced Options"*, **deja las casillas como vienen por defecto** (no marques ni desmarques nada) y apreta **Install**.
6. Espera a que termine (puede tardar varios minutos). Al final, **Next → Next → Finish**.

> 📸 *(Aquí irán capturas de las pantallas clave del instalador.)*
>
> ✅ No necesitas marcar la casilla "Add to PATH" si aparece una advertencia; déjala como viene.

---

## Paso 3 · Abrir Jupyter Notebook por primera vez

1. Abre el menú **Inicio** de Windows y escribe: **Anaconda Navigator**. Ábrelo.
   *(La primera vez puede demorar un poco en abrir.)*
2. En la ventana de Anaconda Navigator, busca el recuadro que dice **Jupyter Notebook** y apreta **Launch**.
3. Se abrirá automáticamente tu **navegador** (Chrome/Edge) con una pantalla que muestra carpetas de tu computador. **¡Eso es Jupyter!** 🎉

> 📸 *(Aquí irá una captura de Anaconda Navigator con el botón Launch, y otra de Jupyter abierto.)*
>
> ℹ️ Verás también que se abre una ventana negra (una "consola"). **No la cierres** mientras uses Jupyter: es el motor que lo mantiene andando. Al terminar, simplemente cierras todo.

---

## Paso 4 · Conseguir los materiales del curso

Te haremos llegar la carpeta del curso (con los notebooks y los datos). Tienes dos formas:

**Opción simple — carpeta comprimida:**
1. Descarga el archivo `.zip` del curso que te compartimos.
2. Descomprímelo (clic derecho → *Extraer todo*) en un lugar fácil de encontrar, por ejemplo en **Documentos**.

**Opción con Git (si ya manejas el repositorio):**
- Clona el repositorio y ubícate en la carpeta `curso/`.

En ambos casos, lo importante es saber **dónde quedó la carpeta**, porque en Jupyter tendrás que navegar hasta ella.

---

## Paso 5 · Abrir el notebook de la Sesión 1

1. En la pantalla de Jupyter (la del navegador), navega haciendo clic por las carpetas hasta llegar a donde dejaste los materiales del curso.
2. Entra a la carpeta `curso`.
3. Haz clic en el archivo **`01 - Sesion 1 - Hola Python.ipynb`**.
4. Se abrirá el cuaderno de la primera clase. 🎉

> 📸 *(Aquí irá una captura mostrando el archivo del notebook en la lista de Jupyter.)*

---

## Paso 6 · La prueba final (¡importante!)

Vamos a confirmar que todo funciona. Dentro del notebook de la Sesión 1:

1. Haz clic en la **primera celda de código** (la que dice `print("¡Hola!...")`).
2. Presiona **`Shift` + `Enter`** en el teclado.
3. Si abajo de la celda aparece el mensaje **"¡Hola! Si ves este mensaje abajo, Jupyter está funcionando."**, entonces **¡estás lista!** ✅

Si quieres una prueba extra de que las librerías están bien, crea una celda nueva, escribe esto y ejecútalo con `Shift`+`Enter`:

```python
import pandas as pd
print("pandas versión:", pd.__version__)
```

Si imprime un número de versión (por ejemplo `2.3.3`) sin errores en rojo, **todo está perfecto**.

---

## ¿Algo salió mal? Problemas frecuentes

| Síntoma | Qué hacer |
|---|---|
| El instalador de Anaconda se queda "pegado" | Cierra otros programas y dale tiempo; la instalación es pesada. |
| No encuentro "Anaconda Navigator" en Inicio | Espera unos minutos tras instalar, o reinicia el computador. |
| Jupyter no abre el navegador solo | Copia la dirección que aparece en la ventana negra (empieza con `http://localhost:8888...`) y pégala en Chrome/Edge. |
| Aparece texto en rojo al ejecutar una celda | No entres en pánico: copia el mensaje y mándalo al canal de ayuda. Casi siempre es algo simple. |
| `import pandas` da error | Avísanos; revisaremos que Anaconda haya quedado bien instalado. |

---

## (Opcional) ¿Y si prefiero VS Code?

Si alguien del equipo ya usa **VS Code**, también sirve para correr los notebooks:
1. Instala las extensiones **Python** y **Jupyter** (ambas de Microsoft) desde el panel de extensiones.
2. Abre la carpeta del curso con *Archivo → Abrir carpeta*.
3. Abre el archivo `.ipynb` y, si te lo pide, selecciona el intérprete de **Anaconda** como kernel.

> Para la clase usaremos Jupyter Notebook clásico (más simple para empezar), pero quien se sienta cómoda en VS Code puede usarlo sin problema.

---

✅ **Cuando hayas completado el Paso 6 con éxito, ¡estás lista para la Sesión 1!**
