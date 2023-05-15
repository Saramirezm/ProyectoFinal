import pandas as pd
import tweepy
from nltk.corpus import stopwords
from keys2 import *
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from unidecode import unidecode
import pytz
import re


def get_twitter_auth():
    """
    @return:
        - La autenticacion de Twitter
    """
    try:
        consumerKey = consumer_key
        consumerSecret = consumer_secret
        accessToken = access_token
        accessTokenSecret = access_token_secret

    except KeyError:
        sys.stderr.write("Twitter Environment Variable not Set\n")
        sys.exit(1)

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    return auth


def get_twitter_client():
    """
    @return:
        - El cliente para acceder a la autenticacion de la API
    """
    auth = get_twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client


def get_dataframe(query, count=100, pages=100):
    """
    @params:
        - query: Las palabras claves de busqueda
    @return
        - un dataframe con los tweets
    """
    client = get_twitter_client()

    all_tweets = []

    for page in tweepy.Cursor(client.search_tweets,
                              q=query,
                              tweet_mode="extended",
                              lang='es',
                              # result_type= 'popular',
                              count=count).pages(pages):
        for tweet in page:
            parsed_tweet = {}
            parsed_tweet['date'] = tweet.created_at
            parsed_tweet['author'] = tweet.user.name
            parsed_tweet['twitter_name'] = tweet.user.screen_name
            parsed_tweet['text'] = tweet.full_text
            parsed_tweet['number_of_likes'] = tweet.favorite_count
            parsed_tweet['number_of_retweets'] = tweet.retweet_count

            all_tweets.append(parsed_tweet)

    # Creamos el dataframe
    df = pd.DataFrame(all_tweets)

    # Eliminamos duplicados
    df = df.drop_duplicates("text", keep='first')

    return df


# Definimos una función para clasificar el sentimiento
def classify_sentiment(text):
    nuevo_texto = text.lower()
    nuevo_texto = unidecode(nuevo_texto)
    sia = SentimentIntensityAnalyzer()
    if sia.polarity_scores(nuevo_texto)['compound'] < -0.1:
        return 0  # Negativo
    elif sia.polarity_scores(nuevo_texto)['compound'] > 0.1:
        return 2  # Positivo
    else:
        return 1  # Neutro


def limpiar_tokenizar(texto):
    """
    Esta función limpia y tokeniza el texto en palabras individuales.
    El orden en el que se va limpiando el texto no es arbitrario.
    El listado de signos de puntuación se ha obtenido de: print(string.punctuation)
    y re.escape(string.punctuation)
    """
    # Se convierte el texto a minúsculas
    nuevo_texto = texto.lower()
    # Eliminación de articulos y  (palabras que empiezan por "http")
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    # Eliminación de páginas web (palabras que empiezan por "http")
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    # Quitar las tildes, etc.
    nuevo_texto = unidecode(nuevo_texto)
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
    hashtags = ['#' + word for word in hashtags]
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
    # fecha_utc = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S%z')

    # Eliminar la información sobre la zona horaria del objeto datetime original
    fecha_naive = fecha_str.replace(tzinfo=None)

    # Obtener los objetos timezone para las zonas horarias original y de destino
    tz_original = pytz.timezone('UTC')
    tz_nueva = pytz.timezone('America/Bogota')

    # Convertir la fecha y hora del objeto datetime original a la nueva zona horaria
    fecha_nueva = tz_original.localize(fecha_naive).astimezone(tz_nueva)

    # Dar formato a la fecha y hora en la nueva zona horaria
    fecha_nueva_str = fecha_nueva.strftime('%Y-%m-%d %H:%M:%S')

    return fecha_nueva_str


def saveData(dataframe):
    """
    :param dataframe:
    :return: Un archivo csv
    """
    return dataframe.to_csv('data.csv')


def CrearDatset(busqueda, count=10, pages=100):
    query = str(busqueda) + '-filter:retweets'
    dataframe = get_dataframe(query, count=count, pages=pages)
    dataframe['sentimiento'] = dataframe['text'].apply(lambda x: classify_sentiment(x))
    dataframe['fecha'] = dataframe['date'].apply(lambda x: conver_date(x))
    # Limpieza de texto
    dataframe['text_clean'] = dataframe['text'].apply(lambda x: limpiar_tokenizar(x))
    dataframe['hashtag'] = dataframe['text'].apply(lambda x: buscar_hashtag(x))
    dataframe['menciones'] = dataframe['text'].apply(lambda x: buscar_mencion(x))
    dataframe = dataframe[
        ['fecha', 'text', 'text_clean', 'hashtag', 'menciones', 'number_of_likes', 'number_of_retweets', 'sentimiento']]
    saveData(dataframe)


if __name__ == '__main__':
    CrearDatset("OpenAI")
