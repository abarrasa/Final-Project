import pandas as pd
import requests
from datetime import datetime 
URL = 'https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/'


def api(url):
    request = requests.get(url)
    response = request.json()
    return response 

def generate_excel_today(data):   
    df_new=pd.DataFrame(data['ListaEESSPrecio'])
    df_new = df_new.rename(columns={'Longitud (WGS84)':'Longitud','C.P.':'Código postal', 'Remisión': 'Rem.', '% Éster metílico': '% éster metílico','Precio Gasolina 95 E5': 'Precio gasolina 95 E5','Precio Gasolina 95 E5 Premium': 'Precio gasolina 95 E5 Premium', 'Precio Gasolina 98 E5': 'Precio gasolina 98 E5', 'Precio Gasoleo A': 'Precio gasóleo A', 'Precio Gasoleo Premium': 'Precio gasóleo Premium'})
    df_new=df_new.drop(columns=['IDProvincia', 'IDEESS', 'IDMunicipio', 'IDCCAA'])
    df_new = df_new[['Provincia','Municipio','Localidad','Código postal','Dirección','Longitud', 'Latitud', 'Precio gasolina 95 E5','Precio gasolina 95 E5 Premium', 'Precio gasolina 98 E5', 'Precio gasóleo A', 'Precio gasóleo Premium', 'Rótulo', 'Horario']]
    df_new['Fecha de extracción']=datetime.today().strftime('%d-%m-%Y')
    df_new = df_new.replace('', 'No disponible')
    dia_hoy=datetime.today().strftime('%d-%m-%Y')
    print('Generando df_new')
    df_new.to_excel(f"./data/df_diario {dia_hoy}.xlsx", index=False)
    return df_new 

def generate_excel_accumulate(data):
    df_acum= pd.read_excel('./data/df_definitivo.xlsx')
    df_new = generate_excel_today(data)
    print('Concat df_new y df_acum')
    df_union=pd.concat([df_acum, df_new])
    print('creando df_definitivo')
    df_definitivo = pd.DataFrame(df_union.values, columns=df_new.columns)
    dia = datetime.today().strftime('%d-%m-%Y')
    print('Generando copia de seguridad')
    df_definitivo.to_excel(f"./data/df_copia_seguridad{dia}.xlsx", index=False)
    print('Generando df_definitivo')
    df_definitivo.to_excel('./data/df_definitivo.xlsx', index=False)
    return df_definitivo



   