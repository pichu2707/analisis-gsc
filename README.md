# Gestión de proyectos desde Google Search Console
Este proyecto es una ampliación automatizada del trabajo de **Jean-Christophe Chouinard**, que puedes encontrar en su [web](https://www.jcchouinard.com/).

## ¿Qué hace este proyecto?

- Descarga y organiza datos de Google Search Console (GSC) por dominio y subdominio.
- Filtra y guarda los datos de cada subdominio en archivos CSV independientes.
- Detecta canibalización de keywords entre URLs de un mismo dominio.
- Permite ejecutar todo el flujo de trabajo con un solo comando, de forma interactiva y modular.

## Estructura principal

- `file_manip.py`: Funciones para crear proyectos, obtener nombres de dominio y manipular archivos.
- `data_clean.py`: Funciones para filtrar datos por subdominio y buscar canibalización.
- `run_gsc.py`: Script principal para lanzar el flujo completo (limpieza y análisis), con selección interactiva.
- Credenciales OAuth: Para autenticación con la API de GSC.

## ¿Cómo funciona el flujo?

1. **Creación de proyecto y carpeta**  
   El nombre de la carpeta principal se genera automáticamente a partir del dominio (usando `get_domain_name`).

2. **Filtrado de subdominios**  
   Los datos de GSC se separan y guardan en CSVs individuales por subdominio.

3. **Análisis de canibalización**  
   El usuario puede elegir si quiere buscar canibalización en los datos filtrados (por defecto, sí).

4. **Ejecución centralizada**  
   Todo el flujo se lanza desde `run_gsc.py`, que pregunta al usuario si desea realizar el análisis de canibalización.

## Ejemplo de uso

```bash
python run_gsc.py --main_folder <nombre_de_tu_carpeta>
```

El script te preguntará si quieres buscar canibalización ('S') o solo filtrar y guardar los datos ('N').

## Personalización

- Puedes cambiar el dominio/proyecto modificando el argumento `--main_folder` o la URL base.
- El flujo es modular: puedes usar solo las funciones de filtrado o solo el análisis de canibalización si lo necesitas.

## Requisitos

- Python 3.8+
- Pandas, requests, google-api-python-client, oauth2client, beautifulsoup4, etc.
- Credenciales OAuth válidas para la API de Google Search Console.

## Créditos

Basado en el trabajo de [Jean-Christophe Chouinard](https://www.jcchouinard.com/).
Automatización y mejoras por tu equipo.

Si tienes alguna duda o crees que se puede ampliar el proyecto no dues en escribirme a mi [email](mailto:hola@javilazaro.es)