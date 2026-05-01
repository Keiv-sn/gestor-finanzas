import flet as ft
from app.database import crear_usuario
from app.theme import ACCENT_RED
import app.theme as th



def register_view(page, navegar, volver):

    texto_username = ft.TextField(label="Nombre de usuario", label_style=ft.TextStyle(color=th.TEXT_PRIMARY), width=300)
    texto_email = ft.TextField(label="Email de registro", label_style=ft.TextStyle(color=th.TEXT_PRIMARY), width=300)
    texto_password = ft.TextField(label="Contraseña", label_style=ft.TextStyle(color=th.TEXT_PRIMARY), width=300, password=True)
    texto_password_confirm = ft.TextField(label="Confirmar contraseña", label_style=ft.TextStyle(color=th.TEXT_PRIMARY), width=300, password=True)

    mesaje_error = ft.Text("", color=ACCENT_RED, visible=False, text_align=ft.TextAlign.CENTER)


    def validar_registro(e):
        
        mesaje_error.visible = False # <--- Ocultamos errores anteriores

        if not texto_username.value or not texto_email.value or not texto_password.value or not texto_password_confirm.value:
            mesaje_error.value = "Por favor, completa todos los campos."
            mesaje_error.visible = True
            page.update()
            return
        
        if texto_password.value != texto_password_confirm.value:
            mesaje_error.value = "Las contraseñas no coinciden."
            mesaje_error.visible = True
            page.update()
            return
        
        if "@" not in texto_email.value:
            mesaje_error.value = "Por favor, ingresa un email válido."
            mesaje_error.visible = True
            page.update()
            return
        
        ok, msg = crear_usuario(texto_username.value, texto_password.value, texto_email.value) # creamos el usuario, y recibimos un booleano si fue exitoso o no, y un mensaje de error en caso que no
        
        if ok:
            navegar("login", limpiar=True)

        else:
            mesaje_error.value = msg
            mesaje_error.visible = True
            page.update()

    boton_registro = ft.ElevatedButton(ft.Text("Registrarse"), width=300, bgcolor=th.BG_SECONDARY, color=th.TEXT_PRIMARY, on_click= validar_registro)

    texto_pregunta = ft.Text("¿Ya tienes una cuenta?")
    boton_inicio = ft.TextButton(ft.Text("Iniciar sesión", color= th.TEXT_PRIMARY), on_click=lambda _: navegar("login"))

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Registro de usuario", color=th.TEXT_PRIMARY, size=24, weight="bold"),
                texto_username,
                texto_email,
                texto_password,
                texto_password_confirm,
                mesaje_error,
                boton_registro,
                ft.Row([texto_pregunta, boton_inicio], alignment=ft.MainAxisAlignment.CENTER)
            ],
            # alinear los elementos 
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        #centrar el contenido en la pantalla
        alignment=ft.Alignment(0, 0),
        expand=True
    )
