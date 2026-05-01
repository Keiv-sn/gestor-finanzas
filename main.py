from app.database import init_db
from app.auth import obtener_sesion_guardada
from app.views.dashboard import dashboard_view
from app.views.login import login_view
from app.views.add_transaction import add_transaction_view
from app.views.transactions import transactions_view
from app.views.budgets import budgets_view
from app.views.register import register_view
import flet as ft
import app.theme as th



def main(page: ft.Page):

    #page.scroll = ft.ScrollMode.AUTO # Esta en veremos hace que le login se vea pegado arriba 
    

    page.bgcolor = th.BG_PRIMARY        # de theme.py
    page.padding = 0
    page.window_width = 400
    page.window_height = 750

    page.title = "Gestor de Finanzas Personales"
    init_db()

    historial = []


    def _cargar_vista(nombre_vista):
        page.controls.clear()
        if nombre_vista == "login":
            page.add(login_view(page, navegar, volver))
        elif nombre_vista == "register":
            page.add(register_view(page, navegar, volver))
        elif nombre_vista == "dashboard":
            page.add(dashboard_view(page, navegar, volver))
        elif nombre_vista == "add_transaction":
            page.add(add_transaction_view(page, navegar, volver))
        elif nombre_vista == "transactions":
            page.add(transactions_view(page, navegar, volver))
        elif nombre_vista == "budgets":
            page.add(budgets_view(page, navegar, volver))
#        elif nombre_vista == "settings":
#            page.add(settings_view(page, navegar, volver))

        page.update()

    def navegar(nombre_vista, limpiar=False):
        if limpiar:
            historial.clear()

        if not historial or historial[-1] != nombre_vista:
            historial.append(nombre_vista)
        _cargar_vista(nombre_vista)

    def volver():
        if len(historial) > 1:
            historial.pop()              # saca la vista actual
            _cargar_vista(historial[-1]) # carga la anterior

    page.on_back_button_click = lambda _: volver()


    sesion = obtener_sesion_guardada()

    if sesion:
        navegar("dashboard")
    else:
        navegar("login")




if __name__ == "__main__":
    ft.run(main)
        
        