# Workflow managers with Python Part.1
#### BARAJAS GOMEZ JUAN MANUEL | 216557005 | COMPUTACION TOLERANTE A FALLAS | 2/03/2023

### OBJETIVO:
Introducción y Primeros pasos con Prefect (PyData Denver)
Seguir el tutorial marcado en plataforma y agregar un ejemplo propio

### DESARROLLO:
Prefect es una plataforma de automatización de flujo de trabajo (workflow) en Python que se utiliza para orquestar, monitorear y administrar procesos y tareas.

Permite definir flujos de trabajo complejos y ajustables que se ejecutan de manera confiable en diferentes entornos de infraestructura, desde máquinas locales hasta clústeres en la nube.

Entre las principales características de Prefect se encuentran la capacidad de definir tareas con funciones decoradas con @task, integración con tecnologías populares como Docker, Kubernetes y AWS, un panel de control web para monitorear el estado de los flujos de trabajo, y una API extensible para personalizar el comportamiento y las funciones de la plataforma.

Prefect se utiliza en una amplia gama de aplicaciones, desde la ciencia de datos y el aprendizaje automático hasta la automatización de procesos empresariales y la administración de infraestructuras.


### EJEMPLO:
```python
import prefect
from prefect import task, Flow

@task
def say_hello():
    print("Hello, world!")

with Flow("My first flow") as flow:
    say_hello()

flow.run()
```

### EJEMPLO EN PRACTICA:
El código mostrado en el ejemplo del video proporcionado en la plataforma por el profesor se desarrolla en Python, implementa un flujo de extracción, transformación y carga (ETL) de datos utilizando la librería Prefect. El objetivo del flujo es obtener datos de quejas de consumidores del sitio web de la Oficina de Protección Financiera del Consumidor (CFPB, por sus siglas en inglés), transformarlos en una estructura de datos más manejable y almacenarlos en una base de datos SQLite.

##### _(El codigo se puede descargar en el archivo de la parte superior)_

```python
import requests # Importar la librería 'requests' para realizar peticiones HTTP a una API
import json # Importar la librería 'json' para trabajar con datos en formato JSON
from collections import namedtuple # Importar la función 'namedtuple' para crear una clase que represente las quejas
from contextlib import closing # Importar la función 'closing' para asegurarse de que las conexiones a la base de datos se cierren correctamente
import sqlite3 # Importar la librería 'sqlite3' para conectarse y trabajar con una base de datos SQLite
from prefect import task, Flow # Importar las funciones 'task' y 'Flow' de la librería 'Prefect' para definir tareas y un flujo de trabajo

## extract
@task # Decorar la función 'get_complaint_data' con la función 'task' para que se convierta en una tarea de Prefect
def get_complaint_data():
    r = requests.get("https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/", params={'size':10}) # Hacer una petición HTTP GET a la API de CFPB con un parámetro de tamaño de respuesta de 10
    response_json = json.loads(r.text) # Analizar la respuesta de la API como un objeto JSON
    return response_json['hits']['hits'] # Devolver una lista de quejas de la respuesta analizada

## transform
@task # Decorar la función 'parse_complaint_data' con la función 'task' para que se convierta en una tarea de Prefect
def parse_complaint_data(raw):
    complaints = [] # Crear una lista vacía para almacenar las quejas procesadas
    Complaint = namedtuple('Complaint', ['data_received', 'state', 'product', 'company', 'complaint_what_happened']) # Crear una clase 'Complaint' utilizando 'namedtuple' para representar las quejas como objetos
    for row in raw: # Iterar sobre cada fila en la lista de quejas
        source = row.get('_source') # Obtener el objeto de datos subyacente para cada queja
        this_complaint = Complaint(
            data_received=source.get('date_recieved'), # Obtener la fecha de recepción de la queja
            state=source.get('state'), # Obtener el estado donde se presentó la queja
            product=source.get('product'), # Obtener el producto financiero relacionado con la queja
            company=source.get('company'), # Obtener la empresa financiera relacionada con la queja
            complaint_what_happened=source.get('complaint_what_happened') # Obtener los detalles de la queja
        ) # Crear un objeto 'Complaint' con los datos de la queja
        complaints.append(this_complaint) # Agregar el objeto 'Complaint' a la lista de quejas procesadas
    return complaints # Devolver la lista de quejas procesadas

## load
@task
def store_complaints(parsed):
    # Crear una cadena que define la tabla 'complaint' y sus columnas
    create_script = 'CREATE TABLE IF NOT EXISTS complaint (timestamp TEXT, state TEXT, product TEXT, company TEXT, complaint_what_happened TEXT)'
    # Crear una cadena que inserta los datos en la tabla 'complaint'
    insert_cmd = "INSERT INTO complaint VALUES (?, ?, ?, ?, ?)"

    # Conectar a la base de datos 'cfpbcomplaints.db' utilizando el módulo 'sqlite3'
    with closing(sqlite3.connect("cfpbcomplaints.db")) as conn:
        # Crear un cursor para la conexión a la base de datos
        with closing(conn.cursor()) as cursor:
            # Ejecutar la cadena 'create_script' en la base de datos utilizando el cursor
            cursor.executescript(create_script)
            # Ejecutar la cadena 'insert_cmd' con los datos transformados 'parsed' en la base de datos utilizando el cursor
            cursor.executemany(insert_cmd, parsed)
            # Confirmar los cambios en la base de datos
            conn.commit()

# Crear un nuevo flujo de Prefect llamado 'my etl flow'
with Flow("my etl flow") as f:
    # Definir una tarea 'raw' que utiliza la función 'get_complaint_data()' para descargar los datos de quejas
    raw = get_complaint_data()
    # Definir una tarea 'parsed' que utiliza la función 'parse_complaint_data()' para analizar y transformar los datos descargados por 'raw'
    parsed = parse_complaint_data(raw)
    # Definir una tarea 'store_complaints' que toma los datos transformados 'parsed' y los inserta en la base de datos utilizando la función 'store_complaints()'
    store_complaints(parsed)

# Ejecutar el flujo 'f' que incluye las tareas 'raw', 'parsed' y 'store_complaints'
f.run()
```
### CAPTURAS:
![Captura de pantalla de 2023-03-02 21-02-27](https://user-images.githubusercontent.com/101375005/222625384-fcfcd434-49f3-446a-927d-f679a61ce96f.png)
![Captura de pantalla de 2023-03-02 21-01-16](https://user-images.githubusercontent.com/101375005/222625387-9d6b535b-b05f-47a6-a4b2-7209f67d2b76.png)
![Captura de pantalla de 2023-03-02 21-01-43](https://user-images.githubusercontent.com/101375005/222625390-27ebaab2-c10f-422c-95a7-fc5aea309ef2.png)

### CONCLUSIÓN:
En el código proporcionado, se utiliza Prefect para automatizar el flujo de trabajo de extracción, transformación y carga de datos (ETL) desde una fuente externa a una base de datos local. Al definir las tareas con @task, el código se vuelve más modular y fácil de entender, lo que facilita la escalabilidad y el mantenimiento del flujo de trabajo en el futuro.
Además, el panel de control web de Prefect proporciona una forma conveniente de monitorear el progreso de la ejecución del flujo de trabajo y detectar rápidamente cualquier problema que surja durante el proceso. 

En general, el uso de Prefect ayuda a mejorar la eficiencia y la confiabilidad de los flujos de trabajo de ETL, lo que es beneficioso para cualquier proyecto que involucre la extracción y transformación de datos.


### REFERENCIAS:
_Prefect. (2020, 17 abril). Getting Started with Prefect (PyData Denver) [Vídeo]. YouTube. https://www.youtube.com/watch?v=FETN0iivZps_
