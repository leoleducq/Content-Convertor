import asyncio
import json
import os

from tweetcapture import *

from __init__ import cc

class contentconvertor :

    def __init__(self, BEARER_TOKEN : str, CONSUMER_KEY : str, CONSUMER_SECRET : str, ACCESS_TOKEN : str, ACCESS_TOKEN_SECRET : str, user : str, nb_tweets : int) :
        api = cc.connexion_to_api(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.user, self.tweets = cc.get_tweets(api ,user, nb_tweets)
        self.main()

    def main(self) :
        """Fonction principale"""
        list_link = []
        # Récupère les tweets de l'utilisateur
        user = self.user
        tweets = self.tweets
        #Récupère les liens des tweets
        for tweet in tweets:
            id = tweet.id
            list_link.append(f"https://twitter.com/{user}/status/{id}?s=20&t=wCS7mk5sE7QbkY3rE3hq3Q")
        i=1
        for link in list_link:
            asyncio.run(TweetCapture().screenshot(link, f"{i}.png", mode=0, night_mode=2))
            i+=1
        #Liste des images précedemment téléchargées
        list_img = [f for f in os.listdir('.') if f.endswith('.png')]
        for path in list_img :
            fit_image, offset, img, path = cc.resizing(path)
            # On colle l'image sur le fond noir
            fit_image.paste(img, offset)
            # On sauvegarde l'image
            fit_image.save(path, quality=100)

if __name__ == "__main__":
    # Récupère les crédentials dans le fichier credentials.json
    with open("../credentials.json", "r") as f:
        credentials = json.load(f)
    BEARER_TOKEN = credentials["BEARER_TOKEN"]
    CONSUMER_KEY = credentials["CONSUMER_KEY"]
    CONSUMER_SECRET = credentials["CONSUMER_SECRET"]
    ACCESS_TOKEN = credentials["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = credentials["ACCESS_TOKEN_SECRET"]
    contentconvertor(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, input("User : "), input("Nombre de tweets : "))