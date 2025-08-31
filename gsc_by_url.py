import pandas as pd

from collections import defaultdict
import datetime
from dateutil.relativedelta import relativedelta

from date_manip import date_to_string
from oauth import execute_request

"""
Inicializamos por defecto con 3 días de delay
Esto lo usaremos cuando el end_date no está definido
"""

today = datetime.datetime.now()
days = relativedelta(days=3)
default_end = today - days

def gsc_by_url(webmasters_service, site:str, list_of_urls:list[str], start_date: datetime.datetime, end_date: datetime.datetime = default_end):
    """Extrae datos de Google Search Console por URL

    Args:
        webmasters_service (_type_): _description_
        site (str): _description_
        list_of_urls (list[str]): _description_
        start_date (_type_): _description_
        end_date (_type_, optional): _description_. Defaults to default_end.
    """

    #Auutoriza las credenciales a logs en las APi
    # Transoforma los datos de fechas en strings
    start_date = date_to_string(start_date)
    end_date = date_to_string(end_date)

    #Inicializando el diccionario vacío
    scDict = defaultdict(list)

    for url in list_of_urls:
        """
        Revisa como está el formato de tus peticiones
        """
        request = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensionFilterGroups": [
                {
                    "filters": [
                        {
                            "dimension": "query", #page, query, country, device, searchAppearance
                            "operator": "contains", #contains, equals, notEquals, noEquals
                            "expression": url
                        }
                    ]
                }
            ]
        }

        # Ejecutar la consulta
        response = execute_request(webmasters_service, site, request)

        #Convertir el Json a un diccionario
        scDict['page'].append(url)
        try:
            for row in response['rows']:
                scDict['clicks'].append(row['clicks'] or 0)
                scDict['impressions'].append(row['impressions'] or 0)
        except Exception as e:
            print(f"Error procensando la {url}: {e}")

    # Convertir el diccionario en un DataFrame de pandas
    df = pd.DataFrame(data = scDict)
    return df