import pandas as pd
import streamlit as st

# Streamlit run Dashboard.py

st.set_page_config(page_title = 'Reporte Casos Covid', 
                   page_icon = ':female-doctor:',
                   layout="wide")

st.title(':clipboard: Reporte Casos Covid') 
st.subheader('29-04-2022')
st.markdown('##')
                   
archivo_excel = 'Reporte de Ventas.xlsx' 
hoja_excel = 'BASE DE DATOS' 
 
#============== LIMPIEZA DEL DATASET ================================================================================
covid = pd.read_csv("poblacion/covid.csv")
poblacion = pd.read_csv("poblacion/poblacion_municipio.csv")

covid['Casos']= covid['Casos'].str.replace(',','')
covid['Defunciones']= covid['Defunciones'].str.replace(',','')
poblacion['Habitantes 2020'] = poblacion['Habitantes 2020'].str.replace(',','')

covid['Casos']= covid['Casos'].astype('float64')
covid['Defunciones']= covid['Defunciones'].astype('float64')
poblacion['Habitantes 2020'] = poblacion['Habitantes 2020'].astype('float64')

covid.drop(covid.tail(1).index,inplace=True)
covid = covid.fillna(0)


covid = pd.merge(covid,poblacion, how='outer', on=['Municipio']).drop('Clave del municipio', axis=1)

#=======================================================================================================================

covid['Tasa de Defunción (%)'] = covid['Defunciones'] / covid['Casos'] * 100

#st.dataframe(covid)

st.sidebar.header("Opciones a filtrar:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
Municipio = st.sidebar.multiselect(
    "Seleccione el Municipio:",
    options = covid['Municipio'].unique(),
    default = covid['Municipio'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)





df_seleccion = covid.query("Municipio==@Municipio" )


total_casos = int(df_seleccion['Casos'].sum())

total_defunciones = int(df_seleccion['Defunciones'].sum())

total_habitantes = int(df_seleccion['Habitantes 2020'].sum())

left_column, midle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Casos Totales:")
    st.subheader(f"{total_casos:,}")

with midle_column:
    st.subheader('Defunciones Totales:')
    st.subheader(f" {total_defunciones:,}")

with right_column:
    st.subheader('Habitantes Totales:')
    st.subheader(f" {total_habitantes:,}")


st.markdown("---") 

st.dataframe(df_seleccion) 