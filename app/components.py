import flet as ft
import flet_charts as fch
from app.theme import BG_PRIMARY,BG_SECONDARY,TEXT_SECONDARY, ACCENT_GREEN,TEXT_PRIMARY
import app.theme as th
from app.utils import formatear_moneda



def navbar(navegar, vista_activa):
    
    def crear_boton(icono_path: str, etiqueta, ruta, especial=False):
        es_activo = vista_activa == ruta
        color_icono = ACCENT_GREEN if es_activo else TEXT_PRIMARY
        color_texto = ACCENT_GREEN if es_activo else TEXT_PRIMARY

        if especial:
            return ft.Container(
                content=ft.Image(src=icono_path,width=32,height=32,fit="contain", color=TEXT_SECONDARY),
                bgcolor=ACCENT_GREEN,
                width=45,
                height=45,
                border_radius=20,
                alignment=ft.Alignment(0, 0),
                shadow=ft.BoxShadow(blur_radius=100, color="#00000050"),
                on_click=lambda e, dest=ruta: navegar(dest),
                ink=True,
            )

        # Botones normales

        return ft.Container(
            content=ft.Column(
                [
                    ft.Image(src=icono_path,width=20,height=20,fit="contain", color=color_icono),
                    ft.Text(etiqueta, color=color_texto, size=10, weight="w500")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=3,
            ),
            padding=ft.Padding.symmetric(vertical=8),
            border_radius=th.BORDER_RADIUS,
            bgcolor=BG_SECONDARY,
            expand=True,
            ink=True,                    # ← importante para feedback visual
            on_click=lambda _, dest=ruta: navegar(dest),
        )

    return ft.Container(
        bgcolor=BG_SECONDARY,
        height=50,
        padding=ft.padding.only(left=3, right=3, bottom=2, top=2),
        border_radius=ft.border_radius.all(20),
        
        content=ft.Row(
            [
                crear_boton("assets/icons/home.png", "Inicio", "dashboard"),
                crear_boton("assets/icons/transacciones.png", "Transacciones", "transactions"),
                crear_boton("assets/icons/add.png", "+", "add_transaction", especial=True),
                crear_boton("assets/icons/presupuestos.png", "Presupuestos", "budgets"),
                crear_boton("assets/icons/settings.png", "Más", "settings")
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            expand=True,
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



def fila_transaccion(t):

    es_ingreso = t["transaction_type"] == "ingreso"
    color_monto = th.ACCENT_GREEN if es_ingreso else th.ACCENT_RED
    signo = "+" if es_ingreso else "-"

    return ft.Row(
        [
            ft.Column(
                [
                    ft.Text(t["description"], color=th.TEXT_PRIMARY, size=th.FONT_SIZE_SM),
                    ft.Text(f"{signo}{formatear_moneda(t['amount'])}", color=color_monto, size=th.FONT_SIZE_SM)
                ]
            ),
            ft.Column(
                [
                    ft.Text(signo, color= color_monto, size= th.FONT_SIZE_MD,text_align=ft.TextAlign.RIGHT,weight="w600",)
                ]
            
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )



def card(contenido,padding=th.PADDING_MD,on_click=None):

    return ft.Container(
        content=contenido,
        bgcolor=th.BG_SECONDARY,
        border_radius=th.BORDER_RADIUS,
        margin=ft.margin.symmetric(horizontal=th.PADDING_MD),
        expand=True,
        padding=th.PADDING_SM,
        shadow=ft.BoxShadow(blur_radius=12, spread_radius=1, color="#00000030"),
        on_click=on_click
    )

"""
    → 5 botones en ft.Row
    → cada botón tiene ícono + label
    → el botón activo se ve destacado (color distinto)
    → el botón + es visualmente diferente (más grande, color acento)
    → fijo en la parte inferior de la pantalla
"""