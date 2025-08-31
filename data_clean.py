import os
import pandas as pd
from urllib.parse import urlparse
from file_manip import load_all_csvs_from_folder

# Carpeta principal que contiene los CSVs descargados
main_folder = input('Ingresa el nombre del subdominio o nominio del proyecto por ejemplo, www.javilazaro.es')
# Carpeta donde se guardarán los CSVs filtrados
filtered_folder = os.path.join(main_folder, 'filtrado')
os.makedirs(filtered_folder, exist_ok=True)

df = load_all_csvs_from_folder(main_folder)

if df.empty:
    print(f'No se encontraron datos en la carpeta {main_folder}')
else:
    # Extraer subdominio de la columna 'page'
    df['subdomain'] = df['page'].apply(lambda x: urlparse(x).netloc if pd.notnull(x) else '')

    subdomains = df['subdomain'].unique()
    print(f'Subdominios encontrados: {subdomains}')

    for sub in subdomains:
        df_sub = df[df['subdomain'] == sub]
        sanitized_sub = sub.replace('/', '_').replace(':', '_')
        output_path = os.path.join(filtered_folder, f'{sanitized_sub}_filtrado.csv')
        df_sub.to_csv(output_path, index=False)
        print(f'Guardado: {output_path}')


def search_canibalization_gsc(file_path: str, min_clicks=0, min_impressions=0):
    """
    Busca canibalización en los datos de GSC, permitiendo filtrar por mínimo de clics e impresiones.

    Args:
        file_path (str): Ruta al archivo CSV de GSC.
        min_clicks (int): Mínimo de clics para conservar la fila.
        min_impressions (int): Mínimo de impresiones para conservar la fila.
    """
    df = pd.read_csv(file_path)
    if 'page' not in df.columns or 'query' not in df.columns:
        print(f'El archivo {file_path} no contiene las columnas necesarias.')
        return

    # Filtrar por clics e impresiones
    if 'clicks' in df.columns:
        df = df[df['clicks'] >= min_clicks]
    if 'impressions' in df.columns:
        df = df[df['impressions'] >= min_impressions]

    # Contar ocurrencias de cada combinación (page, query)
    canibalization_counts = df.groupby(['page', 'query']).size().reset_index(name='count')

    # Filtrar combinaciones con más de una ocurrencia
    canibalization = canibalization_counts[canibalization_counts['count'] > 1]

    if not canibalization.empty:
        print(f'Canibalización encontrada en {file_path}:')
        for index, row in canibalization.iterrows():
            print(f" - Página: {row['page']}, Consulta: {row['query']}, Ocurrencias: {row['count']}")
        output_path = file_path.replace('.csv', '_canibalizacion.csv')
        canibalization.to_csv(output_path, index=False)
    else:
        print(f'No se encontró canibalización en {file_path}.')

file_csv = input('Ingresa el nombre del archivo CSV a analizar por ejemplo, www.javilazaro.es_filtrado.csv')
canibalizacion = search_canibalization_gsc(os.path.join(filtered_folder, file_csv))