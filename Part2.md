# Workflow managers with Python Part.2
#### BARAJAS GOMEZ JUAN MANUEL | 216557005 | COMPUTACION TOLERANTE A FALLAS | 02/03/2023

### OBJETIVO:
Introducción y Primeros pasos con Prefect (PyData Denver)
Seguir el tutorial marcado en plataforma y agregar un ejemplo propio

### DESARROLLO:
En el siguiente ejemplo, el codigo en python se encarga de ejecutar la tarea download_data que descarga los datos del conjunto de datos de calidad de vino de la Universidad de California en Irvine (UCI) obtenidos de un archivo csv, mientras que la tarea clean_data realiza la limpieza y transformación necesarias en el conjunto de datos antes de ejecutar el modelo de aprendizaje automático en la tarea run_model.

La plataforma Prefect garantiza que cada tarea se ejecuta en el orden correcto y que cualquier problema se detecta y se informa en tiempo real, lo que facilita el monitoreo y la solución de problemas del flujo de trabajo.

##### _(El codigo se puede descargar en el archivo de la parte superior)_

```python
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
```

### CONCLUSIÓN:
Este código es un ejemplo de cómo se puede estructurar un flujo de trabajo de ciencia de datos utilizando la biblioteca Prefect. En este caso, se define un flujo de trabajo que consta de tres tareas: extracción de datos, limpieza de datos y ejecución de un modelo de aprendizaje automático. En resumen, este código proporciona un ejemplo útil de cómo utilizar la biblioteca Prefect para crear flujos de trabajo eficientes y escalables para proyectos de ciencia de datos.
