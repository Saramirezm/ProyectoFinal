# Tratamiento de datos
# ==============================================================================
import re
from collections import Counter

# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from unidecode import unidecode
import string

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
    regex = '[\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    nuevo_texto = re.sub(regex, ' ', nuevo_texto)
    # Tokenización por palabras individuales
    nuevo_texto = nuevo_texto.split(sep=' ')
    # Eliminación de tokens con una longitud < 3
    nuevo_texto = [token for token in nuevo_texto if len(token) > 3]
    # Eliminación de stopwords en español
    stop_words = set(stopwords.words('spanish'))
    nuevo_texto = [word for word in nuevo_texto if not word in stop_words]
    #Eliminar la ñ
    nuevo_texto = [unidecode(token) for token in nuevo_texto]
    return nuevo_texto



# Limpieza de cada texto

df['text_clean'] = df['text'].apply(lambda x: limpiar_tokenizar(x))
# print(sampled[['coment', 'coment_clean']].head())

# Unnest de la columna texto_tokenizado

tweets_tidy = df.explode(column='text_clean')
tweets_tidy = tweets_tidy.drop(columns='text')
tweets_tidy = tweets_tidy.rename(columns={'text_clean': 'token'})
tweets_tidy = tweets_tidy['token']

frecuencias = Counter(tweets_tidy)

# Obtén las palabras más frecuentes y sus frecuencias
top_palabras = frecuencias.most_common(5)  # las 5 palabras más frecuentes

# Separa las palabras y sus frecuencias en dos listas diferentes
palabras_grafica = [palabra[0] for palabra in top_palabras]
frecuencias_grafica = [palabra[1] for palabra in top_palabras]

# Grafica el histograma
plt.bar(palabras_grafica, frecuencias_grafica)
plt.xlabel('Palabras')
plt.ylabel('Frecuencia')
plt.title('Las 5 palabras más frecuentes en el dataset de tweets')
print(top_palabras)
plt.show()

palabras = []
for tweet in tweets_tidy:
    palabras.extend(tweet.split())

# Calcula la frecuencia de cada palabra
frecuencia = FreqDist(palabras)

# Grafica el histograma de las 20 palabras más frecuentes
frecuencia.plot(10, cumulative=False)
plt.show()

# Distribución temporal de los tweets
# ==============================================================================
# Los tweets los extrae a la hora que se hace la busqueda, entonces no revela informacion

# Grafica de sentiemientos
#===============================================================================
# Cuenta el número de tweets en cada categoría de sentimiento
num_tweets = df['sentimiento'].value_counts()

# Crea la gráfica de torta
plt.pie(num_tweets, labels=num_tweets.index, autopct='%1.1f%%')

# Añade título a la gráfica
plt.title('Distribución de sentimientos en los tweets')

# Muestra la gráfica
plt.show()