# Medición de contraste en imágenes

Aplicación de escritorio en Python para seleccionar una imagen, elegir un método de medición (entropía o Sobel), configurar los parámetros del algoritmo genético y seleccionar una carpeta donde guardar el resultado. La interfaz muestra la imagen original y la mejorada. Llama a `main(image_path, measurement_method, algorithm_parameters, output_directory)`, que devuelve la ruta de la imagen procesada.

Los parámetros se envían en un diccionario con estos valores iniciales:

```python
{
    "N": 512,
    "Nc": 2,
    "Pc": 0.7,
    "Pm": 0.02,
    "Nm": 20,
    "Epochs": 15,
}
```

`N` debe ser par porque el cruzamiento del algoritmo trabaja con parejas. `Pc` y `Pm` aceptan valores entre 0 y 1; `N` y `Epochs` deben ser enteros positivos.

## Requisitos

- `uv`, que instalará las dependencias del proyecto y puede instalar Python si hace falta.
- El proyecto requiere Python `>=3.12,<3.13`.
- En Linux, Zenity para abrir el selector de archivos del escritorio.

## Instalar uv

Instala `uv` con el instalador oficial de Astral:

**macOS y Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Cierra y vuelve a abrir la terminal si `uv` no se reconoce. Comprueba la instalación:

```bash
uv --version
```

Más opciones están en la [guía oficial de instalación de uv](https://docs.astral.sh/uv/getting-started/installation/).

## Preparar y ejecutar el programa

Abre una terminal en la carpeta del proyecto, donde están `pyproject.toml` y `uv.lock`. Después ejecuta:

```bash
uv python install 3.12
uv sync
uv run python -m ui.flet_app
```

`uv sync` crea el entorno virtual local `.venv` e instala las versiones de dependencias registradas en `uv.lock`. También puedes iniciar directamente con `uv run python -m ui.flet_app`; `uv run` prepara el entorno del proyecto antes de ejecutar el programa.

No hace falta activar `.venv` ni instalar los paquetes con `pip`.

## Requisito adicional en Linux

Flet usa el selector de archivos del sistema. En Linux de escritorio necesita Zenity. En Ubuntu o Debian se instala con:

```bash
sudo apt-get install zenity
```

En otras distribuciones, instala el paquete `zenity` con el gestor de paquetes correspondiente. Este requisito no aplica al ejecutar la aplicación en el navegador.

Consulta la [documentación de FilePicker de Flet](https://flet.dev/docs/services/filepicker/) para más detalles.
