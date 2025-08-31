import gzip
import os
import pandas as pd


from urllib.parse import urlparse

from date_manip import get_dates, date_to_YM


def create_project(directory):
    """Crea un proyecto si no existe

    Args:
        directory (str): Directorio del proyecto.

    """
    if not os.path.exists(directory):
        print(f'Creando el proyecto: {directory}')
        os.makedirs(directory)
    else:
        print(f'El proyecto ya existe: {directory}')

def get_domain_name(start_url):
    """Toma el nombre del dominio
    1. Parsear la URL para obtener el dominio.
    2. Retornar el nombre del dominio.
    3. Reemplaza los puntos para crear una ruta de carpeta utilizable

    Args:
        start_url (_type_): _description_
    """
    if start_url.startswith('sc-domain:'):
        domain_name=start_url.split(':', 1)[1].replace('.', '_')
    else:
        url = urlparse(start_url)
        domain_name = url.netloc
        domain_name = domain_name.replace('.', '_')
    return domain_name


def write_to_csv(data, filename):
    """Escribe los datos en un archivo CSV.

    Args:
        data (list of dict): Los datos a escribir.
        filename (str): El nombre del archivo CSV.
    """
    if not os.path.isfile(filename):
        data.to_csv(filename, index=False)
    else:
        data.to_csv(filename, mode='a', header=False, index=False)


def write_to_csv_gz(data,filename):
    """Escribe o añade los datos a un archivo CSV comprimido.

    Args:
        data (pd.DataFrame): Los datos a escribir.
        filename (str): El nombre del archivo CSV comprimido.
    """
    filename = filename + '.gz'
    if not os.path.isfile(filename):
        print(f'Creando {filename}')
        data.to_csv(filename, index=False, compression='gzip')
    else:
        print(f'Añadiendo a {filename}')
        with gzip.open(filename, 'at') as compressed_file:
            data.to_csv(compressed_file, header=False, index=False)

def get_full_path(site, filename, date):
    """Obtiene la ruta completa del archivo.

    Args:
        site (str): El nombre del sitio.
        filename (str): El nombre del archivo.
        date (str): La fecha para la que se generan los datos.
    Returns:
        tuple: Una tupla que contiene la ruta de salida, el nombre de dominio, la ruta completa y la ruta de datos.
    """
    domain_name = get_domain_name(site)
    data_path = domain_name + '/'
    YM_date = get_dates(date)[0] #Toma el primer día del mes
    output_path = YM_date + '/' + filename
    output = os.path.join(output_path)
    full_path = data_path + output
    return output, domain_name, full_path, data_path


def loop_csv(full_path, filename, start_date):
    """Procesa un archivo CSV en un bucle.

    Args:
        full_path (str): La ruta completa del archivo CSV.
        filename (str): El nombre del archivo CSV.
        start_date (str): La fecha de inicio para el procesamiento.
    """
    date = date_to_YM(start_date)
    file_list = []
    listdir = os.listdir(full_path)
    for file in listdir:
        if file.endswith('_'+filename):
            file_date = file.split('_')[0]
            if file_date>= date:
                print(f'Procesando {file}')
                file_list.append(file)
                file_list.sort()
    return file_list

def date_to_index(df, datecol):
    """Convierte la columna de fecha de un DataFrame a un índice.

    Args:
        df (pd.DataFrame): El DataFrame a modificar.
        datecol (str): El nombre de la columna de fecha.

    Returns:
        pd.DataFrame: El DataFrame con la columna de fecha como índice.
    """
    if df.index.name == datecol:
        if isinstance(df.index, pd.DatetimeIndex):
            print(f'{datecol} ya es un índice de fecha.')
        else:
            df[datecol] = pd.to_datetime(df[datecol])
    else:
        df[datecol] = pd.to_datetime(df[datecol])
        df = df.set_index(datecol)
    return df

def read_csv_list(path, gz=False):
    """Lee el CSV si exite
    Si gz=True, usa el parámetro compremetido

    Args:
        path (_type_): _description_
        gz (bool, optional): _description_. Defaults to False.
    """
    if os.path.isfile(path):
        print(f'Preparando {path} a csv')
        if gz == True:
            data = pd.read_csv(path, compression='gzip')
        else:
            data = pd.read_csv(path)
        return data
    else:
        pass

def read_csvs(full_path: str, site:str, filename: str, start_date, gz=False):
    """Lee múltiples archivos CSV en un directorio.

    Args:
        full_path (str): EL path del archivo del CSV
        site (str): propiedad del sitio en GSC
        filename (str): nombre del archivo
        start_date (str): Fecha de comienzo
        gz (bool): lector de archivo comprimido
    """
    if gz == True:
        filename = filename + '.gz'
    print(f'Checking CSV in {full_path}')
    dfs = []
    csvs = loop_csv(full_path, filename, start_date)

    if not csvs:
        print('No tenemos ningún CSV para procesar')
        df = pd.DataFrame()
    else:
        for csv in csvs:
            path = os.path.join(full_path, csv)
            df = read_csv_list(path, gz=gz)
            dfs.append(df)
        df = pd.concat(dfs)
    print('Extraídos los DataFrames desde los CSVs:')
    return df

def get_dates_csvs(sites: str, output: str, start_date: str, gz=False) -> set:
    """Obtiene una lista de todas las fechas únicas existentes en un conjunto

    Args:
        sites (str): Lista de sitios a procesar.
        output (str): Nombre del archivo de salida.
        start_date (str): Fecha de inicio.
        gz (bool, optional): Marcamos si el archivo está comprimido. Defaults to False.
    """
    df = csvs_to_df(sites, output, start_date, gz=gz)
    if df.empty:
        return None
    else:
        dset = set(df['date'])
        return dset
    

def csvs_to_df(sites: str, output:str, start_date:str, gz=False) -> pd.DataFrame:
    """Convierte múltiples archivos CSV en un DataFrame.

    Args:
        sites (str): Lista de sitios a procesar.
        output (str): Nombre del archivo de salida.
        start_date (str): Fecha de inicio.
        gz (bool, optional): Marcamos si el archivo está comprimido. Defaults to False.

    Returns:
        pd.DataFrame: _description_
    """

    get_path = get_full_path(sites, output, start_date)
    output_path = get_path[3]
    df = read_csvs(output_path, sites, output, start_date, gz=gz)
    return df


def load_all_csvs_from_folder(folder_path):
    """
    Carga todos los archivos CSV y CSV.gz de una carpeta en un único DataFrame,
    añadiendo una columna 'domain' extraída del nombre del archivo.

    Args:
        folder_path (str): Ruta de la carpeta a procesar.

    Returns:
        pd.DataFrame: DataFrame combinado con columna 'domain'.
    """
    import glob
    all_files = glob.glob(os.path.join(folder_path, '*.csv')) + glob.glob(os.path.join(folder_path, '*.csv.gz'))
    dfs = []
    for file in all_files:
        # Extraer dominio del nombre del archivo (antes del primer '_')
        base = os.path.basename(file)
        domain = base.split('_')[0]
        if file.endswith('.gz'):
            df = pd.read_csv(file, compression='gzip')
        else:
            df = pd.read_csv(file)
        df['domain'] = domain
        dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()