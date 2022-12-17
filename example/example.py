import json

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
for tweet in tweets.data :
    # Télécharge les tweets
    cc.download_tweet(user_id, tweet)