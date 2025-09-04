import os
import time
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

# Carpeta principal que contiene los CSVs descargados
main_folder = input('Ingresa el nombre del subdominio o nominio del proyecto por ejemplo, www.javilazaro.es: ')
# Carpeta donde se guardarán los CSVs filtrados
filtered_folder = os.path.join(main_folder, 'filtrado')
if os.makedirs(filtered_folder, exist_ok=True):
    print(f'Carpeta creada: {filtered_folder}')
else:
    print(f'La carpeta ya existe: {filtered_folder}')



user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"

def title_page(url: str) -> str:
    """Obtiene el título de una página web dada su URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req, timeout=10) as response:
            print('Conectando a:', url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            print('parseando')
            title = soup.title.string.strip() if soup.title and soup.title.string else 'No title found'
            print('título encontrado:', title)
            return title
    except Exception as e:
        return f'Error retrieving title: {e}'
    

def headers_page(url: str) -> dict:
    """Obtiene los encabezados de una página web dada su URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req, timeout=10) as response:
            print('Conectando a:', url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            print('parseando')
            headers = []
            for tag in ['h1', 'h2', 'h3', 'h4']:
                headers.extend([f"<{tag}> {h.get_text(strip=True)}" for h in soup.find_all(tag)])
            headers_str = ' | '.join(headers) if headers else 'No headers found'
            print('encabezados encontrados:', headers_str)
            return headers_str
    except Exception as e:
        return f'Error retrieving headers: {e}'


def add_titles_to_canibalization_csvs(folder: str):
    """
    Busca todos los archivos *_canibalizacion.csv en la carpeta dada, añade una columna 'title' con el título de la URL de cada fila y guarda el resultado.
    """
    for file in os.listdir(folder):
        if file.endswith('_canibalizacion.csv'):
            file_path = os.path.join(folder, file)
            print(f'Procesando: {file_path}')
            df = pd.read_csv(file_path)
            print('pansando por el pandas')
            if 'page' not in df.columns:
                print(f'El archivo {file_path} no contiene columna "page".')
                continue
            print('hemos pasado el if correctamente')
            df['title'] = df['page'].apply(title_page)
            print('creando la columna de datos')
            output_path = file_path.replace('.csv', '_con_titulos.csv')
            df.to_csv(output_path, index=False)
            print('creando csv')
            print(f'Guardado: {output_path}')
            time.sleep(1)  # Espera 1 segundo entre solicitudes


def add_headers_to_canibalization_csvs(folder: str):
    """Añade encabezados a los archivos CSV de canibalización en la carpeta dada.

    Args:
        folder (str): La ruta de la carpeta que contiene los archivos CSV.
    """
    for file in os.listdir(folder):
        if file.endswith('_canibalizacion_con_titulos.csv'):
            file_path = os.path.join(folder, file)
            print(f'Procesando: {file_path}')
            df = pd.read_csv(file_path)
            if 'page' not in df.columns:
                print(f'El archivo {file_path} no contiene columna "page".')
                continue
            df['headers'] = df['page'].apply(headers_page)
            output_path = file_path.replace('.csv', '_con_headers.csv')
            df.to_csv(output_path, index=False)
            print(f'Guardado: {output_path}')
            time.sleep(1)


# Función para combinar títulos y headers en un solo archivo por cada CSV
def combine_titles_and_headers(folder: str):
    """
    Une los archivos *_con_titulos.csv y *_con_headers.csv por la columna 'page' y guarda el resultado como *_con_titulos_headers.csv
    """
    for file in os.listdir(folder):
        if file.endswith('_con_titulos.csv'):
            base = file.replace('_con_titulos.csv', '')
            tit_path = os.path.join(folder, file)
            head_path = os.path.join(folder, f'{base}_con_headers.csv')
            if os.path.exists(head_path):
                df_tit = pd.read_csv(tit_path)
                df_head = pd.read_csv(head_path)
                # Unir por 'page' y evitar duplicados
                df_merged = pd.merge(df_tit, df_head[['page', 'headers']], on='page', how='left')
                output_path = os.path.join(folder, f'{base}_con_titulos_headers.csv')
                df_merged.to_csv(output_path, index=False)
                print(f'Guardado: {output_path}')


def get_title_and_headers(url: str) -> pd.Series:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string.strip() if soup.title and soup.title.string else 'No title found'
            headers_str = ';'.join([f"{k}:{v}" for k, v in response.getheaders()])
            return pd.Series({'title': title, 'headers': headers_str})
    except Exception as e:
        return pd.Series({'title': f'Error retrieving title: {e}', 'headers': f'Error retrieving headers: {e}'})

    df[['title', 'headers']] = df['page'].apply(get_title_and_headers)
    output_path = file_path.replace('.csv', '_con_titulos_headers.csv')
    df.to_csv(output_path, index=False)
    print(f'Guardado: {output_path}')
    output_path = file_path.replace('.csv', '_con_encabezados.csv')
    df.to_csv(output_path, index=False)
    print('creando csv')
    print(f'Guardado: {output_path}')
# Ejemplo de uso:
# add_titles_to_canibalization_csvs('bitcoin_com/filtrado')
add_headers_to_canibalization_csvs('bitcoin_com/filtrado')