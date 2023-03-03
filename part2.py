# Se importan las librerías pandas, requests y las clases task y Flow de la librería prefect.
import pandas as pd
import requests

from prefect import task, Flow

# Descarga de archivo csv de la URL, lo decodifica en formato utf-8, y devuelve un DataFrame de Pandas y lee el contenido
@task
def download_data():
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
    response = requests.get(url)
    data = response.content.decode('utf-8')
    return pd.read_csv(pd.compat.StringIO(data), delimiter=";")

# Se recibe un DataFrame de Pandas como entrada, elimina las filas que contienen valores nulos o faltantes en su lugar, y devuelve el DataFrame limpio.
@task
def clean_data(df):
    df.dropna(inplace=True)
    return df

# Se recibe un DataFrame de Pandas limpio como entrada, y ejecuta un modelo de aprendizaje automático en los datos limpios. 
@task
def run_model(df):
    # código para entrenar y ejecutar modelo de aprendizaje automático en los datos limpios
    return model_results

# Se descarga el archivo de datos utilizando download_data(), luego se limpia con clean_data(), y finalmente se ejecuta el modelo con run_model().
with Flow("my data science workflow") as f:
    raw_data = download_data()
    clean_data = clean_data(raw_data)
    model_results = run_model(clean_data)

f.run()