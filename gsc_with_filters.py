import pandas as pd

from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta

from date_manip import date_to_string
from oauth import execute_request

today = datetime.now()
days = relativedelta(days=3)
default_end = today - days

#Levantando la extracción
def gsc_with_filters(webmasters_service, site:str, creds, dimension:str, operator:str, expression:str, start_date: datetime, end_date: datetime = default_end, rowLimit:int = 1000):
    """Extrae datos de Google Search Console con filtros

    Args:
        webmasters_service (_type_): _description_
        site (str): _description_
        dimension (str): _description_
        operator (str): _description_
        expression (str): _description_
        start_date (datetime): _description_
        end_date (datetime, optional): _description_. Defaults to default_end.
        rowLimit (int, optional): _description_. Defaults to 1000.
    """

    scDict = defaultdict(list)

    request = {
        "startDate": date_to_string(start_date),
        "endDate": date_to_string(end_date),
        "dimension": ['date','page','query'], #country, device, page, query, searchAppearance
        "dimensionFilterGroups": [
            {
                "filters": [
                    {
                        "dimension": dimension,
                        "operator": operator,
                        "expression": expression
                    }
                ]
            }
        ],
        'rowLimit': rowLimit
    }

    # Ejecutar la consulta
    response = execute_request(webmasters_service, site, request)

    try:
        for row in response['rows']:
            scDict['date'].append(row['keys'][0] or 0)
            scDict['page'].append(row['keys'][1] or 0)
            scDict['query'].append(row['keys'][2] or 0)
            scDict['clicks'].append(row['clicks'] or 0)
    except Exception as e:
        print(f"Error procesando la {site}: {e}")

    # Convertir el diccionario en un DataFrame de pandas
    df = pd.DataFrame(data = scDict)
    return df