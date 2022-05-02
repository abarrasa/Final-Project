from operator import ne
import modules.geo_calculations as geo
import pandas as pd
from geopy.geocoders import Nominatim 
from datetime import datetime
import folium
from prophet import Prophet

#dia_hoy=datetime.today().strftime('%d-%m-%Y')
#df_new = pd.read_excel(f"./df_diario {dia_hoy}.xlsx")


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
    #df_colores['Precio gasolina 95 E5'].replace('No disponible', pd.NA, inplace=True)
    df_colores['Precio gasolina 95 E5'] = df_colores['Precio gasolina 95 E5'].apply(lambda x: x.replace(',','.'))
    df_colores['Precio gasóleo A'] = df_colores['Precio gasóleo A'].apply(lambda x: x.replace(',','.'))
    df_colores['Precio gasolina 95 E5']=df_colores['Precio gasolina 95 E5'].astype('float64')
    df_colores['Precio gasóleo A']=df_colores['Precio gasóleo A'].astype('float64')
    #df_colores['Precio gasolina 95 E5']=df_colores['Precio gasolina 95 E5'].astype('float64')
    #df_colores['Precio gasóleo A']=df_colores['Precio gasóleo A'].astype('float64')
    #percentil_50=statistical_quartiles(df_colores,'Precio gasolina 95 E5', 50) #amarillo
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

def ubi_gasolinera(df_new):
    mapa_loop = folium.Map(location=[40.549986,-3.635939], zoom_start=13)
    for i in range(0,len(df_new)):
        html=f"""
            <div style="font-family: times new roman; color: black">
            <h><b> {df_new.iloc[i]['Rótulo']}</h></b>
            <p><b>Prices:</b></p>
                <li> Gasoline 95: {df_new.iloc[i]['Precio gasolina 95 E5']} €</li>
                <li> Diesel: {df_new.iloc[i]['Precio gasóleo A']} €</li>
            <p><b>Address:</b></p>
            <p>{df_new.iloc[i]['Dirección'].title}</p>
            """
        
        iframe = folium.IFrame(html=html, width=180, height=215)
        popup = folium.Popup(iframe, max_width=2650)
        
        if df_new.iloc[i]['Colores']== 'verde':
            folium.Marker(
                location=[df_new.iloc[i]['Latitud'],df_new.iloc[i]['Longitud']],
                popup=popup,
                icon=folium.Icon(color="green",  icon="ok-sign"),
            ).add_to(mapa_loop)
        elif df_new.iloc[i]['Colores']== 'amarillo':
            folium.Marker(
                location=[df_new.iloc[i]['Latitud'],df_new.iloc[i]['Longitud']],
                popup=popup,
                icon=folium.Icon(color="orange",  icon="ok-sign"),
            ).add_to(mapa_loop)
            
        elif df_new.iloc[i]['Colores']== 'rojo':
            folium.Marker(
                location=[df_new.iloc[i]['Latitud'],df_new.iloc[i]['Longitud']],
                popup=popup,
                icon=folium.Icon(color="red",  icon="ok-sign"),
            ).add_to(mapa_loop)
    html=f"""
        <div style="font-family: times new roman; color: black">
        <h><b> You are currently here </b></h></div>
        """
    iframe = folium.IFrame(html=html, width=180, height=25)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker(
        location=[df_new.iloc[0]['Latitud_partida'],df_new.iloc[0]['Longitud_partida']],
        popup=popup,
        icon=folium.Icon(color="cadetblue",  icon="home"),
).add_to(mapa_loop) 
    mapa_loop.save('./modules/map.html')
    return mapa_loop

def prediction(df_acum):
    df_acum['Precio gasolina 95 E5'] = df_acum['Precio gasolina 95 E5'].apply(lambda x: x.replace(',','.'))
    df_acum.drop(df_acum.loc[df_acum['Precio gasolina 95 E5']=='No disponible'].index, inplace=True)
    df_acum['Precio gasolina 95 E5']=df_acum['Precio gasolina 95 E5'].astype('float64')
    df_todas_gasolineras = df_acum.groupby(["Fecha de extracción"])["Precio gasolina 95 E5"].median()
    df_prophet_espana=pd.DataFrame(df_todas_gasolineras).reset_index()
    df_prophet_espana.columns = ['ds', 'y']
    format_data = '%d-%m-%Y'
    df_prophet_espana['ds']=df_prophet_espana['ds'].apply(lambda x: datetime.datetime.strptime(x,format_data))
    my_model = Prophet(interval_width=0.8, daily_seasonality=False, yearly_seasonality=False)
    my_model.fit(df_prophet_espana, iter=100)
    future = my_model.make_future_dataframe(periods=7)
    predict= my_model.predict(future)
    predict[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(9)
    my_model.plot(predict, uncertainty=True)
    my_model.plot_components(predict)
    return my_model.plot(predict, uncertainty=True)


#df_new = mercator_gas(df_new)
#print('sale_df_con_distance')
#df_new = colores()
#print('columna colores')

#mapa_loop = ubi_gasolinera(df_new)
#print('mapa gasolineras hecho')
#mapa_loop = ubi_actual(df_new)
#print('mapa ubi hecho')


