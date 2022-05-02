import osmnx as ox
import pandas as pd
import geocoder
from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
import matplotlib.pyplot as plt 
import datetime
import warnings
warnings.filterwarnings('ignore')
from prophet import Prophet
from fbprophet.plot import plot_plotly
import plotly.offline as py


#st.title('prediction')

#df_acum = pd.read_excel("./df_copia_seguridad02-05-2022.xlsx")

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
    graph = my_model.plot(predict, uncertainty=True)
    graph.savefig("prediction_prophet.jpg")
    my_model.plot_components(predict)
    return graph

#graph=prediction(df_acum)
#st.write(graph)
