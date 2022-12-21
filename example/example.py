import json

from contentconvertor import tweet2gram as t2g
# Récupère les crédentials dans le fichier credentials.json
with open("credentials.json", "r") as f :
    credentials = json.load(f)
BEARER_TOKEN = credentials["BEARER_TOKEN"]
# Récupère la connexion à l'API
api = t2g.connexion_to_api(BEARER_TOKEN)
# Récupère l'id de l'utilisateur
user_id = t2g.get_user_id(api, "iziatask")
# Récupère les tweets de l'utilisateur
tweets = t2g.get_tweets(api, user_id, exclude=["replies", "retweets"])
for tweet in tweets.data :
    # Télécharge les tweets
    t2g.download_tweet(user_id, tweet)