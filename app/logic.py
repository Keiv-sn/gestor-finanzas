# Aca se implementarán las funciones para manejar la lógica de la aplicación de presupuesto personal.
# Estas funciones se encargarán de procesar los datos, realizar cálculos y preparar la información para ser mostrada en la interfaz de usuario.

from database import obtener_transacciones
from database import obtener_cuentas
from database import obtener_presupuestos
from database import obtener_categorias
from database import obtener_objetivos_ahorro

def obtener_resumen(user_id, month):

    transacciones = obtener_transacciones(user_id, month)

    ingresos = 0
    gastos = 0

    for t in transacciones:
        if t["transaction_type"] == "ingreso":
            ingresos += t["amount"]
        elif t["transaction_type"] == "gasto":
            gastos += t["amount"]

    balance_neto_mensual = ingresos - gastos# es para saber si el usuario tuvo un mes positivo o negativo en términos de presupuesto

    cuentas = obtener_cuentas(user_id)
    saldo_total_cuentas = sum(c["balance"] for c in cuentas)# suma de los balances de todas las cuentas del usuario

    return {
        "ingresos": ingresos,
        "gastos": gastos,
        "balance_neto_mensual": balance_neto_mensual,
        "saldo_total_cuentas": saldo_total_cuentas
    }





def obtener_estado_presupuesto(user_id, month):

    presupuestos = obtener_presupuestos(user_id, month)
    resultado = []

    for p in presupuestos:
        if p["amount_limit"] > 0:
            en_uso = p["total_spent"] / p["amount_limit"] * 100 # calcula el porcentaje de uso del presupuesto
        else:
            en_uso = 0 # si el límite de gasto es 0, se considera que no se ha usado el presupuesto

        sobre_limite = en_uso > 100 # determina si el presupuesto está sobre el límite o no

        resultado.append({
            "category_name": p["category_name"],
            "amount_limit": p["amount_limit"],
            "total_spent": p["total_spent"],
            "en_uso": round(en_uso, 2),
            "sobre_limite": sobre_limite
        })
    
    resultado.sort(key=lambda x: (x["sobre_limite"], x["en_uso"]), reverse=True) # ordena primero por sobre_limite (True antes que False) y luego por en_uso de mayor a menor
    return resultado


    


def formatear_moneda(amount):# Podria ir en utils.py, pero como es una función muy usada, la dejo acá por ahora.
    return f"${amount:,.0f}".replace(",", ".")



def obtener_gastos_por_categoria(user_id, month):

    categorias = obtener_categorias(user_id, "gasto") # obtenemos las categorías de gasto del usuario

    transacciones = obtener_transacciones(user_id, month, transaction_type="gasto")

    gastos_por_id = {} # diccionario para almacenar el total de gastos por categoría_id

    resultado = []
    

    for t in transacciones:
        id_categoria = t["category_id"]
        monto = t["amount"]
        gastos_por_id[id_categoria] = gastos_por_id.get(id_categoria, 0) + monto # el .get() devuelve el valor actual del id_categoria o 0 si no existe, y luego se le suma el monto de la transacción

    total_mes = sum(t["amount"] for t in transacciones) 

    for c in categorias:
    
        total = gastos_por_id.get(c["id"], 0)

        porcentaje = (total / total_mes * 100) if total_mes > 0 else 0
    
        resultado.append({
            "nombre_categoria": c["name"],
            "total": total,
            "porcentaje": round(porcentaje, 2)
        })
 
    resultado.sort(key=lambda x: x["total"], reverse=True) # ordena el resultado por total de gastos de mayor a menor
        
    return resultado



def obtener_resumen_ahorro(user_id):

    obj = obtener_objetivos_ahorro(user_id)
    resumen = []

    for a in obj:

        target_amount = a["target_amount"]
        current_amount = a["current_amount"]

        porcentaje = round(current_amount / target_amount * 100, 2) if target_amount > 0 else 0 # calcula el porcentaje de ahorro alcanzado, evitando división por cero
        falta = max(0, target_amount - current_amount) # calcula cuánto falta para alcanzar el objetivo de ahorro
        resumen.append({

            "id": a["id"],
            "nombre_objetivo": a["name"],
            "target_amount": target_amount,
            "current_amount": current_amount,
            "porcentaje": porcentaje,
            "falta": falta,
            "completado": porcentaje >= 100
        })

    resumen.sort(key=lambda x: x["porcentaje"], reverse=True) # ordena el resumen por porcentaje de ahorro alcanzado de mayor a menor

    return resumen



"""
Header        →  "Hola, {username} 👋"  +  ícono cerrar sesión
Caja balance  →  saldo total grande
Caja ahorro   →  primer objetivo con barra de progreso
Fila doble    →  gastos por categoría (barras)  |  transacciones recientes
Banner alerta →  si hay presupuesto sobre 80% de uso
Navbar        →  5 botones fijos abajo
"""