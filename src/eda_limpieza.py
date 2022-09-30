# Pseudo Codigo
# 1. leer archivo .csv
# 2. Eliminar registros duplicados
# 3. Reemplazo la columna UNIDAD que tenia valores nulos por una columna nueva sin nulos
# 4. Convierte str en formato de fecha
# 5. Manipulacion Fechas (datetime)
# 6. Consistencia de los Datos: Edad cambia el str por int
# 7. Consistencia de los Datos: Localidad organiza los nombre usando un diccionario

# importar librerias del sistema
import numpy as np
import pandas as pd

# importar librerias del sistema
import os
from pathlib import Path

# manipulacion de fechas
from dateutil.parser import parse

root_dir = Path(__file__).resolve().parent.parent

# Funcion para leer cargar los archivos de filename
def get_data(filename):


    print(root_dir)
    data_dir = "raw"
    file_path = os.path.join(root_dir, "data", data_dir, filename)
    data = pd.read_csv(file_path, encoding='latin-1', sep=';')
    
    return data

# Eliminar registros duplicados
def data_drop_duplicate(data):
    
    data = data.drop_duplicates() # elimina los datos duplicados
    
    return data

# Reemplazo la columna UNIDAD que tenia valores nulos por una columna nueva sin nulos
def data_sin_dato(data):
    
    data['UNIDAD'] = data['UNIDAD'].fillna('SIN_DATO') #

    return data

# Convierte str en formato de fecha
def convertir_formato_fecha(str_fecha):

    val_datetime = parse(str_fecha, dayfirst=True)
    return val_datetime

# Manipulacion Fechas (datetime)
def data_date_time(data):
    
    col = 'FECHA_INICIO_DESPLAZAMIENTO_MOVIL'
    data[col] = pd.to_datetime(data[col], errors='coerce')
    data = data.reset_index()

    list_fechas = list()
    n_filas = data.shape[0]  # len(data['RECEPCION'])

    for i in range(0,n_filas):
        
        str_fecha = data['RECEPCION'][i]
        
        try:
            val_datetime = convertir_formato_fecha(str_fecha= str_fecha)
            list_fechas.append(val_datetime)
        except Exception as e:
            print(i, e)
            list_fechas.append(str_fecha)
            continue

    data['RECEPCION_CORREGIDA'] = list_fechas
    pd.to_datetime(data['RECEPCION_CORREGIDA'],errors='coerce')

    return data

# Consistencia de los Datos: Edad
def data_consistencia_edad(data):

    data['EDAD'] = data['EDAD'].replace({'SIN_DATO' : np.nan})
    
    f = lambda x: x if pd.isna(x) == True else int(x)
    data['EDAD'] = data['EDAD'].apply(f)

    return data

# Consistencia de los Datos: Localidad
def data_consistencia_localidad(data):

    Localidades = { 1:'USAQUEN', 2:'CHAPINERO', 3:'SANTA FE', 4:'SAN CRISTOBAL', 5:'USME', 
                    6:'TUNJUELITO', 7:'BOSA', 8: 'KENNEDY', 9: 'FONTIBON', 10: 'ENGATIVA',
                    11: 'SUBA', 12: 'BARRIOS UNIDOS', 13: 'TEUSAQUILLO', 14: 'LOS MARTIRES',
                    15: 'ANTONIO NARIÑO', 16: 'PUENTE ARANDA', 17: 'LA CANDELARIA', 18: 'RAFAEL URIBE URIBE',
                    19: 'CIUDAD BOLIVAR', 20: 'SUMAPAZ'}

    data['LOCALIDAD'] = data['CODIGO_LOCALIDAD'].map(Localidades)

    return data 

# Guarda el data frame limpio
def save_data(data, filename):
        
    data_dir = "processed"
    out_name = 'Clean_' + filename
    out_path = os.path.join(root_dir, "data", data_dir, out_name)
    data.to_csv(out_path)

def main():

    filename = "llamadas123_julio_2022.csv"
    data = get_data(filename)
    data = data_drop_duplicate(data)
    data = data_sin_dato(data)
    data = data_date_time(data)
    data = data_consistencia_edad(data)
    data = data_consistencia_localidad(data)
    save_data(data, filename)

    print('DONE!!!')

if __name__ == '__main__':
    main()
