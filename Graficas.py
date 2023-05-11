import re
from collections import Counter
import numpy as np
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
from unidecode import unidecode


df = pd.read_csv('data.csv', encoding='latin-1')
# print(df.head())


def limpiar_tokenizar(texto):
    """
    Esta función limpia y tokeniza el texto en palabras individuales.
    El orden en el que se va limpiando el texto no es arbitrario.
    El listado de signos de puntuación se ha obtenido de: print(string.punctuation)
    y re.escape(string.punctuation)
    """
    # Se convierte todo el texto a minúsculas
    nuevo_texto = texto.lower()
    # Eliminación de articulos y  (palabras que empiezan por "http")
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    # Eliminación de páginas web (palabras que empiezan por "http")
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    # Eliminación de signos de puntuación
    regex = '[\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~\n]'
    nuevo_texto = re.sub(regex, ' ', nuevo_texto)
    # Tokenización por palabras individuales
    nuevo_texto = nuevo_texto.split(sep=' ')
    # Eliminación de tokens con una longitud < 3
    nuevo_texto = [token for token in nuevo_texto if len(token) > 3]
    # Eliminación de stopwords en español
    stop_words = set(stopwords.words('spanish'))
    nuevo_texto = [word for word in nuevo_texto if not word in stop_words]
    return nuevo_texto

def buscar_hashtag(texto):
    # Se convierte el texto a minúsculas
    nuevo_texto = texto.lower()
    # Quitar las tildes, etc.
    nuevo_texto = unidecode(nuevo_texto)
    # Solo hashtags
    hashtags = re.findall(r'(?<=#)\w+', nuevo_texto)
    hashtags = ['#'+ word for word in hashtags]
    return hashtags

def buscar_mencion(texto):
    # Se convierte el texto a minúsculas
    nuevo_texto = texto.lower()
    # Quitar las tildes, etc.
    nuevo_texto = unidecode(nuevo_texto)
    # Solo menciones
    menciones = re.findall(r'(?<=@)\w+', nuevo_texto)
    menciones = ['@' + word for word in menciones]
    return menciones

def conver_date(fecha_str):
    # Convertir la fecha y hora original a un objeto datetime de Python
    fecha_utc = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S%z')

    # Eliminar la información sobre la zona horaria del objeto datetime original
    fecha_naive = fecha_utc.replace(tzinfo=None)

    # Obtener los objetos timezone para las zonas horarias original y de destino
    tz_original = pytz.timezone('UTC')
    tz_nueva = pytz.timezone('America/Bogota')

    # Convertir la fecha y hora del objeto datetime original a la nueva zona horaria
    fecha_nueva = tz_original.localize(fecha_naive).astimezone(tz_nueva)

    # Dar formato a la fecha y hora en la nueva zona horaria
    fecha_nueva_str = fecha_nueva.strftime('%Y-%m-%d %H:%M:%S')

    return fecha_nueva_str

df['fecha'] = df['date'].apply(lambda x: conver_date(x))

# Limpieza de texto
df['text_clean'] = df['text'].apply(lambda x: limpiar_tokenizar(x))
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
plt.tight_layout() # Ajusta automáticamente los espacios en blanco
plt.show()

# buscar hashtag
df['hashtag'] = df['text'].apply(lambda x: buscar_hashtag(x))
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
plt.tight_layout() # Ajusta automáticamente los espacios en blanco
plt.show()

# buscar menciones
df['menciones'] = df['text'].apply(lambda x: buscar_mencion(x))
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
plt.tight_layout() # Ajusta automáticamente los espacios en blanco
plt.show()

#############################
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

tod_date = frecuencias_por_hora.nlargest(10)
print(tod_date)

############################

# Grafica de sentiemientos
# ===============================================================================
# Cuenta el número de tweets en cada categoría de sentimiento
num_tweets = df['sentimiento'].value_counts()
# Crea la gráfica de torta
plt.pie(num_tweets, labels=num_tweets.index, autopct='%1.1f%%')
# Añade título a la gráfica
plt.title('Distribución de sentimientos en los tweets')
# Muestra la gráfica
plt.show()