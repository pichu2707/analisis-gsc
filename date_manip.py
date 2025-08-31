import datetime

from dateutil.relativedelta import relativedelta

def date_to_string(date) -> str:
    """Convertir la fecha a un estring en formato: "YYYY-MM-DD"

    Args:
        date (datetime.date): La fecha a convertir.
    """
    cond_1 = isinstance(date, datetime.datetime)
    cond_2 = isinstance(date, datetime.date)
    if cond_1 or cond_2:
        date = datetime.datetime.strftime(date, "%Y-%m-%d") #Convertido a string
    return date

def string_to_date(date: str) -> datetime.date:
    """Convertir un string en formato "YYYY-MM-DD" a una fecha.

    Args:
        date_string (str): El string a convertir.

    Returns:
        datetime.date: La fecha convertida.
    """
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    return date

def date_to_YM(date) -> str:
    """Convertir el año y el mes en un string

    Args:
        date (_type_): Fecha
    
    Returns:
        str: El año y el mes en formato "YYYY-MM".
    """
    dt = string_to_date(date)
    return datetime.datetime.strftime(dt, "%Y-%m")

def list_dates(startDate, endDate) -> list[str]:
    """Generar una lista de fechas entre dos fechas.

    Args:
        startDate (str): La fecha de inicio en formato "YYYY-MM-DD".
        endDate (str): La fecha de fin en formato "YYYY-MM-DD".

    Returns:
        list: Lista de fechas en formato "YYYY-MM-DD".
    """
    start_date = string_to_date(startDate) # toma la fecha de inicio como un objeto de datetime
    end_date = string_to_date(endDate) # toma la fecha final como un objeto de datetime
    delta = end_date - start_date #Muestra la diferencia como un timedelta 

    days = [] #Inicializa la lista de días
    for i in range(delta.days): #  Creamos un bucle con los deta(dias=n)
        timedelta = datetime.timedelta(days=i) # Crea un delta
        day = start_date + timedelta
        day = date_to_string(day) #Convierte a string
        days.append(day)

    return days

def get_dates(chosen_date):
    """toma los días desde que empieza el mes
    Si los días no están definidos, usa el mes en curso, 
    si no usa el mes elegido.

    Args:
        chosen_date (datetime.date): Mes elegido.
    """
    today = datetime.datetime.now()
    days = relativedelta(days=3) #GSC tiene un delay de 3 días
    end_date = today - days #Resta los días de retraso
    if chosen_date == '':
        delta = end_date - today.replace(day=1)     #Toma el primer día del mes
        start_date = end_date - delta 
    else:
        delta = end_date - datetime.datetime.strptime(chosen_date, "%Y-%m-%d")  # Cuenta la diferencia entre el último día y el primero del mes
        start_date = end_date - delta
    YM_date = date_to_YM(start_date)
    return YM_date, start_date, end_date