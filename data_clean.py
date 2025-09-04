import os
import pandas as pd
from urllib.parse import urlparse
from file_manip import load_all_csvs_from_folder

# Carpeta principal que contiene los CSVs descargados
main_folder = input('Ingresa el nombre del subdominio o nominio del proyecto por ejemplo, www.javilazaro.es: ')
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
        # Eliminar filas duplicadas con la misma query y page
        df_sub = df_sub.drop_duplicates(subset=['query', 'page'])
        sanitized_sub = sub.replace('/', '_').replace(':', '_')
        output_path = os.path.join(filtered_folder, f'{sanitized_sub}_filtrado.csv')
        df_sub.to_csv(output_path, index=False)
        print(f'Guardado: {output_path}')


def search_canibalization_gsc(file_path: str, min_clicks: int=0, min_impressions: int=0, max_position: float=25):
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

    # Filtrar por clics, impresiones y posiciones
    if 'clicks' in df.columns:
        df = df[df['clicks'] >= min_clicks]
    if 'impressions' in df.columns:
        df = df[df['impressions'] >= min_impressions]
    if 'position' in df.columns:
        df = df[df['position'] <= max_position]

    # Detectar canibalización: queries que aparecen en más de una URL (sin importar la fecha)
    # Nos quedamos solo con las columnas relevantes
    df_unique = df[['query', 'page']].drop_duplicates()
    # Contar cuántas URLs distintas tiene cada query
    url_counts = df_unique.groupby('query')['page'].nunique().reset_index(name='url_count')
    # Filtrar queries que aparecen en más de una URL
    canibal_queries = url_counts[url_counts['url_count'] > 1]['query']
    # Filtrar el dataframe original para quedarnos solo con esas queries
    canibalization = df[df['query'].isin(canibal_queries)].sort_values(['query', 'page'])

    if not canibalization.empty:
        print(f'Canibalización encontrada en {file_path}:')
        output_path = file_path.replace('.csv', '_canibalizacion.csv')
        canibalization.to_csv(output_path, index=False)
        print(f'Guardado: {output_path}')
    else:
        print(f'No se encontró canibalización en {file_path}.')


file_csv = input("""Ingresa el nombre del archivo CSV a analizar por ejemplo, www.javilazaro.es_filtrado.csv: """)
canibalizacion = search_canibalization_gsc(os.path.join(filtered_folder, file_csv))