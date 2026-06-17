from datetime import datetime
from app.components import mostrar_error, navbar
import flet as ft
from app.auth import obtener_usuario_activo
from app.components import card, card_presupuesto
from app.database import eliminar_presupuesto, obtener_categorias, obtener_presupuestos, crear_presupuesto
import app.theme as th
from app.utils import formatear_moneda, obtener_meses_presupuesto



def budgets_view(page, navegar, volver):

    usuario = obtener_usuario_activo()
    

    meses = obtener_meses_presupuesto()

    meses_adelante = obtener_meses_presupuesto(meses_atras=0, meses_adelante=6)


    categorias_gasto   = obtener_categorias(usuario["id"], "gasto")


    lista_presupuestos = ft.ListView(spacing=8, expand=True,)


    def eliminar(presupuesto_id):
        success, mensaje = eliminar_presupuesto(presupuesto_id)

        if success:
            cargar_presupuestos()
            page.update()
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(mensaje),
                action="Cerrar",
            )
            page.snack_bar.open = True
            page.update()



    def cargar_presupuestos():
        mes, año = dropdown_mes.value.split("/")
        month_sql = f"{año}-{mes}"

        presupuestos = obtener_presupuestos(usuario["id"], month_sql)

        lista_presupuestos.controls.clear()

        for presupuesto in presupuestos:
            lista_presupuestos.controls.append(
                card_presupuesto(presupuesto, on_delete=eliminar)
            )



    def aplicar_filtros(e=None):
        cargar_presupuestos()
        page.update()


    


    dropdown_mes=ft.Dropdown(
    value=f"{datetime.now().month:02d}/{datetime.now().year}",
    options=[ft.dropdown.Option(mes) for mes in meses],
    bgcolor=th.BG_SECONDARY,
    color=th.TEXT_PRIMARY,
    text_size=th.FONT_SIZE_MD,
    height=32,
    content_padding=th.PADDING_SM,
    border_color="transparent",
    #width=120,
    on_select=aplicar_filtros,
    expand=True
    )



    def limpiar_formulario():
        dropdown_categoria.value = None
        campo_limite.value = ""
        dropdown_mes_adelante.value = f"{datetime.now().month:02d}/{datetime.now().year}"


    def mostrar_formulario(e):
        limpiar_formulario()
        formulario.visible = True
        boton_nuevo.visible = False
        page.update()

    def ocultar_formulario(e):
        limpiar_formulario()
        formulario.visible = False
        boton_nuevo.visible = True
        page.update()


    def al_cambiar_monto(e):
        valor = e.control.value
        numeros = "".join(filter(str.isdigit, valor))

        if numeros == "":
            e.control.value = "$0"
        else:
            e.control.value = formatear_moneda(int(numeros))

        page.update()



    dropdown_categoria =ft.Dropdown(
    hint_text="Categoría",
    options=[ft.dropdown.Option(key=str(cat["id"]), text=cat["name"])for cat in categorias_gasto],
    bgcolor=th.BG_SECONDARY,
    color=th.TEXT_PRIMARY,
    text_size=th.FONT_SIZE_MD,
    height=40,
    content_padding=th.PADDING_MD,
    border_color="transparent",
    expand=True
    )


    campo_limite=ft.TextField(
    hint_text="$ 0",
    on_change=al_cambiar_monto,
    keyboard_type=ft.KeyboardType.NUMBER,
    text_align=ft.TextAlign.CENTER,
    text_size=th.FONT_SIZE_MD,
    height=35,
    width=300,
    border_color=th.BG_SECONDARY,
    margin=ft.margin.symmetric(horizontal=th.PADDING_MD),
    hint_style=ft.TextStyle(color=th.TEXT_SECONDARY),
    color= th.TEXT_SECONDARY
    )


    dropdown_mes_adelante=ft.Dropdown(
    value=f"{datetime.now().month:02d}/{datetime.now().year}",
    options=[ft.dropdown.Option(mes) for mes in meses_adelante],
    bgcolor=th.BG_SECONDARY,
    color=th.TEXT_PRIMARY,
    text_size=th.FONT_SIZE_MD,
    height=32,
    content_padding=th.PADDING_SM,
    border_color="transparent",
    #width=120,
    expand=True
    )


    boton_nuevo = ft.Container(
    content=ft.Text(
        "Nuevo presupuesto",
        size=th.FONT_SIZE_LG,
        color=th.TEXT_PRIMARY,
        text_align=ft.TextAlign.CENTER,
    ),
    bgcolor=th.ACCENT_GREEN,
    border_radius=th.BORDER_RADIUS,
    margin=ft.margin.symmetric(horizontal=th.PADDING_MD),
    padding=12,
    alignment=ft.Alignment(0, 0),
    on_click=mostrar_formulario
    )


    def guardar_presupuesto(e):

        if not dropdown_categoria.value:
            return

        if not campo_limite.value:
            return
            

        category_id = int(dropdown_categoria.value)

        numeros = "".join(filter(str.isdigit, campo_limite.value))
        

        if not numeros:
            return
        

        amount_limit = int(numeros)

        if amount_limit <= 0:
            mostrar_error(page,"El monto debe ser mayor a 0")
            return
        

        mes, año = dropdown_mes_adelante.value.split("/")
        month = f"{año}-{mes}"



        success, mensaje = crear_presupuesto(usuario["id"], category_id, amount_limit, month)


        if success:
            formulario.visible = False
            boton_nuevo.visible = True

            limpiar_formulario()
            cargar_presupuestos()
            

        else:
            mostrar_error(page,mensaje)


        page.update()





    formulario = ft.Container(
        visible=False,
        content=card(
            ft.Column(
                [
                    ft.Text(
                        "Crear presupuesto",
                        size=th.FONT_SIZE_MD,
                        color=th.TEXT_PRIMARY,
                    ),

                    dropdown_categoria,

                    campo_limite,

                    dropdown_mes_adelante,

                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Cancelar",
                                on_click=lambda e: ocultar_formulario(e),
                                style=ft.ButtonStyle(bgcolor=th.BG_PRIMARY, color=th.TEXT_PRIMARY, shape=ft.RoundedRectangleBorder(radius=12),)
                            ),
                            ft.ElevatedButton(
                                "Guardar",
                                on_click=guardar_presupuesto,
                                style=ft.ButtonStyle(bgcolor=th.BG_PRIMARY, color=th.TEXT_PRIMARY, shape=ft.RoundedRectangleBorder(radius=12),)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    )
                ],
                spacing=10,
            )
        )
    )






    aplicar_filtros()









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
                ft.Text("Presupuestos", size=th.FONT_SIZE_MD, color=th.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                expand=True
                ),

            dropdown_mes, 

            ],
        ),






        ft.Container(
            content=card(lista_presupuestos),
            expand=True
        ),




        boton_nuevo,

        formulario


    ],expand=True)




    return ft.Stack(
    [
        ft.Container(
            content=contenido,
            padding=ft.padding.only(bottom=65),
            expand=True
        ),

        ft.Container(
            content=navbar(navegar, "budgets"),
            alignment=ft.Alignment.CENTER,
            bottom=0,
            left=0,
            right=0,
            height=60,
        )
    ],
    expand=True
)