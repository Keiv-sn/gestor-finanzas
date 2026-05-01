import flet as ft
import flet_charts as fch
from app.logic import formatear_moneda
from app.theme import BG_PRIMARY,BG_SECONDARY, ACCENT_YELLOW,TEXT_SECONDARY, ACCENT_GREEN
import app.theme as th



def navbar(navegar, vista_activa):

    def crear_boton(icono, etiqueta, ruta, especial=False):

        # El color del icono cambia si está activo
        es_activo = vista_activa == ruta
        color_icono = ACCENT_YELLOW if es_activo else TEXT_SECONDARY
        color_texto = ACCENT_YELLOW if es_activo else TEXT_SECONDARY

        # El botón especial (el "+") tiene un diseño diferente
        if especial:
            return ft.Container(
                content=ft.Icon(icono, color="white", size=24),
                bgcolor=ACCENT_GREEN,
                width=50,
                height=50,
                border_radius=25,
                alignment=ft.Alignment(0, 0),
                shadow=ft.BoxShadow(blur_radius=10, color=f"{th.BG_PRIMARY}4D"),
                on_click=lambda evento, dest=ruta: navegar(dest),
                margin=ft.margin.only(bottom=20)
            )
        
        # Para los botones normales, el fondo cambia si están activos
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icono, color=color_icono),
                    ft.Text(etiqueta, color=color_texto, size=10)
                ],
                alignment=ft.Alignment(0, 0),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=1
            ),
            expand=True,
            on_click=lambda _, e=ruta: navegar(e)
        )
    


    return ft.Container(
            bgcolor=BG_SECONDARY,
            height=80,
            padding=ft.padding.only(left=10, right=10, bottom=15),
            border_radius=ft.border_radius.only(top_left=25, top_right=25),
            content=ft.Row(
                [
                    crear_boton("home", "Dashboard", "dashboard"),
                    crear_boton("receipt_long", "transacciones", "transactions"),
                    crear_boton("add", "+", "add_transaction", especial=True),
                    crear_boton("account_balance_wallet", "Presupuestos", "budgets"), # aca podemos agregar barras graficas laterales
                    crear_boton("settings", "Más", "settings")
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            
        ),
    )


def grafico_gastos(gastos):

    secciones = []

    puntos_color = []
    nombres_cat = []
    porcentajes_cat = []

    colores = [th.ACCENT_ORANGE, th.TEXT_SECONDARY, th.ACCENT_YELLOW, th.ACCENT_RED, th.ACCENT_GREEN, th.BG_PRIMARY] # Paleta de colores para las categorías

    for i, gasto in enumerate(gastos): # la i 
        color_actual = colores[i % len(colores)] # Asigna un color de la paleta

        # gasto['total'] es el valor, gasto['categoria'] el nombre
        secciones.append(
            fch.PieChartSection(
                value=gasto["total"],
                color=colores[i % len(colores)],# Cicla colores si hay muchas categorías
                radius=15,
                title="",

                #tooltip=f"{gasto['nombre_categoria']}: {formatear_moneda(gasto['total'])} ({gasto['porcentaje']}%)"

            )
        )

        puntos_color.append(ft.Container(width=7, height=7, border_radius=4, bgcolor=color_actual))
        nombres_cat.append(ft.Text(gasto["nombre_categoria"][:10], size=10, color=th.TEXT_SECONDARY, overflow=ft.TextOverflow.ELLIPSIS))
        porcentajes_cat.append(ft.Text(f"{int(gasto['porcentaje'])}%", size=10, color="white", weight="bold"))


    if not secciones:
        secciones.append(fch.PieChartSection(value=1, color=th.TEXT_SECONDARY, radius=10))
    
    return {
        "secciones": secciones,
        "puntos": puntos_color,
        "nombres": nombres_cat,
        "porcentajes": porcentajes_cat
    }

"""
    → 5 botones en ft.Row
    → cada botón tiene ícono + label
    → el botón activo se ve destacado (color distinto)
    → el botón + es visualmente diferente (más grande, color acento)
    → fijo en la parte inferior de la pantalla
"""