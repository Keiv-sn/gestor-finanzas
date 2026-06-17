from datetime import datetime
from app.components import navbar
import flet as ft
from app.auth import obtener_usuario_activo
from app.components import card, card_fila_transaccion
from app.database import obtener_meses_con_transacciones, obtener_transacciones
import app.theme as th
from app.utils import formatear_moneda


def transactions_view(page, navegar, volver):

    usuario = obtener_usuario_activo()

    transacciones = obtener_transacciones(usuario["id"])

    controles = []


    meses = obtener_meses_con_transacciones(usuario["id"])


    lista_transacciones = ft.ListView(spacing=8, expand=True,)


    def aplicar_filtros(e=None):

        mes, año = dropdown_mes.value.split("/")
        month_sql = f"{año}-{mes}"

        tipo = None

        if dropdown_tipo.value != "Todos":
            tipo = dropdown_tipo.value

        resultado = obtener_transacciones(
            usuario["id"],
            month=month_sql,
            transaction_type=tipo
        )

        lista_transacciones.controls.clear()

        for t in resultado:
            lista_transacciones.controls.append(
                card_fila_transaccion(t)
            )

        if dropdown_tipo.value == "Todos":
            ingresos = sum(
                t["amount"]
                for t in resultado if t["transaction_type"] == "ingreso")
            
            gastos = sum(
                t["amount"]
                for t in resultado if t["transaction_type"] == "gasto")

            total = ingresos - gastos

        elif dropdown_tipo.value == "ingreso":

            total = sum(t["amount"] for t in resultado)

        else:  # gasto

            total = sum(t["amount"] for t in resultado)     

        texto_total.value = formatear_moneda(total)


        if e:
            page.update()


    dropdown_mes=ft.Dropdown(
        value=meses[0] if meses else None,
        options=[ft.dropdown.Option(mes) for mes  in meses],
        bgcolor=th.BG_SECONDARY,
        color=th.TEXT_PRIMARY,
        text_size=th.FONT_SIZE_SM,
        height=32,
        content_padding=th.PADDING_SM,
        border_color="transparent",
        width=120,
        on_select=aplicar_filtros,
        expand=True
  
        )



    dropdown_tipo = ft.Dropdown(
        value="Todos",
        options=[
            ft.dropdown.Option("Todos"),
            ft.dropdown.Option("gasto"),
            ft.dropdown.Option("ingreso"),
        ],
        bgcolor=th.BG_SECONDARY,
        color=th.TEXT_PRIMARY,
        text_size=th.FONT_SIZE_SM,
        height=32,
        content_padding=th.PADDING_SM,
        border_color="transparent",
        width=120,
        on_select=aplicar_filtros,
        expand=True
            )
    

    texto_total = ft.Text("0",size=th.FONT_SIZE_LG, color=th.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER)


    aplicar_filtros() # carga las transacciones del mes seleccionado al iniciar la vista

    contenido = ft.Column([

        ft.Row([
            ft.Container(
                content=ft.Image(
                src="assets/icons/back.png",
                width=32,
                height=16,
                color=th.TEXT_SECONDARY,
                ),
                border_radius=th.BORDER_RADIUS,
                padding=th.PADDING_SM,
                ink=True,
                on_click=lambda e: volver()
            ),
            ft.Container(
                ft.Text("Transacciones", size=th.FONT_SIZE_LG, color=th.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                expand=True
                ),

            ft.Container(width=48), #Espacio para centrar el titulo

            ],
        ),

        ft.Row(
            [
                ft.Container(
                    content=card(
                        ft.Row([
                            ft.Image(src="assets/icons/calendar.png", width=18, height=20, color=th.TEXT_SECONDARY,),
                            dropdown_mes,
                            
                        ],spacing=0),
                        margin=False,
                    ),
                    expand=True,
                    margin=ft.margin.only(left=th.PADDING_MD)
                ),

                ft.Container(
                    content=card(
                        ft.Row([
                            ft.Image(src="assets/icons/filter.png", width=18, height=18, color=th.TEXT_SECONDARY,),
                            dropdown_tipo,
                        ],spacing=0),
                        margin=False,
                    ),
                    expand=True,
                    margin=ft.margin.only(right=th.PADDING_MD),
                ),
            ],
        ),

        ft.Container(
            content=card(lista_transacciones),
            expand=True
        ),


        card(
            ft.Container(
                content=texto_total,
                alignment=ft.Alignment(0, 0),
                height=50,
            )
        )

    ],
    expand=True
    
    )

    return ft.Stack(
    [
        ft.Container(
            content=contenido,
            padding=ft.padding.only(bottom=65),
            expand=True
        ),

        ft.Container(
            content=navbar(navegar, "transactions"),
            alignment=ft.Alignment.CENTER,
            bottom=0,
            left=0,
            right=0,
            height=60,
        )
    ],
    expand=True
)