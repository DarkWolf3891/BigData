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

root_dir = 'gs://jaime_varela_llamadas123'

# Funcion para leer cargar los archivos de filename
def get_data(filename):

    data_dir = "raw"
    file_path = os.path.join(root_dir, "data", data_dir, filename)
    data = pd.read_csv(file_path, encoding='latin-1', sep=';')
    
    return data;

# Eliminar registros duplicados
def data_drop_duplicate(data):
    
    data = data.drop_duplicates() # elimina los datos duplicados
    data = data.reset_index()
    return data;

# Reemplazo la columna UNIDAD que tenia valores nulos por una columna nueva sin nulos
def data_sin_dato(data):
    
    data['UNIDAD'] = data['UNIDAD'].fillna('SIN_DATO') #

    return data;

# Manipulacion Fechas (datetime)
def data_date_time(data):
    
    data.rename(
                columns = {
                            'FECHA_INICIO_DESPLAZAMIENTO-MOVIL' : 'FECHA_INICIO_DESPLAZAMIENTO_MOVIL',
                            'FECHA_DESPACHO_518' : 'FECHA_INICIO_DESPLAZAMIENTO_MOVIL',
                            'COD_LOCALIDAD' : 'CODIGO_LOCALIDAD'
                          },
                inplace=True
                )
    
    col = 'FECHA_INICIO_DESPLAZAMIENTO_MOVIL'
    data[col] = pd.to_datetime(data[col], errors='coerce')
    
    return data;

# # Consistencia de los Datos: Recepcion
def data_consistencia_recepcion(data):
    
    # Como Los datos antiguos no tienen RECEPCION ecepcin se crea a partir de FECHA_INICIO_DESPLAZAMIENTO_MOVIL  
    
    data['RECEPCION'] = data['FECHA_INICIO_DESPLAZAMIENTO_MOVIL']
    
    def convertir_formato_fecha(str_fecha):
        val_datetime = parse(str_fecha, dayfirst=False, yearfirst = False)
        return val_datetime

    list_fecha = list()
    n_fila = data.shape[0] 

    for i in range(0,n_fila):

        str_fecha = data['RECEPCION'][i]

        try:
            val_datetime = convertir_formato_fecha(str_fecha=str_fecha)
            list_fecha.append(val_datetime)
        except Exception:
            list_fecha.append(str_fecha)
            continue
    data['RECEPCION_CORREGIDA'] = list_fecha
    data['RECEPCION_CORREGIDA']= pd.to_datetime(data['RECEPCION_CORREGIDA'], errors='coerce')
    return data;     
    
# Consistencia de los Datos: Edad
def data_consistencia_edad(data):

    #data['EDAD'] = data['EDAD'].replace({'SIN_DATO' : np.nan})
    #f = lambda x: x if pd.isna(x) == True else int(x)
    #data['EDAD'] = data['EDAD'].apply(f)

    data['EDAD'] = data['EDAD'].fillna('SIN_DATO')
    
    return data;

# Consistencia de los Datos: Localidad
def data_consistencia_localidad(data):

    Localidades = { 1:'USAQUEN', 2:'CHAPINERO', 3:'SANTA FE', 4:'SAN CRISTOBAL', 5:'USME', 
                    6:'TUNJUELITO', 7:'BOSA', 8: 'KENNEDY', 9: 'FONTIBON', 10: 'ENGATIVA',
                    11: 'SUBA', 12: 'BARRIOS UNIDOS', 13: 'TEUSAQUILLO', 14: 'LOS MARTIRES',
                    15: 'ANTONIO NARIÑO', 16: 'PUENTE ARANDA', 17: 'LA CANDELARIA', 18: 'RAFAEL URIBE URIBE',
                    19: 'CIUDAD BOLIVAR', 20: 'SUMAPAZ'}

    data['LOCALIDAD'] = data['CODIGO_LOCALIDAD'].map(Localidades)

    return data;

# Consistencia de los Datos: genero 
def data_consistencia_genero(data):
    
    data['GENERO'] = data['GENERO'].str.upper()
    
    return data  

# Consistencia de los Datos: prioridad 
def data_consistencia_prioridad(data):
    
    data['PRIORIDAD'] = data['PRIORIDAD'].replace(['CRITCA'], 'CRITICA')
    
    return data;

# Guarda el data frame limpio
def save_data(data, filename):
        
    data_dir = "processed"
    out_name = 'Clean_' + filename
    out_path = os.path.join(root_dir, "data", data_dir, out_name)
    data.to_csv(out_path)
    print(data.info())
    
    #Guardar la tabla en BigQuery
    data.to_gbq(destination_table='EspBigDataJVR2022.llamadas_123_2021_2022',if_exists='append')

def main():

    #filename = "llamadas123_julio_2022.csv"
    #filename = "llamadas123_junio_2022.csv"
    #*filename = "datos_llamadas123_mayo_2022.csv" # Edad
    #*filename = "datos_abiertos_abril_2022.csv" # Edad 
    #filename = "datos_abiertos_marzo_2022.csv" # 'FECHA_INICIO_DESPLAZAMIENTO-MOVIL' : 'FECHA_INICIO_DESPLAZAMIENTO_MOVIL'
    #filename = "datos_abiertos_febrero_2022.csv" # Falta la columna recepcion
    #filename = "datos_abiertos_enero_2022.csv" # Falta la columna recepcion
    #*filename = "llamadas_123_diciembre_2021.csv" # Falta la columna recepcion, en desorden
    #filename = "llamadas_123_noviembre_2021.csv" # Falta la columna recepcion
    #*filename = "llamadas_123_octubre_2021.csv" # Falta la columna recepcion, dos columnas vacias al final
    #*filename = "llamadas_123_septiembre2021.csv" # Falta la columna recepcion, codigo localidad en float64 => int64
    #filename = "llamadas_123_agosto2021.csv" # Falta la columna recepcion
    #filename = "llamadas_123_julio2021.csv" # Falta la columna recepcion
    #filename = "llamadas_123_junio2021.csv" # Falta la columna recepcion
    #*filename = "llamadas_123_mayo2021.csv" # Falta la columna recepcion # KeyError: 'FECHA_INICIO_DESPLAZAMIENTO_MOVIL', codigo localidad en float64 => int64
    #filename = "llamadas_123_abril2021.csv" # Falta la columna recepcion
    #*filename = "llamadas_123_marzo2021.csv" # Falta la columna recepcion, *edad en float64 => str
    #*filename = "llamadas_123_febrero2021.csv" # Falta la columna recepcion, KeyError: 'CODIGO_LOCALIDAD', *codigo localidad en float64 => int64
    #filename = "llamadas_123_-enero2021.csv" # Falta la columna recepcion

    data = get_data(filename)
    data = data_drop_duplicate(data)
    data = data_sin_dato(data)
    data = data_date_time(data)
    data = data_consistencia_recepcion(data)
    data = data_consistencia_edad(data)
    data = data_consistencia_localidad(data)
    data = data_consistencia_genero(data)
    data = data_consistencia_prioridad(data)
    save_data(data, filename)

    print('DONE!!!')

if __name__ == '__main__':
    main()