
from app.components import mostrar_error, navbar
import flet as ft
from app.auth import obtener_usuario_activo
from app.components import card, card_objetivo
from app.database import  crear_objetivo_ahorro, obtener_objetivos_ahorro, eliminar_objetivo_ahorro, actualizar_progreso_ahorro, actualizar_objetivos_ahorro
import app.theme as th
from app.utils import formatear_moneda



def savings_view(page, navegar, volver):


    usuario = obtener_usuario_activo()
    
    objetivo_seleccionado = {"objetivo": None}

    lista_objetivos = ft.ListView(spacing=8, expand=True,)


    def eliminar_objetivo(objetivo_id):
        success, mensaje = eliminar_objetivo_ahorro(objetivo_id)

        if success:
            cargar_objetivos()
            page.update()
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(mensaje),
                action="Cerrar",
            )
            page.snack_bar.open = True
            page.update()



    def cargar_objetivos():

        objetivos = obtener_objetivos_ahorro(usuario["id"])

        lista_objetivos.controls.clear()

        for objetivo in objetivos:
            lista_objetivos.controls.append(
                card_objetivo(objetivo,  on_delete=eliminar_objetivo, on_aportar=aportar)
            )



    def aplicar_filtros(e=None):
        cargar_objetivos()
        page.update()



    def limpiar_formulario():
        nombre.value = ""
        campo_limite.value = ""
        date_picker.value = None
        texto_fecha.value = "Sin fecha límite"
        


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


    def aportar(objetivo):

        formulario.visible = False
        boton_nuevo.visible = True

        objetivo_seleccionado["objetivo"] = objetivo
        texto_objetivo.value = f'Aportar a "{objetivo["name"]}"'

        campo_aporte.value = ""

        formulario_aporte.visible = True
        page.update()



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


    campo_aporte=ft.TextField(
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




    boton_nuevo = ft.Container(
    content=ft.Text(
        "Nuevo objetivo",
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

    nombre = ft.TextField(
    label="Nombre",
    border_color=th.BG_SECONDARY,
    color=th.TEXT_PRIMARY,
    )

    texto_objetivo  = ft.Text(
    "",
    color=th.TEXT_PRIMARY,
    )


    texto_fecha = ft.Text(
    "Sin fecha límite",
    color=th.TEXT_PRIMARY,
    size=th.FONT_SIZE_MD,
    )

    seleccionar_fecha = ft.ElevatedButton(
    "Seleccionar fecha",
    icon=ft.Icons.CALENDAR_MONTH,
    on_click=lambda e: page.open(date_picker),
    )

    def cambiar_fecha(e):
        if date_picker.value:
            texto_fecha.value = date_picker.value.strftime("%d/%m/%Y")
            page.update()

    date_picker = ft.DatePicker(
        on_change=cambiar_fecha,
    )

    page.overlay.append(date_picker)


    def confirmar_aporte(e):

        numeros = "".join(filter(str.isdigit, campo_aporte.value))

        if not numeros:
            mostrar_error(page, "Ingrese un monto")
            return
        
        monto = int(numeros)

        if monto <= 0:
            mostrar_error(page, "El monto debe ser mayor a 0")
            return
        

        success, mensaje = actualizar_progreso_ahorro(
            objetivo_seleccionado["objetivo"]["id"],
            monto
        )

        if success:
            texto_objetivo.value = ""
            campo_aporte.value = ""
            objetivo_seleccionado["objetivo"] = None

            formulario_aporte.visible = False

            cargar_objetivos()
            page.update()

        else:
            mostrar_error(page, mensaje)


    def cancelar_aporte(e):
        campo_aporte.value = ""
        texto_objetivo.value = ""
        objetivo_seleccionado["objetivo"] = None
        formulario_aporte.visible = False
        page.update()







    def guardar_objetivo(e):

        deadline = None

        if date_picker.value:
            deadline = date_picker.value.strftime("%Y-%m-%d")


        if not campo_limite.value:
            return
            

        numeros = "".join(filter(str.isdigit, campo_limite.value))
        

        if not numeros:
            return
        

        amount_limit = int(numeros)

        if amount_limit <= 0:
            mostrar_error(page,"El monto debe ser mayor a 0")
            return
        
        if not nombre.value.strip():
            mostrar_error(page, "Ingrese un nombre para el objetivo")
            return
        


        success, mensaje = crear_objetivo_ahorro(    usuario["id"], nombre.value, amount_limit, deadline)


        if success:
            formulario.visible = False
            boton_nuevo.visible = True

            limpiar_formulario()
            cargar_objetivos()
            

        else:
            mostrar_error(page,mensaje)


        page.update()


    formulario_aporte = ft.Container(
        visible=False,
        content=card(
            ft.Column(
                [
                    texto_objetivo,

                    campo_aporte,

                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Cancelar",
                                on_click=cancelar_aporte,
                            ),
                            ft.ElevatedButton(
                                "Confirmar",
                                on_click=confirmar_aporte,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ]
            )
        )
    )



    formulario = ft.Container(
        visible=False,
        content=card(
            ft.Column(
                [
                    ft.Text(
                        "Objetivo de Ahorro",
                        size=th.FONT_SIZE_MD,
                        color=th.TEXT_PRIMARY,
                    ),

                    nombre,

                    campo_limite,

                    card(
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Image(
                                        src="assets/icons/calendar.png",
                                        width=20,
                                        height=20,
                                        fit="contain",
                                        color=th.TEXT_SECONDARY,
                                    ),
                                    texto_fecha,
                                ],
                                spacing=30,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=ft.padding.symmetric(vertical=8),
                        ),
                        on_click=lambda e: page.show_dialog(date_picker),
                    ),

                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Cancelar",
                                on_click=lambda e: ocultar_formulario(e),
                                style=ft.ButtonStyle(bgcolor=th.BG_PRIMARY, color=th.TEXT_PRIMARY, shape=ft.RoundedRectangleBorder(radius=12),)
                            ),
                            ft.ElevatedButton(
                                "Guardar",
                                on_click=guardar_objetivo,
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
                ft.Text("Objetivos de ahorro", size=th.FONT_SIZE_MD, color=th.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                expand=True
                ),

            ft.Container(width=48), #Espacio para centrar el titulo 

            ],
        ),

        ft.Container(
            content=card(lista_objetivos),
            expand=True
        ),

        boton_nuevo,

        formulario,

        formulario_aporte,



    ],expand=True)




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