{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang1036{\fonttbl{\f0\fnil\fcharset0 Calibri;}}
{\colortbl ;\red0\green0\blue255;}
{\*\generator Riched20 10.0.17134}\viewkind4\uc1 
\pard\sa200\sl276\slmult1\qc\f0\fs30\lang12 Projet 5 OpenClassRooms Pur-Beurre \fs22\par

\pard\sa200\sl276\slmult1 T\'e9lecharger le fichier sur : ({{\field{\*\fldinst{HYPERLINK https://github.com/jerem33620/P5_Pur_Beurre_OC.git }}{\fldrslt{https://github.com/jerem33620/P5_Pur_Beurre_OC.git\ul0\cf0}}}}\f0\fs22 )\par
Connectez-vous a mysql et sur PhpMyAdmin\par
Ensuite, il faudra vous mettre dans le dossier P5_Pur_Beurre_OC\par
(Tous les imports sont dans la partie env)\par
Modifiez le fichier config.json , il doit ressembler a ceci:\par
\{\par
    "categories": [\par
        "Viandes",\par
        "Boissons",\par
        "Frais",\par
        "Produits laitiers",\par
        "Poissons",\par
        "Pains"\par
    ],\par
    "user": "root",\par
    "password" : "",\par
    "server": "localhost"\par
\}\par
Executez le script avec par exemple Pycharm en allant sur le fichier main.py et RUN\par
Si c'est la premi\'e8re fois que vous executez l'application, vous devrez peut-etre attendre un peu avant que le menu apparaisse. C'est parce que la base de donnees se creer et va mettre \'e0 jour en faisant des demandes a Open Food Facts.\par
Ensuite vous pourrez tester librement votre nouvelle application qui vous permettra de choisir parmi des categories et des produits diverses et varies en note nutritionnelle "A/B/C/D/E".\par
J'ai choisit de faire une methode de travail agile. J'ai eu enormement de difficulte a comprendre par ou je devais commencer ou meme pour juste rapatrie les produits et categories du site OpenFoodFacts dans ma Base de Donnees. J'ai compris qu'il me fallait un fichier json pour substituer a mon probleme du transfert de fichier. J'ai toujours des difficultes a comprendre les erreurs, mais a force de perseverer, j'ai reussi a finir mon projet meme si j'ai mis plus de temps que prevu.\par
\par
}
 