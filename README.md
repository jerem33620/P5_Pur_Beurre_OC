Projet 5 OpenClssRooms Pur-Beurre
Télecharger le fichier sur : (https://github.com/jerem33620/P5_Pur_Beurre_OC.git
Connectez-vous a mysql et sur PhpMyAdmin
Ensuite, il faudra vous mettre dans le dossier P5_Pur_Beurre_OC
(Tous les imports sont dans la partie env)
Modifiez le fichier config.json , il doit ressembler a ceci:
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
Executez le script avec par exemple Pycharm en allant sur le fichier main.py et RUN
Si c'est la première fois que vous executez l'application, vous devrez peut-etre attendre un peu avant que le menu apparaisse. C'est parce que la base de donnees se creer et va mettre à jour en faisant des demandes a Open Food Facts.
Ensuite vous pourrez tester librement votre nouvelle application qui vous permettra de choisir parmi des categories et des produits diverses et varies en note nutritionnelle "A/B/C/D/E".
J'ai choisit de faire une methode de travail agile. J'ai eu enormement de difficulte a comprendre par ou je devais commencer ou meme pour juste rapatrie les produits et categories du site OpenFoodFacts dans ma Base de Donnees. J'ai compris qu'il me fallait un fichier json pour substituer a mon probleme du transfert de fichier. J'ai toujours des difficultes a comprendre les erreurs, mais a force de perseverer, j'ai reussi a finir mon projet meme si j'ai mis plus de temps que prevu.
