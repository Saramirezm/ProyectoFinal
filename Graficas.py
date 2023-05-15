from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ast
import streamlit as st
df = pd.read_csv('data.csv', encoding='utf-8')

df['text_clean'] = df['text_clean'].apply(lambda x: ast.literal_eval(x))
df['hashtag'] = df['hashtag'].apply(lambda x: ast.literal_eval(x))
df['menciones'] = df['menciones'].apply(lambda x: ast.literal_eval(x))


def plot_tokens():
    # lista de tokens
    token_list = np.concatenate(df['text_clean'].values)
    # frecuencia
    frecuencias_token = Counter(token_list)
    # top y separar palabra - frecuencia
    top_palabras = frecuencias_token.most_common(10)  # las palabras más frecuentes
    tokens, frec_tokens = zip(*top_palabras)
    # Grafica el histograma
    plt.barh(list(reversed(tokens)), list(reversed(frec_tokens)))
    plt.ylabel('Palabras')
    plt.xlabel('Frecuencia')
    plt.title('Palabras más frecuentes en la búsqueda')
    plt.tight_layout()  # Ajusta automáticamente los espacios en blanco
    plt.show()


def plot_hashtag():
    hashtag_list = np.concatenate(df['hashtag'].values)
    # frecuencia
    frec_hashtag = Counter(hashtag_list)
    # top y separar palabra - frecuencia
    top_hashtag = frec_hashtag.most_common(10)  # las palabras más frecuentes
    hashtag, frec_hashtag = zip(*top_hashtag)
    # Grafica el histograma
    plt.barh(list(reversed(hashtag)), list(reversed(frec_hashtag)))
    plt.ylabel('Hashtag')
    plt.xlabel('Frecuencia')
    plt.title('hashtags más frecuentes en la búsqueda')
    plt.tight_layout()  # Ajusta automáticamente los espacios en blanco
    plt.show()


def plot_menciones():
    menciones_list = np.concatenate(df['menciones'].values)
    # frecuencia
    frec_menciones = Counter(menciones_list)
    # top y separar palabra - frecuencia
    top_menciones = frec_menciones.most_common(10)  # las palabras más frecuentes
    menciones, frec_menciones = zip(*top_menciones)
    # Grafica el histograma
    plt.barh(list(reversed(menciones)), list(reversed(frec_menciones)))
    plt.ylabel('Menciones')
    plt.xlabel('Frecuencia')
    plt.title('Menciones más frecuentes en la búsqueda')
    plt.tight_layout()  # Ajusta automáticamente los espacios en blanco
    plt.show()


def plot_fechas():
    fechas = df['fecha'].values
    # Convertir la lista de fechas en un objeto pandas.Series y establecer la columna de fechas como el índice
    fechas_series = pd.Series(pd.to_datetime(fechas)).rename('Fechas').sort_values()
    fechas_series.index = fechas_series
    # Agrupar los datos por hora y contar las frecuencias de cada hora
    frecuencias_por_hora = fechas_series.resample('H').count()
    # Graficar la tabla de frecuencias por hora
    frecuencias_por_hora.plot()
    # Configurar las etiquetas del eje x y y y el título del gráfico
    plt.xlabel('Hora')
    plt.ylabel('Frecuencia')
    plt.title('Frecuencia por hora')
    # Mostrar el gráfico
    plt.show()


def plot_sentimientos():
    # Cuenta el número de tweets en cada categoría de sentimiento
    num_tweets = df['sentimiento'].value_counts()
    # Crea la gráfica de torta
    plt.pie(num_tweets, labels=num_tweets.index, autopct='%1.1f%%')
    # Añade título a la gráfica
    plt.title('Distribución de sentimientos en los tweets')
    # Muestra la gráfica
    plt.show()


def plot_todas():
    plot_sentimientos()
    plot_tokens()
    plot_hashtag()
    plot_menciones()
    plot_fechas()

if __name__ == "__main__":
    plot_todas()
