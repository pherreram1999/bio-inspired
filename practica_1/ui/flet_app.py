"""Interfaz Flet para medir y visualizar imágenes.

Desde la raíz del proyecto se inicia con:
    uv run python -m ui.flet_app
"""

import asyncio
from io import BytesIO
import math

import flet as ft
from PIL import Image as PillowImage

from main import main as run_measurement


DEFAULT_PARAMETERS = {
    "N": 512,
    "Nc": 2,
    "Pc": 0.7,
    "Pm": 0.02,
    "Nm": 20,
    "Epochs": 15,
}

TRANSPARENT_PIXEL = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="


def read_preview_bytes(image_path: str) -> bytes:
    """Convierte una imagen compatible con Pillow a PNG para la vista previa."""
    buffer = BytesIO()
    with PillowImage.open(image_path) as image:
        image.convert("RGB").save(buffer, format="PNG")
    return buffer.getvalue()


def main(page: ft.Page):
    page.title = "Medición de contraste"
    page.window.width = 1200
    page.window.height = 840
    page.window.resizable = True
    page.window.maximizable = True
    page.scroll = ft.ScrollMode.AUTO

    file_picker = ft.FilePicker()
    selected_path = ft.TextField(label="Ruta de la imagen", read_only=True, expand=True)
    output_directory = ft.TextField(
        label="Carpeta para guardar la imagen procesada",
        read_only=True,
        expand=True,
    )
    result_path = ft.TextField(
        label="Ruta de la imagen mejorada",
        read_only=True,
        expand=True,
    )
    method_selector = ft.Dropdown(
        label="Método de medición",
        value="entropia",
        expand=True,
        options=[
            ft.DropdownOption(key="entropia", text="Entropía"),
            ft.DropdownOption(key="sobel", text="Sobel"),
        ],
    )

    n_field = ft.TextField(
        label="N · tamaño de población", value=str(DEFAULT_PARAMETERS["N"]), expand=True
    )
    nc_field = ft.TextField(
        label="Nc · índice de cruzamiento",
        value=str(DEFAULT_PARAMETERS["Nc"]),
        expand=True,
    )
    pc_field = ft.TextField(
        label="Pc · prob. de cruzamiento",
        value=str(DEFAULT_PARAMETERS["Pc"]),
        expand=True,
    )
    pm_field = ft.TextField(
        label="Pm · prob. de mutación",
        value=str(DEFAULT_PARAMETERS["Pm"]),
        expand=True,
    )
    nm_field = ft.TextField(
        label="Nm · índice de mutación",
        value=str(DEFAULT_PARAMETERS["Nm"]),
        expand=True,
    )
    epochs_field = ft.TextField(
        label="Epochs · ciclos",
        value=str(DEFAULT_PARAMETERS["Epochs"]),
        expand=True,
    )

    def preview_panel(title, placeholder_text):
        image = ft.Image(
            src=TRANSPARENT_PIXEL,
            height=280,
            expand=True,
            fit=ft.BoxFit.CONTAIN,
            visible=False,
        )
        placeholder = ft.Text(placeholder_text)
        panel = ft.Card(
            expand=True,
            content=ft.Container(
                expand=True,
                padding=16,
                content=ft.Column(
                    controls=[
                        ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            expand=True,
                            height=300,
                            alignment=ft.Alignment.CENTER,
                            bgcolor="#f2f4f7",
                            content=ft.Column(
                                controls=[placeholder, image],
                                expand=True,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ),
                    ],
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            )
        )
        return image, placeholder, panel

    source_image, source_placeholder, source_panel = preview_panel(
        "Imagen original", "La imagen seleccionada aparecerá aquí"
    )
    result_image, result_placeholder, result_panel = preview_panel(
        "Imagen mejorada", "El resultado aparecerá aquí al terminar"
    )

    status_icon = ft.Icon(ft.Icons.INFO_OUTLINE, color="#1d4ed8", size=24)
    status_message = ft.Text(
        "Selecciona una imagen y una carpeta de salida para comenzar.",
        color="#1e3a8a",
        weight=ft.FontWeight.BOLD,
        selectable=True,
        expand=True,
    )
    status_box = ft.Container(
        padding=14,
        bgcolor="#eff6ff",
        content=ft.Row(controls=[status_icon, status_message]),
    )

    def set_status(message, kind="info"):
        styles = {
            "info": ("#eff6ff", "#1d4ed8", ft.Icons.INFO_OUTLINE),
            "working": ("#fff7ed", "#c2410c", ft.Icons.AUTORENEW),
            "success": ("#ecfdf3", "#15803d", ft.Icons.CHECK_CIRCLE),
            "warning": ("#fffaeb", "#b54708", ft.Icons.WARNING_AMBER),
            "error": ("#fef3f2", "#b42318", ft.Icons.ERROR_OUTLINE),
        }
        background, foreground, icon = styles[kind]
        status_message.value = message
        status_message.color = foreground
        status_icon.icon = icon
        status_icon.color = foreground
        status_box.bgcolor = background

    run_button = ft.Button(
        content="Procesar imagen",
        icon=ft.Icons.PLAY_ARROW,
        height=50,
    )

    async def select_image(_):
        files = await file_picker.pick_files(
            dialog_title="Seleccionar imagen",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["png", "jpg", "jpeg", "bmp", "tif", "tiff"],
            allow_multiple=False,
        )
        if not files:
            return

        image_path = files[0].path
        if image_path is None:
            set_status("El selector no devolvió una ruta local.", "error")
            return

        try:
            source_image.src = await asyncio.to_thread(read_preview_bytes, image_path)
        except (OSError, ValueError) as error:
            set_status(f"No se pudo abrir la imagen: {error}", "error")
            return

        selected_path.value = image_path
        source_image.visible = True
        source_placeholder.visible = False
        result_image.src = TRANSPARENT_PIXEL
        result_image.visible = False
        result_placeholder.visible = True
        result_path.value = ""
        set_status("Imagen cargada. Elige la carpeta de salida.", "info")

    async def select_output_directory(_):
        path = await file_picker.get_directory_path(
            dialog_title="Elegir carpeta para guardar la imagen procesada"
        )
        if path:
            output_directory.value = path
            set_status("Carpeta de salida seleccionada.", "info")

    def collect_parameters():
        def positive_integer(field, name):
            try:
                value = int(field.value)
            except (TypeError, ValueError) as error:
                raise ValueError(f"{name} debe ser un número entero.") from error
            if value <= 0:
                raise ValueError(f"{name} debe ser mayor que cero.")
            return value

        def positive_index(field, name):
            try:
                value = float(field.value)
            except (TypeError, ValueError) as error:
                raise ValueError(f"{name} debe ser un número.") from error
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} debe ser mayor que cero.")
            return int(value) if value.is_integer() else value

        def probability(field, name):
            try:
                value = float(field.value)
            except (TypeError, ValueError) as error:
                raise ValueError(f"{name} debe ser un número entre 0 y 1.") from error
            if not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{name} debe estar entre 0 y 1.")
            return value

        population_size = positive_integer(n_field, "N")
        if population_size % 2 != 0:
            raise ValueError("N debe ser par porque el cruzamiento opera por parejas.")

        return {
            "N": population_size,
            "Nc": positive_index(nc_field, "Nc"),
            "Pc": probability(pc_field, "Pc"),
            "Pm": probability(pm_field, "Pm"),
            "Nm": positive_index(nm_field, "Nm"),
            "Epochs": positive_integer(epochs_field, "Epochs"),
        }

    async def execute_measurement(_):
        image_path = selected_path.value
        destination = output_directory.value
        if not image_path:
            set_status("Selecciona una imagen antes de procesar.", "warning")
            return
        if not destination:
            set_status("Selecciona una carpeta para guardar el resultado.", "warning")
            return

        try:
            algorithm_parameters = collect_parameters()
        except ValueError as error:
            set_status(str(error), "error")
            return

        run_button.disabled = True
        set_status("Procesando imagen. Esto puede tardar unos momentos...", "working")
        page.update()
        try:
            improved_image_path = await asyncio.to_thread(
                run_measurement,
                image_path,
                method_selector.value,
                algorithm_parameters,
                destination,
            )
            if not improved_image_path:
                set_status(
                    "El proceso terminó, pero main no devolvió la ruta de la imagen mejorada.",
                    "warning",
                )
                return

            improved_image_path = str(improved_image_path)
            result_bytes = await asyncio.to_thread(
                read_preview_bytes,
                improved_image_path,
            )
            result_image.src = result_bytes
            result_image.visible = True
            result_placeholder.visible = False
            result_path.value = improved_image_path
            set_status(
                f"Proceso terminado. Imagen mejorada guardada en: {improved_image_path}",
                "success",
            )
        except Exception as error:
            set_status(f"No se pudo completar el procesamiento: {error}", "error")
        finally:
            run_button.disabled = False

    run_button.on_click = execute_measurement

    page.add(
        ft.SafeArea(
            content=ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Medición de contraste",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    "Selecciona la imagen, ajusta el algoritmo y revisa el resultado."
                                ),
                            ],
                            spacing=2,
                        ),
                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(
                                    col={"xs": 12, "lg": 6},
                                    content=ft.Card(
                                        expand=True,
                                        content=ft.Container(
                                            padding=10,
                                            content=ft.Row(
                                                controls=[
                                                    selected_path,
                                                    ft.Button(
                                                        content="Seleccionar imagen",
                                                        icon=ft.Icons.IMAGE_SEARCH,
                                                        on_click=select_image,
                                                    ),
                                                ],
                                            ),
                                        ),
                                    ),
                                ),
                                ft.Container(
                                    col={"xs": 12, "lg": 6},
                                    content=ft.Card(
                                        expand=True,
                                        content=ft.Container(
                                            padding=10,
                                            content=ft.Row(
                                                controls=[
                                                    output_directory,
                                                    ft.Button(
                                                        content="Elegir carpeta",
                                                        icon=ft.Icons.FOLDER_OPEN,
                                                        on_click=select_output_directory,
                                                    ),
                                                ],
                                            ),
                                        ),
                                    ),
                                ),
                            ],
                            spacing=12,
                            run_spacing=4,
                        ),
                        ft.Card(
                            content=ft.Container(
                                padding=16,
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Configuración del algoritmo",
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.ResponsiveRow(
                                            controls=[
                                                ft.Container(
                                                    content=field,
                                                    col={"xs": 12, "sm": 6, "lg": 4},
                                                )
                                                for field in (
                                                    n_field,
                                                    nc_field,
                                                    pc_field,
                                                    pm_field,
                                                    nm_field,
                                                    epochs_field,
                                                )
                                            ],
                                            spacing=12,
                                            run_spacing=4,
                                        ),
                                        ft.ResponsiveRow(
                                            controls=[
                                                ft.Container(
                                                    content=method_selector,
                                                    col={"xs": 12, "md": 8},
                                                ),
                                                ft.Container(
                                                    content=run_button,
                                                    alignment=ft.Alignment.CENTER_RIGHT,
                                                    col={"xs": 12, "md": 4},
                                                ),
                                            ],
                                            spacing=12,
                                            run_spacing=4,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            )
                        ),
                        status_box,
                        ft.Text(
                            "Vista previa",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(content=source_panel, col={"xs": 12, "md": 6}),
                                ft.Container(content=result_panel, col={"xs": 12, "md": 6}),
                            ],
                            spacing=12,
                            run_spacing=4,
                        ),
                        result_path,
                    ],
                    spacing=12,
                    expand=True,
                ),
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
