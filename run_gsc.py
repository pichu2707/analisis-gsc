import pandas as pd
from dateutil.relativedelta import relativedelta

from gsc_by_url import gsc_by_url
from gsc_with_filters import gsc_with_filters
from gsc_to_csv_by_month import gsc_to_csv
from oauth import authorize_creds

import pandas as pd

domain = input('Ingresa el dominio (ejemplo: www.javilazaro.es): ')

site = domain  # Propiedad de dominio
creds = 'client_secret.json'    # Archivo de credenciales
output = 'gsc_data.csv'
start_date = '2025-01-01'
end_date = '2025-08-25'  # Puedes ajustar la fecha final

webmasters_service = authorize_creds(creds)

list_of_urls = ['/gambling/']
list_of_urls = [site + x for x in list_of_urls]

# filtros
dimension = 'query'
operator = 'contains'
expression = 'gambling'
args = webmasters_service, site, creds, dimension, operator, expression, start_date, end_date

gsc_with_filters(*args)

args = webmasters_service, site, output, creds, start_date
gsc_to_csv(*args)

