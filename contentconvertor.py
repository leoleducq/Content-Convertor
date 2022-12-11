import asyncio
from typing import Tuple

import tweepy
from PIL import Image
from tweetcapture import TweetCapture


def connexion_to_api(BEARER_TOKEN : str, CONSUMER_KEY : str, CONSUMER_SECRET : str, ACCESS_TOKEN : str, ACCESS_TOKEN_SECRET : str) -> tweepy.API :
    """Connexion à l'API de tweepy
    :param: BEARER_TOKEN: Token d'authentification
    :param: CONSUMER_KEY: Clé d'authentification
    :param: CONSUMER_SECRET: Clé secret d'authentification
    :param: ACCESS_TOKEN: Token d'accès
    :param: ACCESS_TOKEN_SECRET: Token d'accès secret
    :return: Retourne l'API de tweepy"""
    client = tweepy.Client(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def get_tweets(api : tweepy.API, user : str, nb_tweets : int) -> Tuple[str, list] :
    """Récupère les tweets de l'utilisateur donné en paramètre
    :param: api: API de tweepy
    :param: user: Utilisateur dont on souhaite récupérer les tweets
    :param: nb_tweets: Nombre de tweets à récupérer
    :return: Retourne le nom de l'utilisateur et la liste des tweets"""
    #Récupère les tweets (tweet_mode=extended récupère tout le tweet (bloqué à 140 car. sinon))
    tweets = api.user_timeline(screen_name=user, count=nb_tweets, include_rts=False, exclude_replies=True, tweet_mode="extended")
    return user, tweets

def download_tweets(user, tweets : list) -> None :
    """Télécharge les tweets
    :param: user: Utilisateur dont on souhaite récupérer les tweets
    :param: tweets: Liste des tweets
    :return: None"""
    i = 1
    list_link = []
    for tweet in tweets:
        id = tweet.id
        list_link.append(f"https://twitter.com/{user}/status/{id}?s=20&t=wCS7mk5sE7QbkY3rE3hq3Q")
    i=1
    for link in list_link:
        asyncio.run(TweetCapture().screenshot(link, f"{i}.png", mode=0, night_mode=2))
        i+=1

def get_image(path : str) -> Image :
    """Récupère l'image dans le path donné en paramètre
    :param: img: Chemin de l'image
    :return: Retourne l'objet Image"""
    img = Image.open(path)
    return img

def resizing(img : Image, path : str) -> Tuple[Image, Tuple[int, int], Image] :
    """Redimensionne l'image pour qu'elle soit carrée
    :param img: Image à redimensionner
    :param path: Chemin de l'image
    :return: None"""
    # Dimensions de l'image
    width, height = img.size
    # Valeur max entre les deux
    dimension = max(width, height)
    # Nouvelles dimensions de l'image
    size = dimension, dimension
    # Fond noir
    background_color = (0, 0, 0)
    # Créer une nouvelle image avec le fond noir
    fit_image = Image.new('RGB', size, background_color)
    # Récupère les dimensions du fond noir
    background_width, background_height = fit_image.size
    # Petit calcul pour dire de bien centrer l'image sur le fond noir
    offset = ((background_width - width) // 2, (background_height - height) // 2)
    # Colle l'image sur le fond noir
    fit_image.paste(img, offset)
    # On colle l'image sur le fond noir
    fit_image.paste(img, offset)
    # On sauvegarde l'image
    fit_image.save(path, quality=100)