from modules import acquisition as acq
from modules import reporting as rep
from modules import Analysis as ana
import warnings
warnings.filterwarnings('ignore')
#from openpyxl.workbook import Workbook
import pandas as pd
import streamlit as st
#from geopy.geocoders import Nominatim 
from datetime import datetime
from streamlit_folium import folium_static
import folium
from PIL import Image 
URL = 'https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/'

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns(3)
col1.write("")
col2.title('Gas Station Finder')
col3.write("")

for i in range(5):
    st.write("")

col1, col2 = st.columns([5,5])
with col1:
    st.caption("## Welcome to the official gas station search engine.")
    st.caption("## Here you will find anything you want!") 
with col2:
    st.image('./images/gasolinera.jpeg',width=430)


for i in range(5):
    st.write("")

direccion_usuario=st.text_input("Please, enter your location here: (e.g. Calle Augusto Figueroa, 67, Madrid)") 
if st.button('Search!'):
    run = 'yes'
else:
    run = 'no'

if run == 'no':
        st.write('')
else:
    if __name__ == '__main__':
        #st.info("Searching...")
        data = acq.api(URL)
        df_new = acq.generate_excel_today(data)
        df_definitivo = acq.generate_excel_accumulate(data)
        df_head = ana.mercator_gas(df_new, direccion_usuario)
        df_head = ana.colores(df_head)
        
        col1, col2, col3 = st.columns([1,4,2])
        with col1:
            st.write("")
        with col2:
            folium_static(rep.ubi_gasolinera(df_head))
        with col3:
            st.write("")
        
        col1, col2, col3 = st.columns([4,1,2])
        with col1:
            st.markdown("## Want to know next week´s prices?") 
        
        col1, col2, col3 = st.columns([1,4,2])
        with col1:
            st.write("")
        with col2:
            st.write("todo es correcto")
            graph=rep.prediction(df_definitivo)
            st.write(graph,width=430)
        with col3:
            st.write("")
       
       
       
            
        #if st.button('Predict!'):    
            #run = 'yes'
        #else:
            #run = 'no'
        
        
        #if run == 'no':
            #st.write('')
        #else:
            #graph=rep.prediction(df_definitivo)
            #st.write(graph)

            