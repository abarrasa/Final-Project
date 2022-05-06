from operator import ne
import modules.geo_calculations as geo
import pandas as pd
from geopy.geocoders import Nominatim 
from datetime import datetime
import folium
from prophet import Prophet


def mercator_gas(df_new, direccion_usuario):
    geolocator = Nominatim(user_agent="My-App")
    location = geolocator.geocode(direccion_usuario)
    df_new['Latitud'] = df_new['Latitud'].apply(lambda x: x.replace(',','.'))
    df_new['Longitud'] = df_new['Longitud'].apply(lambda x: x.replace(',','.'))
    df_new['Latitud_partida'] = location.latitude
    df_new['Longitud_partida'] = location.longitude
    df_new['Latitud']=df_new['Latitud'].astype('float64')
    df_new['Longitud']=df_new['Longitud'].astype('float64')
    df_new["mercator_start"] = df_new.apply(lambda x: geo.to_mercator(x['Latitud_partida'],x['Longitud_partida']),axis=1)
    df_new["mercator_finish"] = df_new.apply(lambda x: geo.to_mercator(x['Latitud'],x['Longitud']),axis=1)
    df_new["Distance"] = df_new.apply(lambda x: geo.distance_meters(x['mercator_start'],x['mercator_finish']),axis=1)
    print("ha hecho el mercator")
    df_new=df_new.sort_values(by=['Distance'])
    print("ha ordenado por distancia")
    df_head=df_new.head(10)
    return df_head

def statistical_quartiles(dataset, column, percentile):
    lst = dataset[column].tolist()
    data = sorted(lst)
    if percentile != 100:
        index = int((len(data))*percentile/100)
        #Par, si el resto es 0.  
        if len(lst) % 2 != 0:
            return data[index]
        else:
            return (data[index - 1] + data[index]) / 2
    elif percentile == 100:
        index = int(len(data))-1  
        return data[index]

def colores(df_new):
    df_colores = df_new.iloc[:,[7,10]]
    df_colores['Precio gasolina 95 E5'] = df_colores['Precio gasolina 95 E5'].apply(lambda x: x.replace(',','.'))
    df_colores['Precio gasóleo A'] = df_colores['Precio gasóleo A'].apply(lambda x: x.replace(',','.'))
    df_colores['Precio gasolina 95 E5']=df_colores['Precio gasolina 95 E5'].astype('float64')
    df_colores['Precio gasóleo A']=df_colores['Precio gasóleo A'].astype('float64')
    percentil_75=statistical_quartiles(df_colores,'Precio gasolina 95 E5', 75) #rojo
    percentil_25=statistical_quartiles(df_colores,'Precio gasolina 95 E5', 25) #verde  
    df_new['Precio gasolina 95 E5'] = df_new['Precio gasolina 95 E5'].apply(lambda x: x.replace(',','.'))
    df_new['Precio gasóleo A'] = df_new['Precio gasóleo A'].apply(lambda x: x.replace(',','.'))
    df_new['Precio gasóleo A']=df_new['Precio gasóleo A'].astype('float64')
    df_new['Precio gasolina 95 E5']=df_new['Precio gasolina 95 E5'].astype('float64')
    bins = [0,percentil_25,percentil_75,100]
    colores = ['verde','amarillo','rojo']
    df_new['Colores']= pd.cut(df_new['Precio gasolina 95 E5'],bins,labels = colores)
    return df_new



