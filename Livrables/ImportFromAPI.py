#! /usr/bin/env python3
# coding: utf-8

import requests


class ImportFromApi:
    """ Permet d'obtenir une ou plusieurs catégories et
        d'avoir 20 produits correspondants les plus populaires """

    def __init__(self, nutrition_grade, category):
        """ Donne un grade entre l'instance \'a\' et \'e\' ou un type 0
            pour aucune sélection de catégories """

        self.nutrition_grade = nutrition_grade
        self.category = category

    def get_json(self):
        """ Cette méthode produit la requête,
        soumet une requête à la bibliothéque
        et retourne un json avec les valeurs rendues """

        base_url = 'https://fr.openfoodfacts.org/cgi/search.pl'

        params = {"action": "process"}

        i = 0
        params.update({
            "tagtype_{}".format(i): "categories",
            "tag_contains_{}".format(i): "contains",
            "tag_{}".format(i): self.category
        })
        i += 1

        params.update({
            "tagtype_{}".format(i): "nutrition_grades",
            "tag_contains_{}".format(i): "contains",
            "tag_{}".format(i): self.nutrition_grade
        })

        params.update({"sort_by": "unique_scans_n", "page_size": 1500, "json": 1})

        r = requests.get(base_url, params=params)
        return r.json()
