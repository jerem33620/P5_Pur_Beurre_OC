#! /usr/bin/env python3
# coding: utf-8


class ExtractFromJson:
    """ Permet de recupérer les données brut dans le json
        rendu par l'API et de lancer l'initialisation du json """

    def __init__(self, json_data):
        """ Pour chaque produit enregistré dans la DB, j'aurais besoin de :
            id, product_name, categories, nutrition_grade, stores_tags, generic_name, url """
        self.keys = [
            "id",
            "product_name",
            "categories",
            "nutrition_grades",
            "stores_tags",
            "generic_name",
            "url"
        ]
        self.json_data = json_data

    def extract_json(self):
        """ Obtient les données brut dans le JSON rendu par l'API et crée un nouveau JSON
            avec seulement les données nécessaires pour ma base de données pur_beurre """
        # Liste des produits retournés
        products_list = []
        black_list = []

        for data in self.json_data["products"]:
            temp_dict = {}
            complete = True
            # Je crée une black_list pour éviter les doublons du même produit
            # Il est seulement basé sur les 4 premières lettres du produits

            if data["product_name"][:4].lower() not in black_list:
                black_list.append(data["product_name"][:4].lower())
                # Je vérifie si le champs est vide

                for key in self.keys:
                    # Si le champ n'est pas vide je l'ajoute au dict

                    if key in data and data[key] != "" and data[key] != []:
                        temp_dict[key] = data[key]
                    # Autrement je vais au produit suivant

                    else:
                        complete = False
                        break
                        
                # Si le dict est plein j'ajoute le produit à la liste
                if complete:
                    products_list.append(temp_dict)

        return products_list
