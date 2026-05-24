
from datetime import datetime

from app.auth import obtener_usuario_activo
from app.database import obtener_cuentas, obtener_categorias, crear_transaccion
import app.theme as th
import flet as ft
from app.components import card
from app.utils import formatear_moneda





def add_transaction_view(page, navegar, volver):

    usuario = obtener_usuario_activo()
    cuentas = obtener_cuentas(usuario["id"])
    categorias_gasto   = obtener_categorias(usuario["id"], "gasto")
    categorias_ingreso = obtener_categorias(usuario["id"], "ingreso")

    def al_cambiar_monto(e):

        valor = e.control.value

        numeros = "".join(filter(str.isdigit, valor))

        if numeros == "":
            e.control.value = "$0"
        else:
            e.control.value = formatear_moneda(int(numeros))

        page.update()


    tipo_transaccion = {"valor": "gasto"}

    def cambiar_tipo(tipo):

        tipo_transaccion["valor"] = tipo

        if tipo == "gasto":
            boton_gasto.bgcolor = th.ACCENT_ORANGE
            boton_ingreso.bgcolor = "transparent"

        else:
            boton_ingreso.bgcolor = th.ACCENT_GREEN
            boton_gasto.bgcolor = "transparent"

        page.update()




    texto_fecha = ft.Text(
        datetime.now().strftime("%d/%m/%Y"),
        color=th.TEXT_PRIMARY,
        size=th.FONT_SIZE_MD,
    )


    def cambiar_fecha(e):

        if date_picker.value:
            texto_fecha.value = date_picker.value.strftime("%d/%m/%Y")
            page.update()


    date_picker = ft.DatePicker(
        on_change=cambiar_fecha,
        
    )




    boton_gasto = ft.Container(
    content=ft.Text(
        "Gasto 💸",
        color=th.TEXT_PRIMARY
    ),
    padding=10,
    border_radius=th.BORDER_RADIUS,
    bgcolor=th.ACCENT_ORANGE,
    expand=True,
    alignment=ft.Alignment(0, 0),
    on_click=lambda e: cambiar_tipo("gasto")
    )

    boton_ingreso = ft.Container(
        content=ft.Text(
            "Ingreso 💵",
            color=th.TEXT_PRIMARY
        ),
        padding=10,
        border_radius=th.BORDER_RADIUS,
        bgcolor="transparent",
        expand=True,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: cambiar_tipo("ingreso")
    )

    contenido = ft.Column([

        ft.Text("Nueva Transaccion", size=th.FONT_SIZE_LG, color=th.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                  
        ft.Container(

            ft.Row([       
                boton_gasto,
                boton_ingreso         
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            border=ft.border.all(3, th.BG_SECONDARY),
            bgcolor=th.BG_SECONDARY,
            border_radius=th.BORDER_RADIUS,
            margin=ft.margin.symmetric(horizontal=th.PADDING_MD),
        ),

        ft.TextField(
            hint_text="$ 0",
            on_change=al_cambiar_monto,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_align=ft.TextAlign.CENTER,
            text_size=th.FONT_SIZE_XL,
            height=120,
            width=300,
            border_color=th.BG_SECONDARY,
            margin=ft.margin.symmetric(horizontal=th.PADDING_MD),
            hint_style=ft.TextStyle(color=th.TEXT_SECONDARY),
            color= th.TEXT_SECONDARY
        ),


            
        card(
            ft.Row([

                ft.Image(src="assets/icons/menu.png",width=20,height=20,fit="contain", color=th.TEXT_SECONDARY),

                ft.Dropdown(
                    hint_text="Categoría",
                    options=[],
                    bgcolor=th.BG_SECONDARY,
                    color=th.TEXT_PRIMARY,
                    text_size=th.FONT_SIZE_MD,
                    height=40,
                    content_padding=th.PADDING_MD,
                    border_color="transparent",
                    expand=True
                        )

                
                ])
            ),


        card(
            ft.Row([

                ft.Image(src="assets/icons/description.png",width=20,height=20,fit="contain", color=th.TEXT_SECONDARY),

                ft.TextField(
                    hint_text="Descripción",
                    text_size=th.FONT_SIZE_MD,
                    multiline=False,
                    border_color="transparent",
                    color=th.TEXT_PRIMARY,
                    filled=True,
                    bgcolor=th.BG_SECONDARY,
                    content_padding=th.PADDING_MD,
                    height=40,
                    expand=True
                    )
                ])
            ),


        card(
            ft.Row([

                ft.Image(src="assets/icons/card.png",width=20,height=20,fit="contain", color=th.TEXT_SECONDARY),
            
            

                ft.Dropdown(
                    hint_text="Cuenta",
                    options=[],
                    bgcolor=th.BG_SECONDARY,
                    color=th.TEXT_PRIMARY,
                    text_size=th.FONT_SIZE_MD,
                    height=40,
                    content_padding=th.PADDING_MD,
                    border_color="transparent",
                    expand=True
                    )
                ])
            ),


        card(
             ft.Container(            
                ft.Row([
                    ft.Image(src="assets/icons/calendar.png",width=20,height=20,fit="contain", color=th.TEXT_SECONDARY),

                    texto_fecha,
                    

                    ],
                    spacing=30,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ), 
                    padding=ft.padding.symmetric(vertical=8)
                ),
                on_click=lambda e: page.show_dialog(date_picker)
                
            ),



        card(

            ft.Text("Guardar", size=th.FONT_SIZE_LG, color=th.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),



            bgcolor=th.ACCENT_GREEN,
            border_radius=th.BORDER_RADIUS,
            margin=ft.margin.symmetric(horizontal=th.PADDING_MD),
            padding=12,
            alignment=ft.Alignment(0, 0),

            on_click=lambda e: guardar_transaccion()
        ),        
        
        ],
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    return contenido


"""
┌────────────────────┐
│ ← Nueva Transacción│
│                    │
│ [Gasto][Ingreso]   │
│                    │
│      $ 25.000      │
│                    │
│ [ Categoría ▼ ]    │
│ [ Descripción ]    │
│ [ Cuenta ▼ ]       │
│ [ Fecha ▼ ]        │
│                    │
│ [ Guardar ]        │
└────────────────────┘

"""