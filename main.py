import asyncio
import json
import os
import time
from typing import Tuple

import tweepy
from PIL import Images
from tweetcapture import *


class GetTweets :
    def __init__(self) :
        self.main()
    #Connexion à l'API
    def connexion(self, BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) -> tweepy.API :
        client = tweepy.Client(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        return api

    def get_tweets(self, user) -> Tuple[str, list] :
        api = self.connexion()
        #L'utilisateur dont on souhaite récupérer les tweets
        user = user
        #Le nombre de tweets
        limit = 1
        #Récupère les tweets (tweet_mode=extended récupère tout le tweet (bloqué à 140 car. sinon))
        tweets = api.user_timeline(screen_name=user, count=limit, include_rts=False, exclude_replies=True, tweet_mode="extended")
        return user, tweets

    def main(self):
        tweetcapture = TweetCapture()
        # list_link = ["https://twitter.com/iziatask/status/1577667448639102977?s=20&t=wCS7mk5sE7QbkY3rE3hq3Q","https://twitter.com/iziatask/status/1577637237981818880?s=20&t=wCS7mk5sE7QbkY3rE3hq3Q"]
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
        self.resizing(list_img)

    #Do the resizing
    def resizing(self,list_img):
        for path in list_img:
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
            # On colle l'image sur le fond noir
            fit_image.paste(img, offset)
            # On sauvegarde l'image
            fit_image.save(path, quality=100)

    #Get the image
    def get_image(self, img) -> Image :
        """Récupère l'image dans le path donné en paramètre"""
        img = Image.open(img)
        return img

if __name__ == "__main__":
    # Récupère les crédentials dans le fichier credentials.json
    with open("credentials.json", "r") as f:
        credentials = json.load(f)
    BEARER_TOKEN = credentials["BEARER_TOKEN"]
    CONSUMER_KEY = credentials["CONSUMER_KEY"]
    CONSUMER_SECRET = credentials["CONSUMER_SECRET"]
    ACCESS_TOKEN = credentials["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = credentials["ACCESS_TOKEN_SECRET"]
    GetTweets(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)