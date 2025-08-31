import argparse
import os
import re
import time
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict

import pandas as pd

import date_manip as dm
import file_manip as fm
from oauth import execute_request

today = datetime.datetime.now()
days = relativedelta(days=3)
default_end = today - days

#Creando una función para extraer todos los datos
def gsc_to_csv(webmasters_service, site, output, creds, start_date, end_date=default_end, gz=False):
    
    print(f'gsc_to_csv gz: {gz}')
    get_path = fm.get_full_path(site, output, start_date)
    domain_name = get_path[1]
    output_path = get_path[3]
    fm.create_project(domain_name)
    csv_dt = fm.get_dates_csvs(site, output, start_date, gz=gz)

    #Configurando fechas
    dates = dm.get_dates(start_date)
    start_date = dates[1]
    end_date = dm.string_to_date(end_date)
    delta = datetime.timedelta(days=1)
    scDict = defaultdict(list)
    while start_date <= end_date:
        curr_mont = dm.date_to_YM(start_date)
        full_path = os.path.join(output_path, curr_mont + '-' + output)
        # Si existe un archivo csv de una extracción previa y las fechas coinciden con lo que estamos extrayendo
        if csv_dt is not None and dm.date_to_string(start_date) in csv_dt:
            print(f'Existe la fecha: {start_date}')
            start_date += delta
        else:
            #Nos prenseta por pantalla que comienza la extracción
            print(f'Comenzamos la estracción: {start_date}')

            maxRows = 25000 #Es el máximo que nos permite cada llamada
            numRows = 0
            status = ''

            while (status != 'Finished'):
                # Extrae esta infromación de Google search console
                dt = dm.date_to_string(start_date)
                print(f'date = {dt}')
                request = {
                    'startDate': dt,
                    'endDate': dt,
                    'dimensions': ['date', 'page', 'query'], #Información que extrae
                    'rowLimit': maxRows,
                    'startRow': numRows
                }
                response = execute_request(webmasters_service, site, request)

                #Procesando la respuesta
                try:
                    for row in response['rows']:
                        scDict['date'].append(row['keys'][0] or 0)
                        scDict['page'].append(row['keys'][1] or 0)
                        scDict['query'].append(row['keys'][2] or 0)
                        scDict['clicks'].append(row['clicks'] or 0)
                        scDict['ctr'].append(row['ctr'] or 0)
                        scDict['impressions'].append(row['impressions'] or 0)
                        scDict['position'].append(row['position'] or 0)
                    print(f'Filas extraídas: {len(response["rows"])}')

                except Exception as e:
                    print(f'Error procesando la {site}: {e} en la linea {numRows}')


                #Añadir las respuestas al DataFrame
                df = pd.DataFrame(data = scDict)
                df['clicks'] = df['clicks'].astype('int')
                df['ctr'] = df['ctr']*100
                df['impressions'] = df['impressions'].astype('int')
                df['position'] = df['position'].round(2)

                #Incrementar el 'start_row' 
                print(f'El Numrows de comienzo del loop es: {numRows}')
                try:
                    numRows = numRows + len(response['rows']) 
                except:
                    status = 'Finished'
                print(f'El NumRows final del loop es: {numRows}')

                if numRows % maxRows != 0:
                    status = 'Finished'
                
            to_write = df[df['date'].str.contains(dm.date_to_string(start_date))]
            if gz == False:
                fm.write_to_csv(to_write, full_path)
            elif gz == True:
                fm.write_to_csv_gz(to_write, full_path)
            start_date += delta
    
    print(f'Extracción finalizada. Los archivos están en: {site}')