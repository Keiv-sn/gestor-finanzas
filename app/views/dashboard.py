from app.auth import obtener_usuario_activo
from app.components import navbar, grafico_gastos, fila_transaccion
from app.logic import obtener_gastos_por_categoria, obtener_resumen, obtener_resumen_ahorro, obtener_alerta_limite 
from app.utils import obtener_mes_actual
from app.database import obtener_transacciones
from app.utils import formatear_moneda
import flet as ft
import flet_charts as fch
import app.theme as th



def dashboard_view(page, navegar, volver):
    
    usuario = obtener_usuario_activo()
    mes = obtener_mes_actual()
    resumen = obtener_resumen(usuario["id"], mes)
    ahorros = obtener_resumen_ahorro(usuario["id"])
    gastos = obtener_gastos_por_categoria(usuario["id"], mes)

    transacciones = obtener_transacciones(user_id=usuario["id"], month=mes)
    ultimas = transacciones[:4]  # últimas 4

    top_gastos = gastos[:4] # obtenemos solo las 4 categorías con más gastos para mostrar en el gráfico

    datos_grafico = grafico_gastos(top_gastos)

    # Para mostrar el primer objetivo de ahorro (si existe)
    primer_objetivo = ahorros[0] if ahorros else None

    if primer_objetivo:
        
        # Este es el contenedor que REEMPLAZA al ft.Text
        bloque_ahorro = ft.Container(
            expand=True,
            bgcolor=th.BG_SECONDARY,
            border_radius=th.BORDER_RADIUS,
            padding=th.PADDING_MD,
            height=90,
            content=ft.Column([
                ft.Text("Objetivos de Ahorro", size=th.FONT_SIZE_MD , color=th.TEXT_SECONDARY),
                ft.Row([
                    ft.Text(f"{formatear_moneda(primer_objetivo['current_amount'])} / {formatear_moneda(primer_objetivo['target_amount'])}", size=th.FONT_SIZE_SM, color="white"),
                    ft.Text(primer_objetivo['nombre_objetivo'].upper(), size=th.FONT_SIZE_SM, color=th.TEXT_SECONDARY),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                # Barra de progreso manual 
                ft.ProgressBar(
                    value=primer_objetivo['porcentaje'] / 100, 
                    bgcolor=th.BG_PRIMARY,
                    color=th.ACCENT_YELLOW,
                    border_radius=10,
                    height=8
                )
            ], spacing=8),

        )
    else:
        bloque_ahorro = ft.Container(content=ft.Text("", color=th.TEXT_SECONDARY))



    alerta_limite  = obtener_alerta_limite( usuario["id"], mes)


    if alerta_limite:

        bloque_limite = ft.Container(
            bgcolor=th.BG_SECONDARY,
            border_radius=th.BORDER_RADIUS,
            padding=th.PADDING_MD,
            content=ft.Column(
                [
                    ft.Text(
                        "Límite de presupuesto",
                        size=th.FONT_SIZE_MD,
                        color=th.TEXT_SECONDARY,
                    ),

                    ft.Text(
                        f"{alerta_limite['categoria']} ha alcanzado el "
                        f"{alerta_limite['porcentaje']}% del presupuesto.",
                        color=th.TEXT_PRIMARY,
                    ),

                    ft.ProgressBar(
                        value=alerta_limite["porcentaje"] / 100,
                        color=th.ACCENT_RED,
                        bgcolor=th.BG_PRIMARY,
                        height=8,
                        border_radius=10,
                    ),
                ],
                spacing=8,
            ),
        )

    else:
        bloque_limite = None

    #Contenido dashboard(bento)

    contenido = ft.Column(
        [
            ft.Row([
                ft.Text(f"Hola, {usuario['username']} 👋", size=th.FONT_SIZE_LG, color=th.TEXT_PRIMARY)],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            
            ft.Container(
                expand=True,
                bgcolor=th.BG_SECONDARY,
                border_radius=th.BORDER_RADIUS, 
                padding=th.PADDING_MD,
                content=ft.Column([
                    ft.Text("Balance Total", size=th.FONT_SIZE_MD, color=th.TEXT_SECONDARY),
                    ft.Text(formatear_moneda(resumen["saldo_total_cuentas"]), size=th.FONT_SIZE_XL, color=th.ACCENT_YELLOW)
                    ], 
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    )
            ),


            bloque_ahorro,



            ft.Row([

                ft.Container(
                    expand=1,
                    bgcolor=th.BG_SECONDARY,
                    border_radius=th.BORDER_RADIUS,
                    padding=th.PADDING_SM,
                    content=ft.Column([
                        ft.Text("Gastos por categoría", size=th.FONT_SIZE_SM, color=th.TEXT_SECONDARY),
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
                        
                        
                        ft.Column(
                            controls=datos_grafico["leyenda"],
                            spacing=8,
                        ),
                    ]
                ),
            ),
                ft.Container(
                    expand=1,
                    bgcolor=th.BG_SECONDARY,
                    border_radius=th.BORDER_RADIUS,
                    padding=th.PADDING_SM,
                    content=ft.Column([
                        ft.Text("Transacciones recientes", size=th.FONT_SIZE_SM, color=th.TEXT_SECONDARY),
                         ft.ListView(
                             
                             controls=[fila_transaccion(t) for t in ultimas],
                             spacing=10,
                             expand=True
                             
                         )
                        ])
                        
                ),
            ]),


            *([bloque_limite] if bloque_limite else []),



            ft.Container(height=10) # Espacio para que la nav no tape nada
        ],

        scroll=ft.ScrollMode.AUTO,
        expand=1,
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH
    )

    # Devuelves el Stack que junta ambos componentes
    return ft.Stack(
        [
                # EL CUERPO: Usamos padding abajo para que el contenido NUNCA quede detrás de la nav
                ft.Container(
                    content=contenido, 
                        padding=ft.padding.only(
                            left=th.PADDING_MD,
                            right=th.PADDING_MD,
                            top=th.PADDING_SM,
                            bottom=85,
                            ),
                    expand=True
                ),
                
                # LA NAVBAR: Posicionada con 'bottom=0' para que flote siempre abajo
                ft.Container(
                    content=navbar(navegar, "dashboard"),
                    alignment=ft.Alignment.CENTER,
                    bottom=0,
                    left=0,
                    right=0,
                    height=60,
                )
            ],
            expand=True
        )


#horizontal_alignment=ft.CrossAxisAlignment.STRETCH # Hace que ocupen todo el ancho