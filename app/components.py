import flet as ft
from theme import BG_PRIMARY,BG_SECONDARY, ACCENT_YELLOW,TEXT_SECONDARY, ACCENT_GREEN


def navbar(page,navegar, vista_activa):

    def crear_boton(icono, etiqueta, ruta, especial=False):

        # El color del icono cambia si está activo
        es_activo = vista_activa == ruta
        color_icono = ACCENT_YELLOW if es_activo else TEXT_SECONDARY
        color_texto = ACCENT_YELLOW if es_activo else TEXT_SECONDARY

        # El botón especial (el "+") tiene un diseño diferente
        if especial:
            return ft.Container(
                content=ft.Icon(name=icono, color="white", size=24),
                bgcolor=ACCENT_GREEN,
                width=50,
                height=50,
                border_radius=25,
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.3, "black")),
                on_click=lambda evento, dest=ruta: navegar(dest),
                margin=ft.margin.only(bottom=20)
            )
        
        # Para los botones normales, el fondo cambia si están activos
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(name=icono, color=color_icono),
                    ft.Text(etiqueta, color=color_texto, size=10)
                ],
                alignment=ft.alignment.center,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=1
            ),
            expand=True,
            on_click=lambda _, e=ruta: navegar(e)
        )
    


    page.bottom_appbar = ft.BottomAppBar(
            bgcolor=BG_SECONDARY,
            height=80,
            padding=ft.padding.only(left=10, right=10, bottom=15),
            border_radius=ft.border_radius.only(top_left=25, top_right=25),
            content=ft.Row(
            [
                crear_boton("home", "Dashboard", "dashboard"),
                crear_boton("receipt_long", "transacciones", "transactions"),
                crear_boton("add", "+", "add_transaction", especial=True),
                crear_boton("account_balance_wallet", "Presupuestos", "budgets"), # aca podemos agrgara barras graficas laterales
                crear_boton("settings", "Más", "settings")
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
            
        ),
    )

    page.update()






"""
    → 5 botones en ft.Row
    → cada botón tiene ícono + label
    → el botón activo se ve destacado (color distinto)
    → el botón + es visualmente diferente (más grande, color acento)
    → fijo en la parte inferior de la pantalla
"""