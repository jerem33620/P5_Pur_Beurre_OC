#! /usr/bin/env python3
# coding: utf-8

import json
import random
import sys
import records

from TablesCreator import TablesCreator
from DatabaseCreator import DatabaseUpdator
from ExtractJson import ExtractFromJson
from ImportFromAPI import ImportFromApi


class Database:
    """ Permet de faire toutes les demandes nécessaires à la base de données """

    def __init__(self, usr, pswd, server):
        self.db = None
        self.usr = usr
        self.pswd = pswd
        self.server = server

    def connect(self):
        """ Permet de créez une connexion à la base de données """
        try:
            self.db = records.Database(
                'mysql+pymysql://{}:{}@{}'.format(self.usr, self.pswd, self.server))
        except:
            print("Les informations de connexion sont erronées:\nVérifiez votre fichier config.json")
        self.db.query('USE pur_beurre')

    def create_base(self):
        """ Permet de créez la base de donnée si elle n'existe pas """
        self.db.query(
            'CREATE DATABASE IF NOT EXISTS pur_beurre CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')

    def create_tables(self):
        """ Permet de créez toutes les tables nécéssaires à la base de donnée """
        self.table = TablesCreator(self.db)
        self.table.store_create()
        self.table.product_create()
        self.table.category_create()
        self.table.product_category_create()
        self.table.save_create()
        self.table.product_store_create()

    def fill_in(self, grade, category):
        """ Permet de rajouter tous les produits de la catégorie
        et du grade nutritionelle dans la base de données """
        api_json = ImportFromApi(grade, category)
        extracted_data = ExtractFromJson(api_json.get_json())
        self.fill_in_db = DatabaseUpdator(extracted_data.extract_json(), self.db)
        self.fill_in_db.table_store_update()
        self.fill_in_db.table_product_update()
        self.fill_in_db.table_category_update()
        self.fill_in_db.table_product_category_update()
        self.fill_in_db.table_product_store_update()

    def clean_product_category(self):
        """ Supprime la partie de product_category pour la nettoyer,
        ce qui supprime tous les produits non sauvegarder """
        try:
            self.db.query("DELETE FROM product_category\
                WHERE PC_PROD_id NOT IN (\
                SELECT SAU_PROD_id FROM save)")
            print("product_category cleaned")
        except:
            print("un problème est survenue lors du nettoyage de product_category")
            print("Erreur :", sys.exc_info()[0])

    def clean_product_store(self):
        """ Même principe que pour clean_product_category, sauf que ici c'est pour les magasins """
        try:
            self.db.query("DELETE FROM product_store\
                WHERE PS_PROD_id NOT IN \
                (SELECT SAU_PROD_id FROM save)")
            print("product_store cleaned")
        except:
            print("un problème est survenue lors du nettoyage de product_store")
            print("Erreur :", sys.exc_info()[0])

    def clean_product(self):
        """ Supprime toutes les données dans la table product sauf les produits PROD_id
        qui sont sauvegarder """
        try:
            self.db.query("DELETE FROM product\
                WHERE PROD_id NOT IN (SELECT SAU_PROD_id FROM save)")
            print("product cleaned")
        except:
            print("un problème est survenue lors du nettoyage de product")
            print("Erreur :", sys.exc_info()[0])

    def save_product(self, id):
        """ Permet d'obtenir PROD_id qui va le sauvegardé dans la table save
        et vérifié si il est dans la table product """
        try:
            self.db.query("INSERT INTO save VALUES (:id)", id=id)
        except:
            prod_name = self.db.query(
                "SELECT PROD_name FROM product WHERE PROD_id = :id", id=id)
            print("{} est déjà dans la base".format(prod_name.export('json')))

    def delete_from_save(self, prod_id):
        """ Permet de supprimer un produit de la table save """
        try:
            self.db.query("DELETE FROM save\
            WHERE SAU_PROD_id = :id", id=prod_id)
        except:
            input("une erreur est survenue")

    def get_grade_e_products(self, category):
        """ Permet de prendre une catégorie et de retourner aléatoirement 20 produits
         de cette catégorie 'on peut changer ici le nombre de produits qui sera présenté' """
        rows = self.db.query("SELECT product.PROD_name, product.PROD_descr, product.PROD_id\
            FROM product\
            INNER JOIN product_category\
            ON product.PROD_id = product_category.PC_PROD_id\
            INNER JOIN category\
            ON product_category.PC_CAT_id = category.CAT_id\
            WHERE CAT_nom = :category\
            ORDER BY RAND()\
            LIMIT 20;", category=category)

        return json.loads(rows.export('json'))

    def get_grade_a_products_id(self, category):
        """ Propose un produit de substitution plus sain de grade A """
        rows = self.db.query("SELECT product.PROD_id\
            FROM product\
            INNER JOIN product_category\
            ON product.PROD_id = product_category.PC_PROD_id\
            INNER JOIN category\
            ON product_category.PC_CAT_id = category.CAT_id\
            WHERE CAT_nom = :category AND PROD_grade = 'a'",
                             category=category)
        return json.loads(rows.export('json'))

    def get_cat_id_list(self, product_id):
        """ Retourne une liste des catégories d'un produit """
        rows = self.db.query("SELECT PC_CAT_id FROM product_category\
            WHERE PC_PROD_id = :prod_id",
                             prod_id=product_id)
        return json.loads(rows.export('json'))

    def get_prod_id_by_name(self, name):
        """ Obtient le nom d'un produit et retourne l'id """
        rows = self.db.query("SELECT PROD_id FROM product\
            WHERE PROD_name = :name",
                             name=name)
        return json.loads(rows.export('json'))

    def get_best_match(self, prod_id, cat_id):
        """ Permet d'obtenir des produits PROD_id et sa catégorie principale CAT_id
            et retourne un produit de substitution de grade A similaire au produit choisi """
        prod_id_list = []
        liste_set = []
        matches_list = []

        prod_id_list.append(prod_id)

        for item in (self.get_grade_a_products_id(cat_id)):
            prod_id_list.append(item["PROD_id"])

        for prod_id in prod_id_list:
            cat_id_set = set()
            for cat_id in (self.get_cat_id_list(prod_id)):
                cat_id_set.add(cat_id["PC_CAT_id"])
            liste_set.append(cat_id_set)

        for loop in range(1, len(liste_set)):
            matches_list.append(len(set(liste_set[0] & set(liste_set[loop]))))
        max_matches = max(matches_list)

        index_matches = [i + 1 for i in range(len(matches_list)) if matches_list[i] == max_matches]

        return prod_id_list[random.choice(index_matches)]

    def get_prod_by_id(self, prod_id):
        """ Obtient toutes les informations sur un produit de la table 'product' """
        rows = self.db.query("SELECT * FROM product WHERE PROD_id = :id", id=prod_id)
        return json.loads(rows.export('json'))

    def get_stores_by_prod_id(self, prod_id):
        """ Obtient tous les magasins associés au produit sélectionné """
        rows = self.db.query("SELECT store.MAG_nom\
            FROM store\
            INNER JOIN product_store\
                ON store.MAG_id = product_store.PS_MAG_id\
            INNER JOIN product\
                ON product_store.PS_PROD_id = product.PROD_id\
            WHERE PROD_id = :id", id=prod_id)
        return json.loads(rows.export('json'))

    def get_fav(self):
        """ Retourne la liste SAU_PROD_id de la table 'save' """
        rows = self.db.query("SELECT SAU_PROD_id FROM save")
        return json.loads(rows.export('json'))
