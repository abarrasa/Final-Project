import geo_calculations as geo
import pandas as pd
from geopy.geocoders import Nominatim 
from datetime import datetime 

dia_hoy=datetime.today().strftime('%d-%m-%Y')
df_new = pd.read_excel(f"./Final-Project/df_diario {dia_hoy}.xlsx")

direccion_usuario= input("Please, Enter your location: ")

def mercator_gas():
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
    return df_new


df_new = mercator_gas()
print(df_new)