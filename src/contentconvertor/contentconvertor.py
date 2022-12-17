import asyncio

import tweepy
from PIL import Image
from tweetcapture import TweetCapture
from typing import Tuple

def connexion_to_api(BEARER_TOKEN : str) -> tweepy.API :
    """Connexion à l'API de tweepy
    :param: CONSUMER_KEY: Clé d'authentification
    :param: CONSUMER_SECRET: Clé secret d'authentification
    :param: ACCESS_TOKEN: Token d'accès
    :param: ACCESS_TOKEN_SECRET: Token d'accès secret
    :return: Retourne l'API de tweepy"""
    return tweepy.Client(bearer_token=BEARER_TOKEN)

def get_user_id(api : tweepy.API, user : str) -> Tuple[str, str] :
    """Récupère l'ID de l'utilisateur
    :param: api: API de tweepy
    :param: user: Nom de l'utilisateur
    :return: Retourne l'ID de l'utilisateur"""
    user = api.get_user(username=user)
    return user.data.id

def get_tweets(api : tweepy.API, user_id : str, *args, **kwargs) -> list :
    """Récupère les tweets de l'utilisateur donné en paramètre
    :param: api: API de tweepy
    :param: user_id: l'ID de l'utilisateur dont on souhaite récupérer les tweets
    :kwargs: nb_tweets: Nombre de tweets à récupérer, par défaut 5
    :kwargs: exclude: Exclure les tweets de type "replies" et/ou "retweets", par défaut ""
    :return: Retourne la liste des tweets"""
    nb_tweets = 5
    exclude = ""
    for key, value in kwargs.items() :
        if key == "nb_tweets" :
            nb_tweets = value
        elif key == "exclude" :
            exclude = value
    if exclude == "" :
        tweets = api.get_users_tweets(id=user_id, max_results=nb_tweets)
    else :
        tweets = api.get_users_tweets(id=user_id, max_results=nb_tweets, exclude=exclude)
    return tweets

def download_tweets(user, tweets : list, *args, **kwargs) -> None :
    """Télécharge les tweets
    :param: user: Utilisateur dont on souhaite récupérer les tweets
    :param: tweets: Liste des tweets
    :kwargs: path: Chemin où sauvegarder les images, par défaut [""]
    :kwargs: mode: Mode de capture d'écran, par défaut 0
    :kwargs: night_mode: Mode nuit, par défaut 0
    :return: None"""
    path = ""
    mode = 0
    night_mode = 2
    # Récupère les arguments
    for key, value in kwargs.items() :
        if key == "path" :
            path = value
        elif key == "mode" :
            mode = value
        elif key == "night_mode" :
            night_mode = value
    i = 1
    list_link = []
    for tweet in tweets.data :
        id = tweet.id
        list_link.append(f"https://twitter.com/{user}/status/{id}?s=20&t=wCS7mk5sE7QbkY3rE3hq3Q")
    i=1
    for link in list_link :
        asyncio.run(TweetCapture().screenshot(link, f"{path}{i}.png", mode=mode, night_mode=night_mode))
        i+=1

def get_image(path : str) -> Image :
    """Récupère l'image dans le path donné en paramètre
    :param: img: Chemin de l'image
    :return: Retourne l'objet Image"""
    return Image.open(path)

def resizing(img : Image, path : str) -> None :
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