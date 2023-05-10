import pandas as pd
import tweepy
from keys2 import *
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_twitter_auth():
    """
    @return:
        - La autenticacion de Twitter
    """
    try:
        consumerKey = consumer_key
        consumerSecret = consumer_secret
        accessToken= access_token
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

def get_dataframe(query):
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
                              tweet_mode = "extended",
                              lang='es',
                              #result_type= 'popular',
                              count=100).pages(100):
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
    df = df.drop_duplicates( "text" , keep='first')

    return df

def saveData(dataframe):
    """
    :param dataframe:
    :return: Un archivo csv
    """
    return dataframe.to_csv('data.csv')

# Definimos una función para clasificar el sentimiento
def classify_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    if sia.polarity_scores(text)['compound'] < -0.1:
        return 0  # Negativo
    elif sia.polarity_scores(text)['compound'] > 0.1:
        return 2  # Positivo
    else:
        return 1  # Neutro


def main():
    query = '"Gobierno" -filter:retweets'
    dataframe = get_dataframe(query)
    dataframe['sentimiento'] = dataframe['text'].apply(lambda x: classify_sentiment(x))
    saveData(dataframe)


if __name__ == "__main__":
    main()