import os
import datetime
import pandas as pd
import random

def getData(fichero_path,frequencies):
    df = pd.read_csv(fichero_path, sep=";", skiprows=3)
    df.rename(columns={'Unnamed: 1':'Fecha','Unnamed: 2':'Hora', 'I (W/m2)':'Radiacion','T (K)':'Temperatura'},inplace=True)
    df = df[['Fecha', 'Hora', 'Radiacion', 'Temperatura']].copy()
    df=df[df.Hora.isin(frequencies)]
    #df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d').dt.strftime('%m')
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.strftime('%H')
    return df[['Fecha', 'Hora', 'Radiacion', 'Temperatura']]


path_mediciones = 'C:\MEDICIONES'
datos= pd.DataFrame(columns=['Fecha', 'Hora', 'Radiacion', 'Temperatura'])
frequencies= pd.date_range(start='2019-01-01 00:00:00', end='2019-01-02 00:00:00', freq='5T').strftime("%H:%M:%S")

with os.scandir(path_mediciones) as carpetas:
    subdirectorios = [carpeta.name for carpeta in carpetas if carpeta.is_dir()]

for carpeta in subdirectorios:
    print(carpeta)
    with os.scandir(path_mediciones + '\\' + carpeta) as ficheros:
        lista_ficheros = list(ficheros)
        num_el=len(lista_ficheros)
        if(num_el>10):
            pos_ficheros= random.sample(range(num_el), 10)
        else:
            pos_ficheros= range(num_el)
        for pos in pos_ficheros:
            print(lista_ficheros[pos].path)
            datos_fichero=getData(lista_ficheros[pos].path,frequencies)
            datos = pd.concat([datos,datos_fichero])

datos.to_csv("datos.csv",index=False)


