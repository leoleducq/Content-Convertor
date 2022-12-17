import json
import os

import contentconvertor.contentconvertor as cc


class contentconvertor :

    def __init__(self, BEARER_TOKEN : str, CONSUMER_KEY : str, CONSUMER_SECRET : str, ACCESS_TOKEN : str, ACCESS_TOKEN_SECRET : str, user : str, nb_tweets : int) :
        api = cc.connexion_to_api(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.tweets = cc.get_tweets(api ,user, nb_tweets=nb_tweets)
        self.user = user
        self.main()

    def main(self) :
        """Fonction principale"""
        # Récupère les tweets de l'utilisateur
        user = self.user
        tweets = self.tweets
        # Télécharge les tweets
        cc.download_tweets(user, tweets)
        #Liste des images précedemment téléchargées
        list_img = [f for f in os.listdir('.') if f.endswith('.png')]
        for path in list_img :
            img = cc.get_image(path)
            cc.resizing(img, path)

if __name__ == "__main__":
    # Récupère les crédentials dans le fichier credentials.json
    with open("credentials.json", "r") as f :
        credentials = json.load(f)
    BEARER_TOKEN = credentials["BEARER_TOKEN"]
    CONSUMER_KEY = credentials["CONSUMER_KEY"]
    CONSUMER_SECRET = credentials["CONSUMER_SECRET"]
    ACCESS_TOKEN = credentials["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = credentials["ACCESS_TOKEN_SECRET"]
    contentconvertor(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, input("User : "), input("Nombre de tweets : "))