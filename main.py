from modules import acquisition as acq
from modules import Analysis as ana
import warnings
warnings.filterwarnings('ignore')
#from openpyxl.workbook import Workbook
import pandas as pd
import streamlit as st
#from geopy.geocoders import Nominatim 
#from datetime import datetime
from streamlit_folium import folium_static
import folium
from PIL import Image 
URL = 'https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/'

st.set_page_config(layout="wide")

st.title ("Gas Finder") 

col1, col2 = st.columns([3,5])
with col1:
    st.markdown("## Welcome to the official gas station search engine. Here you will find anything you want") 
with col2:
    st.image('./images/gasolinera.jpeg')

st.text_input("Please, enter your location here: (e.g.Calle de Augusto Figueroa, 67, Madrid") 
if st.button('Calculate!'):
    run = 'yes'
else:
    run = 'no'

if run == 'no':
        st.write('')
else:
    if __name__ == '__main__':
        data = acq.api(URL)
        df_new = acq.generate_excel_today(data)
        #df_definitivo = acq.generate_excel_accumulate(data)
        df_head = ana.mercator_gas(df_new)
        df_head = ana.colores(df_head)
        folium_static(ana.ubi_gasolinera(df_head))
        #graph = ana.prediction(df_definitivo) 
        #col1, col2, col3 = st.columns([1,4,2])
        #with col1: 
            #st.write("")  
        #with col2:
            #st.markdown("##Want to know next week´s prices?") 
        #with col3:
            #st.write("")
        #if st.button('Calculate!'):
            #run = 'yes'
    #else:
    #run = 'no'

#if run == 'no':
        #st.write('')