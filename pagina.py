import streamlit as st
import fun_main as fun
import numpy as np
import pandas as pd
from collections import Counter
import plotly.graph_objs as go
import plotly.express as px


import ast

st.title('Proyecto Final')

frase = st.text_input('Buscar tema de interes')

if st.button('Buscar'):
    busqueda = frase
    st.write(f'Frase ingresada: {busqueda}')
    #1 Crear el datafrrame con la base
    df = fun.CrearDatset(frase)
    st.write(f'Base de datos guardada')



if st.button('Graficar'):
    # leer dataframe
    df = pd.read_csv('data.csv', encoding='utf-8')
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['text_clean'] = df['text_clean'].apply(lambda x: ast.literal_eval(x))
    df['hashtag'] = df['hashtag'].apply(lambda x: ast.literal_eval(x))
    df['menciones'] = df['menciones'].apply(lambda x: ast.literal_eval(x))

    # grafica tokens
    token_list = np.concatenate(df['text_clean'].values)
    frecuencias_token = Counter(token_list)
    top_palabras = frecuencias_token.most_common(10)
    tokens, frec_tokens = zip(*top_palabras)
    # Crear una gráfica de barras horizontal en Plotly
    fig_1 = go.Figure(go.Bar(
        x=list(reversed(frec_tokens)),
        y=list(reversed(tokens)),
        orientation='h'
    ))
    # Configurar los títulos y ejes
    fig_1.update_layout(
        title='Palabras más frecuentes en la búsqueda',
        xaxis_title='Frecuencia',
        yaxis_title='Palabras'
    )
    # st.plotly_chart(fig_1)

    hashtag_list = np.concatenate(df['hashtag'].values)
    frec_hashtag = Counter(hashtag_list)
    top_hashtag = frec_hashtag.most_common(10)  # las palabras más frecuentes
    hashtag, frec_hashtag = zip(*top_hashtag)
    # Grafica el histograma
    fig_2 = go.Figure(go.Bar(
        x=list(reversed(frec_hashtag)),
        y=list(reversed(hashtag)),
        orientation='h'
    ))
    # Configurar los títulos y ejes
    fig_2.update_layout(
        title='Hashtags más frecuentes en la búsqueda',
        xaxis_title='Frecuencia',
        yaxis_title='Hashtag'
    )
    #st.plotly_chart(fig_2)

    menciones_list = np.concatenate(df['menciones'].values)
    frec_menciones = Counter(menciones_list)
    top_menciones = frec_menciones.most_common(10)  # las palabras más frecuentes
    menciones, frec_menciones = zip(*top_menciones)
    # Grafica el histograma
    fig_3 = go.Figure(go.Bar(
        x=list(reversed(frec_menciones)),
        y=list(reversed(menciones)),
        orientation='h'
    ))
    # Configurar los títulos y ejes
    fig_3.update_layout(
        title='Menciones más frecuentes en la búsqueda',
        xaxis_title='Frecuencia',
        yaxis_title='Menciones'
    )
    # Agrupar los datos por hora y contar las frecuencias de cada hora
    frecuencias_por_hora = df.groupby(pd.Grouper(key='fecha', freq='H')).count()['text']

    # Crear una figura interactiva de Plotly y agregar un gráfico de línea
    fig_4 = go.Figure()
    fig_4.add_trace(go.Scatter(x=frecuencias_por_hora.index, y=frecuencias_por_hora.values, mode='lines'))

    # Configurar los títulos y ejes de la gráfica
    fig_4.update_layout(
        title='Frecuencia por hora',
        xaxis_title='Hora',
        yaxis_title='Frecuencia'
    )

    # Contar el número de tweets en cada categoría de sentimiento
    num_tweets = df['sentimiento'].value_counts()
    # Crear figura de pastel
    fig_5 = px.pie(num_tweets, values=num_tweets.values, names=num_tweets.index,
                 title='Distribución de sentimientos en los tweets')

    fig_1.update_layout(width=None, height=None, margin=dict(l=0, r=0, t=30, b=0))
    # Mostrar la gráfica de Plotly en la aplicación Streamlit
    st.plotly_chart(fig_1, use_container_width=True)

    fig_2.update_layout(width=None, height=None, margin=dict(l=0, r=0, t=30, b=0))
    # Mostrar la gráfica de Plotly en la aplicación Streamlit
    st.plotly_chart(fig_2, use_container_width=True)

    fig_3.update_layout(width=None, height=None, margin=dict(l=0, r=0, t=30, b=0))
    # Mostrar la gráfica de Plotly en la aplicación Streamlit
    st.plotly_chart(fig_3, use_container_width=True)

    fig_4.update_layout(width=None, height=None, margin=dict(l=0, r=0, t=30, b=0))
    # Mostrar la gráfica de Plotly en la aplicación Streamlit
    st.plotly_chart(fig_4, use_container_width=True)

    fig_5.update_layout(width=None, height=None, margin=dict(l=0, r=0, t=30, b=0))
    # Mostrar la gráfica de Plotly en la aplicación Streamlit
    st.plotly_chart(fig_5, use_container_width=True)








