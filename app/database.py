import sqlite3
import bcrypt
from pathlib import Path

APP_DIR = Path.home()/".gestor_finanzas" # Directorio de la aplicación
DB_PATH = APP_DIR/"finanzas.db"# Ruta a la base de datos

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
    return conn



def init_db():
    conn = None
    try:
        # Crear el directorio de la aplicación si no existe
        APP_DIR.mkdir(parents=True, exist_ok=True)
        # Crear la base de datos y las tablas si no existen

        conn = get_connection() 
        cursor = conn.cursor()

        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                account_type TEXT,
                balance INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, name)
            );
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                category_type TEXT CHECK(category_type IN ('ingreso', 'gasto')) NOT NULL,
                is_default INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, name)
            );
                             
             CREATE UNIQUE INDEX IF NOT EXISTS unique_global_categories
                ON categories(name)
                WHERE user_id IS NULL;
                             
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                account_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                transaction_type TEXT CHECK(transaction_type IN ('ingreso', 'gasto')) NOT NULL,
                description TEXT,
                date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (account_id) REFERENCES accounts(id),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            );
            CREATE TABLE IF NOT EXISTS savings_goals(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT UNIQUE NOT NULL,
                target_amount INTEGER NOT NULL,
                current_amount INTEGER DEFAULT 0,
                deadline TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                amount_limit INTEGER NOT NULL,
                month TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (category_id) REFERENCES categories(id),
                UNIQUE(user_id, category_id, month)                         
            );
                
        """)
        cursor.execute("SELECT COUNT(*) FROM categories WHERE is_default = 1")
        count = cursor.fetchone()[0]
        if count == 0:

            categorias_default = [
            (None, 'Sueldo', 'ingreso', 1),
            (None, 'Freelance', 'ingreso', 1),
            (None, 'Inversiones', 'ingreso', 1),
            (None, 'Otros Ingresos', 'ingreso', 1),
            (None, 'Arriendo', 'gasto', 1),
            (None, 'Comida', 'gasto', 1),
            (None, 'Transporte', 'gasto', 1),
            (None, 'Entretenimiento', 'gasto', 1),
            (None, 'Educación', 'gasto', 1),
            (None, 'Servicios básicos', 'gasto', 1),
            (None, 'Ropa', 'gasto', 1),
            (None, 'Otros Gastos', 'gasto', 1),
            ]

            cursor.executemany(
                "INSERT INTO categories (user_id, name, category_type, is_default) VALUES (?, ?, ?, ?)",
                categorias_default
            )

        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()



#       -Funciones de usuarios-       #

def crear_usuario(username, password, email):
    conn = None

    try:
        sal = bcrypt.gensalt() # Genera una sal() aleatoria
        encript = bcrypt.hashpw(password.encode('utf-8'), sal).decode('utf-8') # Encripta la contraseña con la sal

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)", (email, username, encript))
        conn.commit()
        return True, "Usuario creado"
        
    except sqlite3.IntegrityError as e:
        if "email" in str(e):
            return False, "El correo electrónico ya está registrado."
        elif "username" in str(e):
            return False, "El nombre de usuario ya está registrado."
        else:
            return False, "Error al crear el usuario."
    finally:
        if conn:
            conn.close()


def obtener_usuario_email(email):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()# Devuelve un diccionario con los datos del usuario o None si no se encuentra
        return user # Devuelve el usuario encontrado o None si no se encuentra
    

    

    finally:# Cierra la conexión a la base de datos
        if conn:
            conn.close()


def obtener_usuario_por_id(user_id):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()# Devuelve un diccionario con los datos del usuario o None si no se encuentra
        return user # Devuelve el usuario encontrado o None si no se encuentra

    finally:# Cierra la conexión a la base de datos
        if conn:
            conn.close()


def verificar_password(password, password_hash):
    
    code_password = bytes(password, 'utf-8')# Convierte la contraseña ingresada a bytes

    return bcrypt.checkpw(code_password, password_hash.encode('utf-8'))# Compara la contraseña ingresada con el hash almacenado


#       -Funciones de cuentas-       #


def crear_cuenta(user_id, name, account_type, balance):# Crea una nueva cuenta para un usuario específico
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (user_id, name, account_type, balance) VALUES (?, ?, ?, ?)", (user_id, name, account_type, balance))
        conn.commit()
        return True, "Cuenta creada"
        
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e):
            return False, "El nombre de la cuenta ya está registrado."
        else:
            return False, "Error al crear la cuenta."
    finally:
        if conn:
            conn.close()


def obtener_cuentas(user_id): #Devuelve una lista de cuentas para un usuario específico
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,))
        accounts = cursor.fetchall()

        if not accounts:
            return []
        return accounts
    
    except sqlite3.Error as e:
        return []
    finally:
        if conn:
            conn.close()


def ajustar_balance(account_id, amount):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))

        if cursor.rowcount == 0:
            return False, "Cuenta no encontrada."

        conn.commit()
        return True, "Balance Ajustado"
    
    except sqlite3.Error as e:
        return False, f"Error: {e}"
    finally:
        if conn:
            conn.close()


#       -Funciones de categorías-       #


def obtener_categorias(user_id, category_type=None): # Devuelve una lista de categorías, opcionalmente filtradas por tipo (ingreso/gasto)
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        if category_type is not None:
            cursor.execute("SELECT * FROM categories WHERE (user_id = ? OR user_id IS NULL) AND category_type = ?", (user_id, category_type))
        else:
            cursor.execute("SELECT * FROM categories WHERE (user_id = ? OR user_id IS NULL)", (user_id,))

        categories = cursor.fetchall()
        return categories
        
    except sqlite3.Error as e:
        return []
    finally:
        if conn:
            conn.close()


def crear_categoria(user_id, name, category_type): # Crea una nueva categoría para un usuario específico
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (user_id, name, category_type) VALUES (?, ?, ?)", (user_id, name, category_type))
        conn.commit()
        return True, "Categoría creada"
    
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e):
            return False, "El nombre de la categoría ya está registrado."
        else:
            return False, f"Error al crear la categoría: {e}"
    finally:
        if conn:
            conn.close()


def eliminar_categoria(id): # Elimina una categoría por su ID solo si no es default
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verificar si está en uso
        cursor.execute(
            "SELECT 1 FROM transactions WHERE id = ? LIMIT 1", (id,))
        if cursor.fetchone():
            return False, "No puedes eliminar una categoría en uso"


        cursor.execute("DELETE FROM categories WHERE id = ? AND is_default = 0", (id,))

        if cursor.rowcount == 0:
            return False, "No se puede eliminar una categoría por defecto o la categoría no existe."

        conn.commit()
        return True, "Categoría eliminada"
    
    except sqlite3.Error as e:
        return False, f"Error: {e}"
    
    finally:
        if conn:
            conn.close()


#       -Funciones de transacciones-       #


def crear_transaccion(user_id, account_id, category_id, amount, transaction_type, description, date):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (user_id, account_id, category_id, amount, transaction_type, description, date) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, account_id, category_id, amount, transaction_type, description, date))
        
        if transaction_type == "gasto":
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
        else:
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        
        conn.commit()
        return True, "Transacción creada"

    except sqlite3.Error as e:
        return False, f"Error: {e}"
    
    finally:
        if conn:
            conn.close()

    
def obtener_transacciones(user_id, month = None, date_from = None, date_to = None, category_id = None, amount_min = None , amount_max = None, transaction_type = None):
    conn= None

    try:
        conn= get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM transactions WHERE user_id = ?"
        params = [user_id]

        if month is not None:
            query += " AND date LIKE ?"
            params.append(f"{month}%")
        else:
            if date_from is not None:
                query += " AND date >= ?"
                params.append(date_from)

            if date_to is not None:
                query += " AND date <= ?"
                params.append(date_to)

        if category_id is not None:
            query += " AND category_id = ?"
            params.append(category_id)

        if amount_min is not None:
            query += " AND amount >= ?"
            params.append(amount_min)

        if amount_max is not None:
            query += " AND amount <= ?"
            params.append(amount_max)

        if transaction_type is not None:
            query += " AND transaction_type = ?"
            params.append(transaction_type)

        query += " ORDER BY date DESC"

        cursor.execute(query, params)
        transactions = cursor.fetchall()

        return transactions

    except sqlite3.Error as e:
        return []
    finally:
        if conn:
            conn.close()


def eliminar_transaccion(id):
    conn = None

    try:
        conn = get_connection()
        cursor= conn.cursor()

        cursor.execute("SELECT account_id, amount, transaction_type FROM transactions WHERE id = ?", (id,))
        transaction = cursor.fetchone()
        
        if not transaction:
            return False, "Transacción no encontrada."
        
        account_id, amount, transaction_type = transaction

        if transaction_type == "gasto":
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        else:
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))


        cursor.execute("DELETE FROM transactions WHERE id = ?", (id,))
        conn.commit()
        return True, "transacción eliminada"
    
    except sqlite3.Error as e:
        return False, f"Error: {e}"
    finally:
        if conn:
            conn.close()


#       -FunFunciones de objetivos de ahorro-       #

def crear_objetivo_ahorro(user_id, name, target_amount, deadline = None):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO savings_goals (user_id, name, target_amount, deadline) VALUES (?, ?, ?, ?)", (user_id, name, target_amount, deadline))
        conn.commit()
        return True, "Objetivo de ahorro creado"
    
    except sqlite3.Error as e:
        return False, f"Error: {e}"
    
    finally:
        if conn:
            conn.close()



def obtener_objetivos_ahorro(user_id):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM savings_goals WHERE user_id = ?", (user_id,))
        goals = cursor.fetchall()
        return goals
    
    except sqlite3.Error as e:
        return []
    
    finally:
        if conn:
            conn.close()



def eliminar_objetivo_ahorro(id):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM savings_goals WHERE id = ? LIMIT 1", (id,))
        
        if not cursor.fetchone():
            return False, "Objetivo de ahorro no encontrado."

        cursor.execute("DELETE FROM savings_goals WHERE id = ?", (id,))
        conn.commit()
        return True, "Objetivo de ahorro eliminado"

    except sqlite3.Error as e:
        return False, f"Error: {e}"

    finally:
        if conn:
            conn.close()



def actualizar_progreso_ahorro(id, new_amount):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Primero obtenemos el estado actual para validar
        cursor.execute("SELECT target_amount, current_amount FROM savings_goals WHERE id = ?", (id,))
        goal = cursor.fetchone()

        if not goal:
            return False, "Objetivo no encontrado."
        
        nuevo_total = goal["current_amount"] + new_amount

        # 2. Actualizamos usando el ID
        cursor.execute("UPDATE savings_goals SET current_amount = ? WHERE id = ?", (nuevo_total, id))
        
        conn.commit()
        return True, goal["target_amount"] - nuevo_total # Devuelve cuánto falta para alcanzar la meta

    except sqlite3.Error as e:
        return False, f"Error de base de datos: {e}"
    finally:
        if conn:
            conn.close()



def actualizar_objetivos_ahorro(id, name=None, target_amount=None, deadline=None):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT target_amount, current_amount FROM savings_goals WHERE id = ?", (id,))
        goal = cursor.fetchone()

        if not goal:
            return False, "Objetivo no encontrado."
        
        if target_amount is not None and target_amount < goal["current_amount"]:
            return False, f"La nueva meta no puede ser menor a lo ya ahorrado."

        updates = []
        params = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)

        if target_amount is not None:
            updates.append("target_amount = ?")
            params.append(target_amount)

        if deadline is not None:
            updates.append("deadline = ?")
            params.append(deadline)

        if not updates:
            return False, "No se proporcionaron campos para actualizar."

        params.append(id)
        query = f"UPDATE savings_goals SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()

        return True, "Objetivo de ahorro actualizado"

    except sqlite3.Error as e:
        return False, f"Error: {e}"

    finally:
        if conn:
            conn.close()

#       -FunFunciones de presupuestos-       #

def crear_presupuesto(user_id, category_id, amount_limit, month):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO budgets (user_id, category_id, amount_limit, month) VALUES (?, ?, ?, ?)", (user_id, category_id, amount_limit, month))
        conn.commit()
        return True, "Presupuesto creado"

    except sqlite3.Error as e:
        return False, "Ya existe un presupuesto para esta categoría en ese mes."

    finally:
        if conn:
            conn.close()



def obtener_presupuestos(user_id, month):# Devuelve una lista de presupuestos para un usuario específico en un mes específico, incluyendo el total gastado en cada categoría
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        query= """
        SELECT 
            budgets.id,
            budgets.category_id,
            categories.name AS category_name,
            budgets.amount_limit,
            COALESCE(SUM(transactions.amount), 0) AS total_spent

        FROM budgets

        JOIN categories 
            ON budgets.category_id = categories.id

        LEFT JOIN transactions 
            ON transactions.category_id = budgets.category_id
            AND transactions.user_id = budgets.user_id
            AND transactions.transaction_type = 'gasto'
            AND transactions.date LIKE ?

        WHERE budgets.user_id = ?
        AND budgets.month = ?

        GROUP BY budgets.id
        """
        cursor.execute(query, (f"{month}%", user_id, month))# El filtro de fecha se aplica en la unión con transacciones para sumar solo los gastos del mes correspondiente
        return cursor.fetchall()
        
    except sqlite3.Error as e:
        return []
    finally:
        if conn:
            conn.close()



def eliminar_presupuesto(id):
    
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM budgets WHERE id = ? LIMIT 1", (id,))
        
        if not cursor.fetchone():
            return False, "Presupuesto no encontrado."

        cursor.execute("DELETE FROM budgets WHERE id = ?", (id,))
        conn.commit()
        return True, "Presupuesto eliminado"

    except sqlite3.Error as e:
        return False, f"Error: {e}"

    finally:
        if conn:
            conn.close()














if __name__ == "__main__":
    init_db()
    print("Base de datos creada correctamente")

#funciones CRUD