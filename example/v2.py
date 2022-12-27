import asyncio
import json
from typing import Tuple

import requests
import tweepy
from PIL import Image, ImageDraw, ImageFont, ImageColor
from tweetcapture import TweetCapture


def connexion_to_api_v2(BEARER_TOKEN : str) -> tweepy.API :
    """Connexion à l'API V2 de tweepy
    :param: BEARER_TOKEN: Token d'accès à l'API
    :return: Retourne l'API V2 de tweepy"""
    return tweepy.Client(bearer_token=BEARER_TOKEN)

def connexion_to_api_v1(CONSUMER_KEY : str, CONSUMER_SECRET : str, ACCESS_TOKEN : str, ACCESS_TOKEN_SECRET : str) -> tweepy.API :
    """Connexion à l'API V1 de tweepy
    :param: CONSUMER_KEY: Clé d'API
    :param: CONSUMER_SECRET: Clé secret
    :param: ACCESS_TOKEN: Token d'accès
    :param: ACCESS_TOKEN_SECRET: Token secret d'accès
    :return: Retourne l'API V1 de tweepy"""
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def get_user_id(apiv2 : tweepy.API, user : str) -> Tuple[str, str] :
    """Récupère l'ID de l'utilisateur
    :param: api: API de tweepy
    :param: user: Nom de l'utilisateur
    :return: Retourne l'ID de l'utilisateur"""
    user = apiv2.get_user(username=user)
    return user.data.id

def get_tweets(apiv2 : tweepy.API, user_id : str, *args, **kwargs) -> list :
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
        return apiv2.get_users_tweets(id=user_id, max_results=nb_tweets)
    else :
        return apiv2.get_users_tweets(id=user_id, max_results=nb_tweets, exclude=exclude)

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

def get_profile_picture_and_banner(api : tweepy.API, user : str) -> None :
    """Récupère la photo de profil de l'utilisateur
    :param: api: API de tweepy
    :param: user: Utilisateur dont on souhaite récupérer la photo de profil
    :return: None"""
    user = api.get_user(screen_name=user)
    photo_url = user.profile_image_url.replace("normal", "400x400")
    banner_url = user.profile_banner_url
    response = requests.get(photo_url)
    with open("photo.png", "wb") as f:
        f.write(response.content)
    response = requests.get(banner_url)
    with open("banner.png", "wb") as f:
        f.write(response.content)
    # Ouvrez la photo de profil
    photo = Image.open("photo.png")
    # Récupérez les dimensions de la photo de profil
    photo_width, photo_height = photo.size
    # La photo de profil doit être ronde, donc on prend la plus petite dimension
    photo_dimension = min(photo_width, photo_height)
    # On crée une nouvelle image avec les dimensions de la photo de profil
    photo = photo.resize((photo_dimension, photo_dimension))
    # On crée un cercle avec la photo de profil
    mask = Image.new("L", photo.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + photo.size, fill=255)
    mask = mask.resize(photo.size, Image.Resampling.LANCZOS)
    photo.putalpha(mask)
    # Sauvegarde la photo de profil
    photo.save("photo.png", quality=100)

def get_main_color(image : str) -> tuple :
    """Récupère la couleur principale de l'image
    :param: image: Image dont on souhaite récupérer la couleur principale
    :return: tuple: Couleur principale de l'image"""
    # Ouvre l'image
    image = Image.open(image)
    # Récupère les couleurs de l'image
    colors = image.getcolors(image.size[0] * image.size[1])
    # Trie les couleurs par ordre décroissant
    colors.sort(reverse=True)
    # Récupère la couleur principale
    main_color = colors[0][1]
    # Récupère la couleur secondaire
    second_color = colors[1][1]
    return main_color, second_color

def main() :
    # Récupère les crédentials dans le fichier credentials.json
    with open("credentials.json", "r") as f :
        credentials = json.load(f)
    BEARER_TOKEN = credentials["BEARER_TOKEN"]
    CONSUMER_KEY = credentials["CONSUMER_KEY"]
    CONSUMER_SECRET = credentials["CONSUMER_SECRET"]
    ACCESS_TOKEN = credentials["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = credentials["ACCESS_TOKEN_SECRET"]
    # Récupère la connexion à l'API
    # api = connexion_to_api(BEARER_TOKEN)
    # Récupère l'ID de l'utilisateur
    # Utilisez l'API pour récupérer les informations de l'utilisateur
    username = "iziatask"
    apiv1 = connexion_to_api_v1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    apiv2 = connexion_to_api_v2(BEARER_TOKEN)
    get_profile_picture_and_banner(apiv1, username)
    user_id = get_user_id(apiv2, username)
    tweets = get_tweets(apiv2, user_id, nb_tweets=5, exclude=["replies","retweets"])
    for tweet in tweets.data:
        print(tweet)
        # Récupère le texte du tweet
        tweet_text = tweet["text"]
        break
    # Récupère la couleur principale de la bannière
    main_color, second_color = get_main_color("banner.png")
    # Ouvre un objet Image de 1080 pixels par 1080 pixels et de la couleur principale de la bannière
    tweet_screenshot = Image.new("RGB", (1080, 1080), main_color)
    # Rajoute la photo de profil sur l'image en bas à gauche en petit (400x400)
    profil_picture = Image.open("photo.png")
    profil_picture = profil_picture.resize((100, 100))
    tweet_screenshot.paste(profil_picture, (0, 980))
    # Positionne le texte en bas au milieu avec la photo de profil à droite
    draw = ImageDraw.Draw(tweet_screenshot)
    # Police d'écriture avec une taille qui dépend de la longueur du texte
    font = ImageFont.truetype("comic.ttf", 50)
    # Position du texte
    text_position = (110, 1000)
    # Couleur du texte
    text_color = second_color
    # Ecrit le nom d'utilisateur
    draw.text(text_position, username, text_color, font=font)
    # Met le texte du tweet au milieu de l'image
    draw = ImageDraw.Draw(tweet_screenshot)
    # Police d'écriture
    font = ImageFont.truetype("arial.ttf", 50)
    # Position du texte
    text_position = (0, 0)
    # Couleur du texte
    text_color = second_color
    # Ecrit le texte du tweet
    draw.text(text_position, tweet_text, text_color, font=font)
    # Sauvegarde l'image
    tweet_screenshot.save("image.png", quality=100)

if __name__ == "__main__" :
    main()
    