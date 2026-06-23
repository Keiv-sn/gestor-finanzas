
from app.components import mostrar_error, navbar
from app.auth import obtener_usuario_activo
from app.logic import obtener_comparativa, obtener_gastos_por_categoria, obtener_resumen, obtener_resumen_ahorro, lista_meses
from app.components import grafico_gastos, card, formatear_moneda
import flet as ft
import app.theme as th





def report_view(page, navegar, volver):


    usuario = obtener_usuario_activo()

    meses = lista_meses()


    def actualizar_mes(e):
        cargar_grafico()
        cargar_resumen()
        page.update()



    def cargar_grafico():

        gastos = obtener_gastos_por_categoria(
            usuario["id"],
            dropdown_mes.value
        )

        grafico.content = card(
            ft.Column(
                [
                    ft.Text("Gastos por categoría"),
                    grafico_gastos(gastos)
                ]
            )
        )


    def cargar_resumen():

        datos = obtener_resumen(
            usuario["id"],
            dropdown_mes.value
        )

        resumen.content = card(
            ft.Column(
                [
                    ft.Text("Resumen del mes"),

                    ft.Text(f"Ingresos: {formatear_moneda(datos['ingresos'])}"),

                    ft.Text(f"Gastos: {formatear_moneda(datos['gastos'])}"),

                    ft.Text(f"Balance: {formatear_moneda(datos['balance_neto_mensual'])}")
                ]
            )
        )


    def cargar_comparativa():

        datos = obtener_comparativa(usuario["id"])

        comparativa.content = card(
            ft.Column(
                [
                    ft.Text("Últimos meses")
                ]
            )
        )

        columna = comparativa.content.content

        for mes in datos:

            columna.controls.append(

                ft.Row(
                    [
                        ft.Text(mes["mes"]),

                        ft.Text(
                            formatear_moneda(mes["balance"])
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )

            )





    dropdown_mes = ft.Dropdown(
        value=meses[0],
        options=[ft.dropdown.Option(m) for m in meses],
        bgcolor=th.BG_SECONDARY,
        color=th.TEXT_PRIMARY,
        border_color="transparent",
        on_select=actualizar_mes,
    )

    grafico = ft.Container()

    resumen = ft.Container()

    comparativa = ft.Container()

















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
                ft.Text("Reporte", size=th.FONT_SIZE_MD, color=th.TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                expand=True
                ),

            ft.Container(width=48), #Espacio para centrar el titulo 

            ],
        ),



        card(dropdown_mes),

        grafico,

        resumen,

        comparativa,

        card(
            ft.Column(
                [
                    ft.Text("Exportar datos"),

                    ft.Row(
                        [
                            #boton_csv,
                            #boton_excel
                        ]
                    )
                ]
            )
        ),

      






    ],
    expand=True,
    scroll=ft.ScrollMode.AUTO,
    
    )

    cargar_grafico()
    cargar_resumen()
    cargar_comparativa()

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