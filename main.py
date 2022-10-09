from credentials import bearer_token, api_key, api_secret, access_token, access_token_secret
from tweetcapture import *
import asyncio
import os
from PIL import Image
import tweepy
import time
from credentials import *

# client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
# auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
# api = tweepy.API(auth)

# search_terms = ["python"]

# class MyStream(tweepy.StreamingClient):
#     def on_connect(self):
#         print("Connected to Twitter API.")
    
#     def on_tweet(self,tweet):
#         if tweet.referenced_tweets == None:
#             print(tweet.text)

#             time.sleep(0.2)

# stream = MyStream(bearer_token=bearer_token)

# for term in search_terms:
#     stream.add_rules(tweepy.StreamRule(term))

# stream.filter(tweet_fields=["referenced_tweets"])

#Connexion à l'API
def connexion():
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def get_tweets():
    api = connexion()
    #L'utilisateur dont on souhaite récupérer les tweets
    user = "iziatask"
    #Le nombre de tweets
    limit = 1
    #Récupère les tweets (tweet_mode=extended récupère tout le tweet (bloqué à 140 car. sinon))
    tweets = api.user_timeline(screen_name=user, count=limit, include_rts=False, exclude_replies=True, tweet_mode="extended")
    return user, tweets

def main():
    tweetcapture = TweetCapture()
    # list_link = ["https://twitter.com/iziatask/status/1577667448639102977?s=20&t=wCS7mk5sE7QbkY3rE3hq3Q","https://twitter.com/iziatask/status/1577637237981818880?s=20&t=wCS7mk5sE7QbkY3rE3hq3Q"]
    list_link = []
    user, tweets = get_tweets()
    for tweet in tweets:
        id = tweet.id
        list_link.append(f"https://twitter.com/{user}/status/{id}?s=20&t=wCS7mk5sE7QbkY3rE3hq3Q")
    i=1
    for link in list_link:
        asyncio.run(tweetcapture.screenshot(link, f"{i}.png", mode=0, night_mode=2))
        i+=1
    #Liste des images précedemment téléchargées
    list_img = [f for f in os.listdir('.') if f.endswith('.png')]
    resizing(list_img)

#Do the resizing
def resizing(list_img):
    for path in list_img:
        img = get_image(path)
        #Dimensions de l'image
        width, height = img.size
        #Valeur max entre les deux
        dimension = max(width, height)
        #Nouvelles dimensions de l'image
        size = dimension, dimension
        #Fond noir
        background_color = (0, 0, 0)
        #Créer une nouvelle image avec le fond noir
        fit_image = Image.new('RGB', size, background_color)
        #Récupère les dimensions du fond noir
        background_width, background_height = fit_image.size
        #Petit calcul pour dire de bien centrer l'image sur le fond noir
        offset = ((background_width - width) // 2, (background_height - height) // 2)
        #On colle l'image sur le fond noir
        fit_image.paste(img, offset)
        #On sauvegarde l'image
        fit_image.save(path)

#Get the image
def get_image(img):
    img = Image.open(img)
    return img

if __name__ == "__main__":
    main()