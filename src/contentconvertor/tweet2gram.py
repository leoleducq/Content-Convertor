import asyncio
from typing import Tuple

import tweepy
from PIL import Image
from tweetcapture import TweetCapture


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

def get_tweets(api : tweepy.API, user_id : str, nb_tweets : int = None, exclude : str = None) -> list :
    """Récupère les tweets de l'utilisateur donné en paramètre
    :param: api: API de tweepy
    :param: user_id: l'ID de l'utilisateur dont on souhaite récupérer les tweets
    :param: nb_tweets: Nombre de tweets à récupérer, par défaut 5
    :param: exclude: Exclure les tweets de type replies ou retweets, par défaut "" (aucun)
    :return: Retourne la liste des tweets"""
    if nb_tweets == None :
        nb_tweets = 5
    if exclude == None :
        return api.get_users_tweets(id=user_id, max_results=nb_tweets)
    else :
        return api.get_users_tweets(id=user_id, max_results=nb_tweets, exclude=exclude)

def download_tweet(user : str, tweet : str = None, path : str = None, name : str = None, mode : int = None, night_mode : int = None, link : str = None) -> None :
    """Télécharge les tweets
    :param: user: Utilisateur dont on souhaite télécharger le tweet
    :param: tweet: Tweet à télécharger
    :param: path: Chemin où enregistrer le tweet
    :param: name: Nom du fichier
    :param: mode: Mode de capture, 0 = capture normale, 1 = capture en mode nuit, 2 = capture en mode jour
    :param: night_mode: Mode de capture en mode nuit, 0 = capture en mode nuit, 1 = capture en mode jour
    :param: link: Lien du tweet
    :return: None"""
    if path == None :
        path = ""
    if name == None :
        name = "tweet"
    if mode == None :
        mode = 0
    if night_mode == None :
        night_mode = 2
    if link == None :
        tweet_id = tweet.id
        link = f"https://twitter.com/{user}/status/{tweet_id}"
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