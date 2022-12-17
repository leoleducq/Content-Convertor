import json
import os

import contentconvertor.contentconvertor as cc

# Récupère les crédentials dans le fichier credentials.json
with open("credentials.json", "r") as f :
    credentials = json.load(f)
BEARER_TOKEN = credentials["BEARER_TOKEN"]

# Récupère la connexion à l'API
api = cc.connexion_to_api(BEARER_TOKEN)
# Récupère l'id de l'utilisateur
user_id = cc.get_user_id(api, "iziatask")
# Récupère les tweets de l'utilisateur
tweets = cc.get_tweets(api, user_id, exclude=["replies", "retweets"])
# Télécharge les tweets
cc.download_tweets(user_id, tweets)
#Liste des images précedemment téléchargées
list_img = [f for f in os.listdir('.') if f.endswith('.png')]
for path in list_img :
    # Récupère l'image
    img = cc.get_image(path)
    # Redimensionne l'image
    cc.resizing(img, path)