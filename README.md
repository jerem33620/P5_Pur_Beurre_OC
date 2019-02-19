# Projet 5 OpenClassRooms Pur-Beurre 

Tableau **[trello !](https://trello.com/b/BdchSBv2/purbeurre)**

Télécharger le fichier sûr : **[https://github.com/jerem33620/P5_Pur_Beurre_OC.git](https://github.com/jerem33620/P5_Pur_Beurre_OC.git)**

Connectez-vous à **[mysql](https://www.mysql.com/fr/)** et sur **[PhpMyAdmin](https://www.phpmyadmin.net/)**

Il faudra vous mettre dans le dossier ( **cd P5_Pur_Beurre_OC/Livrables** )

(Tous les **imports** sont dans la partie **venv** )

Modifiez le fichier **config.json** , il doit ressembler à ceci:

    ```json
    {
        "categories": [
            "Viandes",
            "Boissons",
            "Frais",
            "Produits laitiers",
            "Poissons",
            "Pains"
        ],
        "user": "root",
        "password" : "",
        "server": "localhost"
    }
    ```

Il faudra changer **root** et rajouter votre **mot de passe!**

Exécutez le script, avec par exemple **[Pycharm](https://www.jetbrains.com/pycharm/)** en allant sur le fichier **main.py** et **RUN**. 

Si, c'est la première fois que vous exécutez l'application, vous devrez peut-être attendre un peut avant que le menu apparaisse. 
C'est car, la base de données se créer et va mettre à jour en faisant des demandes à **[Open Food Facts](https://fr.openfoodfacts.org/).**

Ensuite vous pourrez tester librement votre nouvelle application, qui vous permettra de choisir parmi des catégories et des produits diverses et variés en note nutritionnelle  "A/B/C/D/E" .


J'ai eu des difficultés à comprendre par où je devais commencer ou même pour juste rapatrié les produits et catégories du site OpenFoodFacts dans ma Base de Données. 
J'ai compris qu'il me fallait un fichier json pour substituer à mon problème du transfert de fichier. J'ai toujours des difficultés à comprendre les erreurs, mais à force de persévérer, j'ai réussi à finir mon projet, même si j'ai mis plus de temps que prévu.
    ```json
    {
        "categories": [
            "produits laitiers",
            "boissons",
            "desserts",
            "plats préparés",
            "snacks sucrés"
        ],
        "user": "USER",
        "password" : "PASSWORD",
        "server": "localhost"
    }
    ```