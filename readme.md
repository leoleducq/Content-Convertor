# Content-Convertor

Content-Convertor est un package python permettant de convertir des tweets en fichiers png prêts à être postés sur Instagram.

## Installation
Pour l'installer, il suffit de lancer la commande : `pip install contentconvertor`.

## Utilisation
Ce package comprends différentes fonctions.

1. `connexion_to_api` : permet de se connecter à l'API de Twitter. Il faut pour cela rentrer les clés d'API et les tokens d'accès. Pour les obtenir, il faut créer une application sur le site de Twitter.
    - Liste des paramètres dans l'ordre : 
        - `bearer_token` : token d'authentification `Bearer`
        - `consumer_key` : clé d'API
        - `consumer_secret` : clé secret d'API
        - `access_token` : token d'accès
        - `access_token_secret` : token secret d'accès
    - Retourne la connexion à l'API de Twitter  
    - Code d'exemple : 
    ```python
    api = connexion_to_api(
        bearer_token="",
        consumer_key="",
        consumer_secret="",
        access_token="",
        access_token_secret=""
    )
    ```

2. `get_tweets` : permet de récupérer les tweets d'un utilisateur. Il faut pour cela rentrer le nom de l'utilisateur et le nombre de tweets à récupérer.
    - Liste des paramètres dans l'ordre : 
        - `api` : connexion à l'API de Twitter (obtenue avec la fonction `connexion_to_api`)
        - `username` : nom de l'utilisateur (sans le @)
        - `nb_tweets` : nombre de tweets à récupérer
    - Retourne un utilisateur,  associé à une liste de tweets  
    - Code d'exemple : 
    ```python
    user = get_tweets(api, "iziatask", 10)
    ```

3. `download_tweets` : permet de télécharger au format png les tweets d'un utilisateur.
    - Liste des paramètres dans l'ordre : 
        - `user` : utilisateur (obtenu avec la fonction `get_tweets`)
    - Retourne rien, vous aurez vos tweets téléchargés au format png, à l'endroit où vous avez lancé votre script.
    - Code d'exemple : 
    ```python
    download_tweets(user)
    ```

4. `get_image` : permet de récupérer l'image d'un tweet. Il faut pour cela rentrer l'URL de l'image.
    - Liste des paramètres dans l'ordre : 
        - `url` : URL de l'image
    - Retourne l'objet Image
    - Code d'exemple : 
    ```python
    image = get_image("https://pbs.twimg.com/media/E1Z8Z7hXoA0ZQ8a.jpg")
    ```

5. `resizing` : permet de redimensionner une image.
    - Liste des paramètres dans l'ordre : 
        - `image` : objet Image (obtenu avec la fonction `get_image`)
    - Retourne rien, vous aurez votre image redimensionnée.
    - Code d'exemple : 
    ```python
    resizing(image)
    ```

## Exemple d'utilisation
Pour voir un exemple d'utilisation complet, rendez-vous ici : [GitHub](https://github.com/leoleducq/Content-Convertor/blob/master/example/example.py).