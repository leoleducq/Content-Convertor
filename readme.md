# Content-Convertor

Content-Convertor est un package python permettant de convertir des tweets en fichiers png prêts à être postés sur Instagram.

## Installation
Pour l'installer, il suffit de lancer la commande : `pip install contentconvertor`.

## Utilisation
Ce package comprends différentes fonctions.

1. `connexion_to_api` : permet de se connecter à l'API de Twitter. Il faut pour cela rentrer les clés d'API et les tokens d'accès. Pour les obtenir, il faut créer une application sur le site de Twitter.  
**Liste des paramètres dans l'ordre**
    - `bearer_token` : clé d'API (Bearer Token)

    **Retourne la connexion à l'API de Twitter**  
- Code d'exemple : 
    ```python
    api = connexion_to_api(bearer_token="")
    ```
2. `get_user_id` : permet de récupérer l'id d'un utilisateur. Il faut pour cela rentrer le nom de l'utilisateur.  
**Liste des paramètres dans l'ordre**
    - `api` : connexion à l'API de Twitter (obtenue avec la fonction `connexion_to_api`)
    - `username` : nom de l'utilisateur (sans le @)

    **Retourne l'id de l'utilisateur**

3. `get_tweets` : permet de récupérer les tweets d'un utilisateur. Il faut pour cela rentrer le nom de l'utilisateur et le nombre de tweets à récupérer.  
    **Liste des paramètres dans l'ordre**
- Obligatoire :
    - `api` : connexion à l'API de Twitter (obtenue avec la fonction `connexion_to_api`)
    - `user_id` : ID de l'utilisateur (obtenu avec la fonction `get_user_id`)
- Optionnel :
    - `nb_tweets` : nombre de tweets à récupérer (par défaut : 5)
    - `exclude` : exclure les tweets de type "replies" ou "retweets" (par défaut : None) 

    **Retourne une liste de tweets**  
- Code d'exemple : 
    - Minimum requis
    ```python
    list_tweets = get_tweets(api, "iziatask")
    ```
    - Avec tous les paramètres
    ```python
    list_tweets = get_tweets(api, "iziatask", nb_tweets=5, exclude=["replies", "retweets"])
    ```

4. `download_tweets` : permet de télécharger au format png les tweets d'un utilisateur.  
**Liste des paramètres dans l'ordre**
    - Obligatoire :
        - `user` : utilisateur 
        - `tweets` : (obtenu avec la fonction `get_tweets`)
    - Optionnel :
        - `path` : chemin où télécharger les tweets (par défaut : "")
        - `mode` : mode de capture d'écran (par défaut  : 0)
        - `nigh_mode` : mode nuit (par défaut : 2)  

    **Retourne rien, vous aurez vos tweets téléchargés au format png, à l'endroit où vous avez lancé votre script.**
- Code d'exemple :  
    - Minimum requis
    ```python
    download_tweets(user, tweets)
    ```
    - Avec tous les paramètres
    ```python
    download_tweets(user, tweets, path="images", mode=0, nigh_mode=2)
    ```

5. `get_image` : permet de récupérer l'image d'un tweet. Il faut pour cela rentrer le path de l'image.  
**Liste des paramètres dans l'ordre**  
        - `path` : path de l'image  
**Retourne l'objet Image**
- Code d'exemple : 
    ```python
    image = get_image("chemin/vers/image.png")
    ```

6. `resizing` : permet de redimensionner une image.  
**Liste des paramètres dans l'ordre**  
        - `image` : objet Image (obtenu avec la fonction `get_image`)  
**Retourne rien, vous aurez votre image redimensionnée enregistrée au même endroit que précédemment.**
    - Code d'exemple : 
    ```python
    resizing(image)
    ```

## Exemple d'utilisation
Pour voir un exemple d'utilisation complet, rendez-vous ici : [GitHub](https://github.com/leoleducq/Content-Convertor/blob/master/example/example.py).