import asyncio
import json
import os
from typing import Tuple

import tweepy
from PIL import Image
from tweetcapture import *


class GetTweets :

    def __init__(self, BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, user, nb_tweets) -> tweepy.API :
        """Récupère les tokens d'authentification et les crédentials, le nom de l'utilisateur et le nombre de tweets à récupérer
        :param BEARER_TOKEN: Token d'authentification
        :param CONSUMER_KEY: Token d'authentification
        :param CONSUMER_SECRET: Token
        :param ACCESS_TOKEN: Token
        :param ACCESS_TOKEN_SECRET: Token
        :param user: Utilisateur dont on souhaite récupérer les tweets
        :param nb_tweets: Nombre de tweets à récupérer"""
        self.client = tweepy.Client(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.user = user
        self.nb_tweets = nb_tweets
        self.main()

    def get_tweets(self) -> Tuple[str, list] :
        """Récupère les tweets de l'utilisateur donné en paramètre
        :return: Retourne le nom de l'utilisateur et la liste des tweets"""
        #L'utilisateur dont on souhaite récupérer les tweets
        user = self.user
        #Le nombre de tweets
        limit = self.nb_tweets
        #Récupère les tweets (tweet_mode=extended récupère tout le tweet (bloqué à 140 car. sinon))
        tweets = self.api.user_timeline(screen_name=user, count=limit, include_rts=False, exclude_replies=True, tweet_mode="extended")
        return user, tweets

    #Do the resizing
    def resizing(self,path) -> Tuple[Tuple[int, int], str] :
        """Redimensionne l'image pour qu'elle soit carrée
        :param path: Chemin de l'image
        :return: Retourne l'image redimensionnée, les dimensions de l'image, l'image et le chemin de l'image"""
        img = self.get_image(path)
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
        return fit_image, offset, img, path

    #Get the image
    def get_image(self, img) -> Image :
        """Récupère l'image dans le path donné en paramètre"""
        img = Image.open(img)
        return img

    def main(self) :
        """Fonction principale"""
        tweetcapture = TweetCapture()
        list_link = []
        user, tweets = self.get_tweets()
        for tweet in tweets:
            id = tweet.id
            list_link.append(f"https://twitter.com/{user}/status/{id}?s=20&t=wCS7mk5sE7QbkY3rE3hq3Q")
        i=1
        for link in list_link:
            asyncio.run(tweetcapture.screenshot(link, f"{i}.png", mode=0, night_mode=2))
            i+=1
        #Liste des images précedemment téléchargées
        list_img = [f for f in os.listdir('.') if f.endswith('.png')]
        for path in list_img :
            fit_image, offset, img, path = self.resizing(path)
            # On colle l'image sur le fond noir
            fit_image.paste(img, offset)
            # On sauvegarde l'image
            fit_image.save(path, quality=100)

if __name__ == "__main__":
    # Récupère les crédentials dans le fichier credentials.json
    with open("credentials.json", "r") as f:
        credentials = json.load(f)
    BEARER_TOKEN = credentials["BEARER_TOKEN"]
    CONSUMER_KEY = credentials["CONSUMER_KEY"]
    CONSUMER_SECRET = credentials["CONSUMER_SECRET"]
    ACCESS_TOKEN = credentials["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = credentials["ACCESS_TOKEN_SECRET"]
    GetTweets(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, input("User : "), input("Nombre de tweets : "))