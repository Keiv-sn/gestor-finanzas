from app.components import navbar
from app.auth import obtener_usuario_activo, cerrar_sesion
from app.components import card
from app.database import crear_cuenta, crear_categoria
from app.components import mostrar_error
import app.theme as th


import flet as ft



def settings_view(page, navegar, volver):



    usuario = obtener_usuario_activo()


    def limpiar_formulario_cuenta():
        campo_nombre_cuenta.value = ""
        dropdown_tipo_cuenta.value = None
        campo_saldo.value = ""

    def limpiar_formulario_categoria():
        campo_nombre_categoria.value = ""
        cambiar_tipo("gasto")


    def ocultar_formulario(formulario):
        formulario.visible = False
        page.update()



    def mostrar_formulario(formulario, limpiar=None):
        if limpiar:
            limpiar()

        formulario.visible = not formulario.visible
        page.update()


    def guardar_cuenta(e):

        nombre = campo_nombre_cuenta.value
        tipo = dropdown_tipo_cuenta.value

        numeros = "".join(filter(str.isdigit, campo_saldo.value))
        saldo = int(numeros) if numeros else 0

        success, mensaje = crear_cuenta(user_id=usuario["id"], name=nombre, account_type=tipo, balance=saldo, )

        if not nombre.strip():
            mostrar_error(page, "Ingrese un nombre para la cuenta.")
            return

        if not tipo:
            mostrar_error(page, "Seleccione un tipo de cuenta.")
            return

        if saldo < 0:
            mostrar_error(page, "El saldo no puede ser negativo.")
            return

        if success:
             limpiar_formulario_cuenta()
             ocultar_formulario(formulario_cuenta)
            
        else:
            mostrar_error(page, mensaje)



    def guardar_categoria(e):

        nombre = campo_nombre_categoria.value.strip()

        if not nombre:
            mostrar_error(page, "Ingrese un nombre.")
            return

        success, mensaje = crear_categoria(
            user_id=usuario["id"],
            name=nombre,
            category_type=switch_categoria["valor"],
        )

        if success:
            limpiar_formulario_categoria()
            ocultar_formulario(formulario_categoria)
        else:
            mostrar_error(page, mensaje)




    campo_nombre_cuenta = ft.TextField(
        hint_text="Nombre de la cuenta",
        bgcolor=th.BG_SECONDARY,
        color=th.TEXT_PRIMARY,
        border_color="transparent",
        text_size=th.FONT_SIZE_MD,
        content_padding=th.PADDING_MD,
    )


    dropdown_tipo_cuenta = ft.Dropdown(
        hint_text="Tipo",
        options=[
            ft.dropdown.Option("Efectivo"),
            ft.dropdown.Option("Cuenta corriente"),
            ft.dropdown.Option("Cuenta vista"),
            ft.dropdown.Option("Ahorro"),
            ft.dropdown.Option("Crédito"),
            ft.dropdown.Option("Otra")
        ],

        bgcolor=th.BG_SECONDARY,
        color=th.TEXT_PRIMARY,
        border_color="transparent",
        text_size=th.FONT_SIZE_MD,
        content_padding=th.PADDING_MD,
        expand=True
    )




    campo_saldo = ft.TextField(
        hint_text="$0",
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor=th.BG_SECONDARY,
        color=th.TEXT_PRIMARY,
        border_color="transparent",
        text_size=th.FONT_SIZE_MD,
        content_padding=th.PADDING_MD,
    )






    obetivos_ahorro = ft.Container(
        content=ft.Row(
            [
                ft.Text("Objetivos de ahorro",size=th.FONT_SIZE_SM, color=th.TEXT_PRIMARY,),

                ft.Image(
                    src="assets/icons/arrow_right.png",width=12, height=12, color=th.TEXT_SECONDARY,),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=th.PADDING_MD, vertical=12,),
        ink=True,
        on_click=lambda e: navegar("savings")
    )


    reportes = ft.Container(
        content=ft.Row(
            [
                ft.Text("Reportes",size=th.FONT_SIZE_SM, color=th.TEXT_PRIMARY,),

                ft.Image(
                    src="assets/icons/arrow_right.png",width=12, height=12, color=th.TEXT_SECONDARY,),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=th.PADDING_MD, vertical=12,),
        ink=True,
        on_click=lambda e: navegar("reports")
    )



    cuentas = ft.Container(
        content=ft.Row(
            [
                ft.Text("Añadir cuentas",size=th.FONT_SIZE_SM, color=th.TEXT_PRIMARY,),
                ft.Image(src="assets/icons/arrow_down.png",width=16, height=16, color=th.TEXT_SECONDARY,),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=th.PADDING_MD, vertical=12),
        ink=True,
        on_click=lambda e: mostrar_formulario(formulario_cuenta)
    )


    formulario_cuenta = ft.Container(
        visible=False,
        margin=ft.margin.only(left=20, right=12, bottom=10),
        content=ft.Column(
            [
                campo_nombre_cuenta,
                dropdown_tipo_cuenta,
                campo_saldo,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Cancelar",
                            on_click=lambda e:ocultar_formulario(formulario_cuenta),
                            style=ft.ButtonStyle(bgcolor=th.BG_PRIMARY, color=th.TEXT_PRIMARY, shape=ft.RoundedRectangleBorder(radius=12),)
                        ),
                        ft.ElevatedButton(
                            "Guardar",
                            on_click=guardar_cuenta,
                            style=ft.ButtonStyle(bgcolor=th.BG_PRIMARY, color=th.TEXT_PRIMARY, shape=ft.RoundedRectangleBorder(radius=12),)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ]
        ),
    )

###################################################################


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





    switch_categoria=ft.Container(
        ft.Row(
            [
                boton_gasto,
                boton_ingreso,
            ],
            spacing=0,
        ),
        bgcolor=th.BG_SECONDARY,
        border=ft.border.all(3, th.BG_SECONDARY),
        border_radius=th.BORDER_RADIUS,
        )



    campo_nombre_categoria = ft.TextField(
        hint_text="Nombre de la categoría",
        bgcolor=th.BG_SECONDARY,
        border_color="transparent",
        color=th.TEXT_PRIMARY,
        text_size=th.FONT_SIZE_MD,
        content_padding=th.PADDING_MD,
    )


    formulario_categoria = ft.Container(
        visible=False,
        margin=ft.margin.only(left=20, right=12, bottom=10),
        content=ft.Column(
            [
                campo_nombre_categoria,
                switch_categoria,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Cancelar",
                            on_click=lambda e:ocultar_formulario(formulario_categoria),
                            style=ft.ButtonStyle(bgcolor=th.BG_PRIMARY, color=th.TEXT_PRIMARY, shape=ft.RoundedRectangleBorder(radius=12),)
                        ),
                        ft.ElevatedButton(
                            "Guardar",
                            on_click=guardar_categoria,
                            style=ft.ButtonStyle(bgcolor=th.BG_PRIMARY, color=th.TEXT_PRIMARY, shape=ft.RoundedRectangleBorder(radius=12),)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ]
        ),
    )
    

    categorias = ft.Container(
        content=ft.Row(
            [
                ft.Text("Añadir categorias",size=th.FONT_SIZE_SM, color=th.TEXT_PRIMARY,),
                ft.Image(src="assets/icons/arrow_down.png",width=16, height=16, color=th.TEXT_SECONDARY,),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=th.PADDING_MD, vertical=12),
        ink=True,
        on_click=lambda e:mostrar_formulario(formulario_categoria, limpiar_formulario_categoria)
    )


    def mostrar_confirmacion(page, titulo, mensaje, on_confirmar):

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                titulo,
                color=th.TEXT_PRIMARY,
                size=th.FONT_SIZE_MD,
            ),
            content=ft.Text(
                mensaje,
                color=th.TEXT_SECONDARY,
            ),
            bgcolor=th.BG_PRIMARY,
            shape=ft.RoundedRectangleBorder(radius=th.BORDER_RADIUS),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: cerrar_dialogo(dialog, page),
                ),
                ft.TextButton(
                    "Confirmar",
                    on_click=lambda e: confirmar(dialog, page, on_confirmar),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()



    def cerrar_dialogo(dialog, page):
        dialog.open = False
        page.update()

        page.overlay.remove(dialog)


    def confirmar(dialog, page, accion):
        dialog.open = False
        page.update()

        page.overlay.remove(dialog)
        # Ejecutamos la acción después de cerrar visualmente el diálogo
        if accion:
            accion()


    bonton_cerrar=ft.ElevatedButton(
        "Cerrar sesión",
        on_click=lambda e: mostrar_confirmacion(
            page,
            "Cerrar sesión",
            "¿Deseas cerrar la sesión?",
            lambda: cerrar_sesion()
        ),
        style=ft.ButtonStyle(bgcolor=th.BG_PRIMARY, color=th.ACCENT_ORANGE, shape=ft.RoundedRectangleBorder(radius=12),)
        )


    
    contenido = ft.Column([

        

        ft.Row([
            ft.Container(
                content=ft.Image(
                src="assets/icons/back.png",
                width=28,
                height=16,
                color=th.TEXT_SECONDARY,
                ),
                border_radius=th.BORDER_RADIUS,
                padding=th.PADDING_SM,
                ink=True,
                on_click=lambda e: volver()
            ),
            ft.Container(
                ft.Text("Configuración", size=th.FONT_SIZE_LG, color=th.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                expand=True,
                ),

            ft.Container(width=48), #Espacio para centrar el titulo

            ],
        ),
    

        ft.Container(
            content=ft.Row(
                [
                    ft.Image(
                        src="assets/icons/user.png",
                        width=26,
                        height=26,
                        color=th.TEXT_SECONDARY,
                    ),

                    ft.Column(
                        [
                            ft.Text(
                                usuario["username"],
                                size=th.FONT_SIZE_MD,
                                color=th.TEXT_PRIMARY,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                usuario["email"],
                                size=th.FONT_SIZE_SM,
                                color=th.TEXT_SECONDARY,
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=th.PADDING_MD),
        ),

        ft.Divider(height=1, color=th.BG_SECONDARY),


        obetivos_ahorro,

        ft.Divider(height=1, color=th.BG_SECONDARY),

        reportes,

        ft.Divider(height=1, color=th.BG_SECONDARY),


        cuentas,
        formulario_cuenta,

        ft.Divider(height=1, color=th.BG_SECONDARY),

        categorias,
        formulario_categoria,

        ft.Divider(height=1, color=th.BG_SECONDARY),


        ft.Container(expand=True),


        ft.Container(
            (bonton_cerrar),
            padding=ft.padding.symmetric(horizontal=th.PADDING_MD),),

        



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
            content=navbar(navegar, "settings"),
            alignment=ft.Alignment.CENTER,
            bottom=0,
            left=0,
            right=0,
            height=60,
        )
    ],
    expand=True
)