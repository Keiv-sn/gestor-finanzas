from app.auth import obtener_usuario_activo
from app.components import navbar, grafico_gastos
from app.logic import formatear_moneda, obtener_gastos_por_categoria, obtener_resumen, obtener_resumen_ahorro
from app.utils import obtener_mes_actual
from app.database import obtener_transacciones
import flet as ft
import flet_charts as fch
import app.theme as th


def dashboard_view(page, navegar, volver):
    
    usuario = obtener_usuario_activo()
    mes = obtener_mes_actual()
    resumen = obtener_resumen(usuario["id"], mes)
    ahorros = obtener_resumen_ahorro(usuario["id"])
    gastos = obtener_gastos_por_categoria(usuario["id"], mes)

    top_gastos = gastos[:4] # obtenemos solo las 4 categorías con más gastos para mostrar en el gráfico

    datos_grafico = grafico_gastos(top_gastos)

    # Para mostrar el primer objetivo de ahorro (si existe)
    primer_objetivo = ahorros[0] if ahorros else None

    if primer_objetivo:
        
        # Este es el contenedor que REEMPLAZA al ft.Text
        bloque_ahorro = ft.Container(
            bgcolor=th.BG_SECONDARY,
            border_radius=th.BORDER_RADIUS,
            padding=th.PADDING_MD,
            content=ft.Column([
                ft.Text("Objetivos de Ahorro", size=th.FONT_SIZE_MD , color=th.TEXT_SECONDARY),
                ft.Row([
                    ft.Text(f"{formatear_moneda(primer_objetivo['current_amount'])} / {formatear_moneda(primer_objetivo['target_amount'])}", size=th.FONT_SIZE_SM, color="white"),
                    ft.Text(primer_objetivo['nombre_objetivo'].upper(), size=th.FONT_SIZE_SM, color=th.TEXT_SECONDARY),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                # Barra de progreso manual 
                ft.ProgressBar(
                    value=primer_objetivo['porcentaje'] / 100, 
                    bgcolor=th.ACCENT_YELLOW,
                    color=th.ACCENT_YELLOW,
                    border_radius=10,
                    height=8
                )
            ], spacing=8)
        )
    else:
        bloque_ahorro = ft.Container(content=ft.Text("Sin objetivos activos", color=th.TEXT_SECONDARY))

    #Contenido dashboard(bento)

    contenido = ft.Column(
        [
            ft.Row([
                ft.Text(f"Hola, {usuario['username']} 👋", size=th.FONT_SIZE_LG, color=th.TEXT_PRIMARY)],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Balance Total", size=th.FONT_SIZE_MD, color=th.TEXT_SECONDARY),
                    ft.Text(formatear_moneda(resumen["saldo_total_cuentas"]), size=th.FONT_SIZE_XL, color=th.ACCENT_YELLOW)]),
                        bgcolor=th.BG_SECONDARY,
                        border_radius=th.BORDER_RADIUS, 
                        padding=th.PADDING_MD
            ),


            bloque_ahorro,



            ft.Row([

                ft.Container(
                    expand=1,
                    bgcolor=th.BG_SECONDARY,
                    border_radius=th.BORDER_RADIUS,
                    padding=th.PADDING_SM,
                    content=ft.Column([
                        ft.Text("Gastos por categoría", size=th.FONT_SIZE_MD, color=th.TEXT_SECONDARY),
                        ft.Container(
                            height=100, # Altura fija para la gráfica
                            content=fch.PieChart(
                                sections=datos_grafico["secciones"],
                                sections_space=2,
                                center_space_radius=45, # Esto lo hace tipo "Dona"
                                expand=True,
                            ),
                            alignment=ft.Alignment(0, 0)
                        ),
                        
                        
                        ft.Row([
                            ft.Column(controls=datos_grafico["puntos"], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER),

                            ft.Column(controls=datos_grafico["nombres"], spacing=10, expand=True),

                            ft.Column(controls=datos_grafico["porcentajes"], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.END),

                            ],alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
                        ])
                        
                    ),
                        
                ft.Container(
                    expand=1,
                    bgcolor=th.BG_SECONDARY,
                    border_radius=th.BORDER_RADIUS,
                    padding=th.PADDING_SM,
                    content=ft.Column([
                        ft.Text("Transacciones recientes", size=th.FONT_SIZE_MD, color=th.TEXT_SECONDARY),


                        ])
                        
                ),
            ]),


            ft.Container(content=ft.Text("Limite")),

            ft.Container(height=40) # Espacio para que la nav no tape nada
        ],

        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=10
    )

    # Devuelves el Stack que junta ambos componentes
    return ft.Stack(
        [
                # EL CUERPO: Usamos padding abajo para que el contenido NUNCA quede detrás de la nav
                ft.Container(
                    content=contenido, 
                    padding=ft.padding.only(bottom=85), # Ajusta este número al alto de tu navbar
                    expand=True
                ),
                
                # LA NAVBAR: Posicionada con 'bottom=0' para que flote siempre abajo
                ft.Container(
                    content=navbar(page, navegar),
                    bottom=0,
                    left=0,
                    right=0
                )
            ],
            expand=True
        )


#horizontal_alignment=ft.CrossAxisAlignment.STRETCH # Hace que ocupen todo el ancho