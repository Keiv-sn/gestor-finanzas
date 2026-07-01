
from app.components import mostrar_error, navbar
from app.auth import obtener_usuario_activo
from app.logic import obtener_comparativa, obtener_gastos_por_categoria, obtener_resumen, lista_meses, exportar_csv, exportar_excel
from app.components import grafico_gastos, card, formatear_moneda, mostrar_exito
import csv
import flet as ft
import flet_charts as fch
import app.theme as th





def report_view(page, navegar, volver):



    usuario = obtener_usuario_activo()

    meses = lista_meses()

    def archivo_seleccionado(e):
        if not e.path:
            return
        print(e.path)


    async def guardar_excel(e):

        ruta = await file_picker.save_file(
            file_name=f"reporte_{dropdown_mes.value}.xlsx"
        )

        if ruta is None:
            return

        exportar_excel(
            usuario["id"],
            dropdown_mes.value,
            ruta
        )

        mostrar_exito(page, "Archivo Excel exportado correctamente.")



    async def guardar_csv(e):

        ruta = await file_picker.save_file(
            file_name=f"reporte_{dropdown_mes.value}.csv"
        )

        if ruta is None:
            return

        exportar_csv( usuario["id"], dropdown_mes.value, ruta)

        mostrar_exito(page, "Archivo csv exportado correctamente.")



    def actualizar_mes(e):
        cargar_grafico()
        cargar_resumen()
        page.update()



    def cargar_grafico():

        gastos = obtener_gastos_por_categoria(
            usuario["id"],
            dropdown_mes.value
        )

        datos_grafico = grafico_gastos(gastos)

        grafico.content = card(
            ft.Column(
                [
                    ft.Text(
                        "Gastos por categoría",
                        size=th.FONT_SIZE_MD,
                        color=th.TEXT_PRIMARY,
                    ),

                    ft.Container(
                        height=100,
                        alignment=ft.Alignment(0, 0),
                        content=fch.PieChart(
                            sections=datos_grafico["secciones"],
                            sections_space=2,
                            center_space_radius=45,
                            expand=True,
                        ),
                    ),

                    ft.Column(
                        controls=datos_grafico["leyenda"],
                        spacing=8,
                    ),
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
                    ft.Text("Resumen del mes",  size=th.FONT_SIZE_MD,color=th.TEXT_PRIMARY,),

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
        filas = [ft.Text("Últimos meses")]

        for mes in datos:
            filas.append(
                ft.Row(
                    [
                        ft.Text(mes["mes"]),
                        ft.Text(formatear_moneda(mes["balance"]))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )

        comparativa.content = card(
            ft.Column(filas)
        )






    dropdown_mes = ft.Dropdown(
        value=meses[0],
        options=[ft.dropdown.Option(m) for m in meses],
        bgcolor=th.BG_SECONDARY,
        color=th.TEXT_PRIMARY,
        text_size=th.FONT_SIZE_SM,
        border_radius=th.BORDER_RADIUS,
        content_padding=th.PADDING_SM,
        margin=ft.margin.symmetric(horizontal=th.PADDING_MD),
        border_color="transparent",
        on_select=actualizar_mes,
        height=32,
        
    )

    grafico = ft.Container()

    resumen = ft.Container()

    comparativa = ft.Container()


    file_picker = ft.FilePicker()


    boton_csv = ft.ElevatedButton(
    "Exportar CSV",
    on_click=guardar_csv,
    )

    boton_excel = ft.ElevatedButton(
    "Exportar Excel",
    on_click=guardar_excel,
)



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



        dropdown_mes,

        ft.Container(height=0),

        grafico,

        resumen,

        ft.Divider(height=1, color=th.BG_SECONDARY),

        comparativa,

        card(
            ft.Column(
                [
                    ft.Text("Exportar datos"),

                    ft.Row(
                        [
                            boton_csv,
                            boton_excel
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