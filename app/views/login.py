import flet as ft
from app.auth import iniciar_sesion
from app.theme import ACCENT_RED

def login_view(page, navegar, volver):
    
    texto_email = ft.TextField(label="Email", width=300)
    texto_password = ft.TextField(label="Contraseña", width=300, password=True)

    mensaje_error = ft.Text("", color=ACCENT_RED, visible=False, text_align=ft.TextAlign.CENTER)


    def validar_login(e):
      
        if "@" not in texto_email.value or not texto_password.value:
            mensaje_error.value = "Por favor, completa todos los campos."
            mensaje_error.visible = True
            page.update()
            return

        if iniciar_sesion(texto_email.value, texto_password.value):
            navegar("dashboard", limpiar=True)
        else:
            mensaje_error.value = "Credenciales incorrectas. Inténtalo de nuevo."
            mensaje_error.visible = True
            page.update()

    boton_inicio = ft.ElevatedButton(text="Iniciar sesión", width=300, on_click= validar_login)

    texto_pregunta = ft.Text("¿No tienes una cuenta?")
    # Aquí usamos lambda para no tener que crear una función 'ir_a_registro' aparte
    boton_registro = ft.TextButton(text="Registrarse", on_click=lambda _: navegar("register"))

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Iniciar sesión", size=24, weight="bold"),
                texto_email,
                texto_password,
                mensaje_error,
                boton_inicio,
                ft.Row([texto_pregunta, boton_registro], alignment=ft.MainAxisAlignment.CENTER)
            ],
            # alinear los elementos horizontalmente en el centro
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        #centrar el contenido en la pantalla
        alignment=ft.alignment.center,
        expand=True
    )


    

























"""
Campos:
  → Email
  → Contraseña

Botones:
  → "Iniciar sesión"  → llama iniciar_sesion() → navega a dashboard
  → "Registrarse"     → navega a register

Manejo de errores:
  → Credenciales incorrectas → mostrar mensaje en pantalla
  → Campos vacíos → validar antes de llamar a la DB



- Logo o título de la app
- Campo email
- Campo password (oculto)
- Botón "Iniciar sesión"
    → llama a iniciar_sesion(email, password) de auth.py
    → si True → navegar("dashboard")
    → si False → mostrar mensaje de error
- Link o botón "Crear cuenta" → navegar("register")






Orden recomendado para las vistas
1. login.py       → primera pantalla, la más simple
2. register.py    → muy similar al login
3. dashboard.py   → la más importante, la ves siempre
4. transactions.py
5. budgets.py
6. reports.py









"""