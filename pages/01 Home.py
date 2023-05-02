import streamlit as st
import pandas as pd
import plotly.express as px
from funciones_app import filter_area_perimetro
from conect_datarows import setle_clean,selec_setle, animl_clean, df_gps
import plotly.express as px

st.image('imagenes/Header_bastó.jpeg')

st.title('Información general')

st.write('Gracias a la base de datos podemos saber el conteo de animales en el sigue menú.')

animals= animl_clean()
setle= setle_clean()# arroja dataframe arreglado de setle---


select_an= st.selectbox('Seleccione tipo de animal:',animals.animalType.unique())


df=animals[animals['animalType']==select_an]
a= df['animalType'].count()
b= animals['animalType'].count()

clicked = st.button("Conteo animales")
if clicked:
    st.write(
        f"En esta área hay: {a}:"
    )
    st.write(
        f"En total hay: {b}"
    )
    st.write('La semana en las que más hubo registros dentro de este potrero fueron de 13 del año. Que comprenden del 20 al 34 de marzo del 2023')
    df.createdAt= pd.to_datetime(df.createdAt)
    data_week= df.groupby(['_id',df.createdAt.dt.week]).agg({'createdAt':'count'}).rename(columns={'createdAt':'count_register'})
    data_week=data_week.reset_index()

    fig= px.bar( data_week,x='createdAt',y='count_register')
    st.plotly_chart(fig,use_container_width=True) 


clicked_2 = st.button("Más informacion")

if clicked_2:
    st.write(
        f"El peso promedio de esta población es: {df['weight'].mean()}, con una desviación estandar de {df['weight'].std()}"

    )
    st.write(
        f"Las razas registradas son: {pd.DataFrame(df['breed'].value_counts())} "
    )



st.title('Información de Potrero de interés')


select_sl= st.selectbox('Seleccione un asentamiento a evaluar:',setle.name.unique())
nombre= setle[setle.name==select_sl]._id.values[0]
print(nombre)
elec_setle= selec_setle(setle,nombre) # arroja dataframe pequeño de un solo dato del asentamiento---

on_perimetro=filter_area_perimetro(df_gps,elec_setle.latitud_c, elec_setle.longitud_c, elec_setle.hectares)# arroja dataframe---
uuid_devis = on_perimetro.UUID.unique()

clicked_3 = st.button("Conteo dispositivo")
if clicked_3:
    st.write(
        f"En esta área hay: {len(uuid_devis)} collares que proveen datos de GPS de un total de 518 vacas en total"
    )
    

