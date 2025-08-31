"""
@author: Javi Lázaro
@role: Analista, SEO, CRO, programador
@website: www.javilazaro.es
@LinkedIn: www.linkedin.com/in/javilazaro


Consigue hacer análisis en diferentes subdominios cuando conectas un dominio en tu Google Search Console con la API de Google.


Más informacion próximamente en www.javilazaro.es
"""

import argparse
import httplib2
import requests

from googleapiclient.discovery import build
from oauth2client import client, file, tools

def authorize_creds(creds):
    """Autorizar al usuario y devolver las credenciales para permitir el acceso

    Args:
        creds (_type_): _description_
    """

    # Variable para controlar 
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

    #
    CLIENT_SECRET_PATH = 'client_secret.json'

    #Creando un flujo de autenticación abriendo el navegador para aceptar
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        parents=[tools.argparser]
    )
    flags = parser.parse_args([])

    #Crear autentificacion desde el archivo de client_secret
    # Esto generará un error InvalidClientSecretsError si el archivo no es válido para flujos desconocidos

    flow = client.flow_from_clientsecrets(
        CLIENT_SECRET_PATH, SCOPES,
        message=tools.message_if_missing(CLIENT_SECRET_PATH)
    )

    #Preparar credeciales y autorizar HTTP
    # Si existen, obtenerlas del objeto de almacenamiento
    # Las credenciales se volverán a escribir en el archivo de authorizedcreds.data

    storage = file.Storage('authorizedcreds.data')
    credentials = storage.get()

    # Si la acreditación de autenticación no existe abre el navegador de autenticación
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)

    # Toma las credenciales y la autorización para usar el httplib2
    http = httplib2.Http() #Crea un objeto Http

    # crea un request de httplib2
    http = credentials.authorize(http) #Firma cada solicitud del cliente HTTP con el token de acceso OAuth 2.0
    webmasters_service = build('searchconsole', 'v1', http=http)

    print("Auth OK")
    return webmasters_service

# Crea la función para ejecutar la petición de tu API
def  execute_request(service, property_uri, request):
    return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()