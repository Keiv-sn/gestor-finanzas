from database import verificar_password
from database import obtener_usuario_email    
import json
from pathlib import Path
from database import APP_DIR, obtener_usuario_por_id

current_user = None
SESSION_PATH = APP_DIR/"session.json"


def iniciar_sesion(email, password):
    global current_user
    user = obtener_usuario_email(email)
    if user and verificar_password(password, user['password_hash']):
        current_user = user

        session = {
            "user_id": user['id']
        }

        with open(SESSION_PATH, "w") as f:
            json.dump(session, f)

        return True
    return False


def cerrar_sesion(): # tener en cuenta que si intenta cerrar sesión sin haber iniciado sesión, no debería hacer nada y retornar False
    global current_user

    if current_user:
        if Path(SESSION_PATH).exists():
            Path(SESSION_PATH).unlink()

        current_user = None
        return True
    return False


def obtener_sesion_guardada():
    global current_user
    if SESSION_PATH.exists():

        try:

            with open(SESSION_PATH, "r") as f:
                session = json.load(f)
            user_id = session.get("user_id")

            if user_id:
                current_user = obtener_usuario_por_id(user_id)
                return current_user
        
        except Exception as e:
            return None
    return None


def obtener_usuario_activo():
    if current_user:
        return current_user
    return None
