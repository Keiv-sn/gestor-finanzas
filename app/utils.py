from datetime import datetime, timedelta

# Diccionario para nombres en español
MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}


def obtener_mes_actual():
    mes_actual = datetime.now().strftime("%Y-%m")
    return mes_actual


def formatear_fecha(date_str):

    try:
        fecha_obj = datetime.strptime(date_str, "%Y-%m-%d")
        año = fecha_obj.year
        mes_nombre = MESES_ES[fecha_obj.month]
        dia = fecha_obj.day
        return f"{dia} {mes_nombre} {año}"
    
    except (ValueError, TypeError):
        return "Fecha inválida"


def lista_meses():
    # Obtenemos año y mes actual como enteros
    hoy = datetime.now()
    anio_actual = hoy.year
    mes_actual = hoy.month
    
    meses = []
    
    for i in range(12):
        # Calculamos el mes y año restando i
        # Usamos (mes_actual - 1 - i) para manejar el índice base 0 y el módulo 12
        total_meses = (mes_actual - 1) - i # Esto da un número que puede ser negativo, pero el módulo 12 lo ajustará
        nuevo_mes = (total_meses % 12) + 1
        nuevo_anio = anio_actual + (total_meses // 12)
        
        # Formateamos con :02 para que el mes siempre tenga dos dígitos (ej: 04)
        meses.append(f"{nuevo_anio}-{nuevo_mes:02}")
        
    return meses
