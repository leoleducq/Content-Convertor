import asyncio

import tweepy
from PIL import Image
from tweetcapture import TweetCapture
from typing import Tuple

def connexion_to_api(BEARER_TOKEN : str) -> tweepy.API :
    """Connexion à l'API de tweepy
    :param: BEARER_TOKEN: Token d'accès à l'API
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
        return api.get_users_tweets(id=user_id, max_results=nb_tweets)
    else :
        return api.get_users_tweets(id=user_id, max_results=nb_tweets, exclude=exclude)

def download_tweet(user, tweet : str, *args, **kwargs) -> None :
    """Télécharge les tweets
    :param: user: Utilisateur dont on souhaite télécharger le tweet
    :param: tweet: Tweet à télécharger
    :kwargs: path: Chemin où sauvegarder les images, par défaut ""
    :kwargs: name: Nom du fichier, par défaut "tweet"
    :kwargs: mode: Mode de capture d'écran, par défaut 0
    :kwargs: night_mode: Mode nuit, par défaut 0
    :return: None"""
    path = ""
    name = "tweet"
    mode = 0
    night_mode = 2
    # Récupère les arguments
    for key, value in kwargs.items() :
        if key == "path" :
            path = value
        elif key == "name" :
            name = value
        elif key == "mode" :
            mode = value
        elif key == "night_mode" :
            night_mode = value
    id = tweet.id
    link = f"https://twitter.com/{user}/status/{id}?s=20&t=wCS7mk5sE7QbkY3rE3hq3Q"
    path = f"{path}{name}.png"
    asyncio.run(TweetCapture().screenshot(link, path, mode=mode, night_mode=night_mode))
    img = Image.open(path)
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