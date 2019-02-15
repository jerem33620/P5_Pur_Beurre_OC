#! venv\Scripts\activate
# coding: utf-8

import sys
import os
import json

from Database import Database


class AppPurBeurre:
    """ Gère l'interface de l'utilisateur et la connexion à la base de donnée """

    def __init__(self, arg):

        try:
            self.arg = arg[1]
        except:
            self.arg = None

        with open("./config.json") as f:
            self.config = json.load(f)

        self.pur_beurre = Database(
            self.config["user"], self.config["password"], self.config["server"])

        try:
            self.pur_beurre.connect()
            print("Connexion réussie")
        except:
            # Permet de mettre tous les fichiers dans la base de donnée
            # et de les mètres à jours
            print("la base n'existe pas")
            self.pur_beurre.create_base()
            self.pur_beurre.create_tables()
            self.pur_beurre.connect()
            for category in self.config["categories"]:
                self.pur_beurre.fill_in('a', category)
                self.pur_beurre.fill_in('b', category)
                self.pur_beurre.fill_in('c', category)
                self.pur_beurre.fill_in('d', category)
                self.pur_beurre.fill_in('e', category)

        try:
            if self.arg == '-update':
                print("mise à jour")
                self.pur_beurre.clean_product_category()
                self.pur_beurre.clean_product_store()
                self.pur_beurre.clean_product()
                for category in self.config["categories"]:
                    self.pur_beurre.fill_in('a', category)
                    self.pur_beurre.fill_in('b', category)
                    self.pur_beurre.fill_in('c', category)
                    self.pur_beurre.fill_in('d', category)
                    self.pur_beurre.fill_in('e', category)
        except:
            pass

    def show_category_menu(self):
        """ Permet à l'utilisateur de choisir parmi plusieurs catégories un produit """
        while True:
            cat_num = 0

            os.system('cls' if os.name == 'nt' else 'clear')

            print("Bienvenue sur l'application Pur Beurre")
            print("Entrez un chiffre correspondant à la catégorie que vous souhaitez choisir!")
            for category in self.config["categories"]:
                print("Pour la catégorie {} tapez le chiffre {} "
                      "puis appuyer sur la touche entrée! ".format(category, cat_num))
                cat_num += 1
            print("Pour consulter votre liste de produits favoris tapez '1' entrée, puis 'f' !")
            user_input = input(">")

            try:
                if 0 <= int(user_input) <= cat_num:
                    return int(user_input)
            except:
                pass

    def show_category_products(self, usr_input_category):
        a = int(usr_input_category)
        """ Permet à l'utilisateur de choisir parmi au moins 20 produits """
        while True:
            print(usr_input_category)
            category = self.config["categories"][a]
            prod_nb = 0

            request_json = self.pur_beurre.get_grade_e_products(category)
            os.system('cls' if os.name == 'nt' else 'clear')

            print("Veuillez sélectionner un produit de la catégorie {}".format(category))
            print("Entrez le numéro associé et trouvez un aliement de substitution plus saint:")

            for product in request_json:
                print("{num} : {prod_name}".format(
                    num=prod_nb, prod_name=product["PROD_name"]))
                print("    {descr}\n".format(descr=product["PROD_descr"]))
                prod_nb += 1

            user_input_product = input(">")

            try:
                if 0 <= int(user_input_product) <= prod_nb:
                    return self.pur_beurre.get_prod_id_by_name(request_json[int(user_input_product)]["PROD_name"])
            except:
                pass

    def show_best_match(self, product_id, category_index):
        """ Montre le produit le plus pertinent stocké dans la base de donnée """

        os.system('cls' if os.name == 'nt' else 'clear')
        best_match_id = self.pur_beurre.get_best_match(product_id, self.config["categories"][category_index])

        grade_e_prod = self.pur_beurre.get_prod_by_id(product_id)
        match_prod = self.pur_beurre.get_prod_by_id(best_match_id)
        match_prod_store = self.pur_beurre.get_stores_by_prod_id(best_match_id)

        print("En replacement de \'{name}\' nous vous conseillons le produit suivant:\n".format(
            name=grade_e_prod[0]["PROD_name"]))
        print("{name} :\n{descr}\n".format(name=match_prod[0]["PROD_name"],
                                           descr=match_prod[0]["PROD_descr"]))
        print("Ce produit a une note nutritionelle {note}\n".format(note=match_prod[0]["PROD_grade"]))
        print("Vous pouvez vous le procurer dans les magasins suivants :")
        for mag in match_prod_store:
            print("\t{}".format(mag["MAG_nom"]))
        print("Lien vers la fiche du produit :\n{url}".format(url=match_prod[0]["PROD_url"]))

        self.show_save_product(match_prod[0]["PROD_id"])

    def show_save_product(self, product_id):
        """ Montre la liste des produits dans vos favoris """

        print("Pour enregistrer ce produit dans vos favoris entrez 's'")
        print("pour revenir au menu appuyez sur n'importe quelle touche:")
        user_input = input(">")

        if user_input.lower() == 's':
            self.pur_beurre.save_product(product_id)
        # else:
        #    self.show_save_product(product_id)

    def show_fav(self):
        """ Montre les produits sauvegarder dans les favoris par l'utilisateur
            et permet aussi de choisir le produit à supprimer! """
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            i = 0
            fav_prod_list = self.pur_beurre.get_fav()

            print("Pour supprimer un produit de vos favoris,")
            print("entrez le numéro correspondant au produit\n")
            for prod_id in fav_prod_list:
                prod = self.pur_beurre.get_prod_by_id(prod_id["SAU_PROD_id"])
                prod_store = self.pur_beurre.get_stores_by_prod_id(prod_id["SAU_PROD_id"])
                print("{i} :\n{name}".format(i=i, name=prod[0]["PROD_name"]))
                print(prod[0]["PROD_descr"])
                print("{url}".format(url=prod[0]["PROD_url"]))
                print("Est vendu dans les enseignes suivantes :")
                for mag in prod_store:
                    print(mag["MAG_nom"], '')
                print(fav_prod_list)
                i += 1
            user_input = input("Entrez un numéro de produit\nou tapez sur n'importe quelle touche pour quitter >")
            try:
                if 0 <= int(user_input) <= i:
                    self.pur_beurre.delete_from_save(fav_prod_list[int(user_input)]["SAU_PROD_id"])
            except:
                break


def main(argv):
    # Commence une nouvelle configuration de session à la base de donnée et le met à jours si besoin
    new_session = AppPurBeurre(argv)

    while True:
        # Montre le menu catégorie, retourne la catégorie choisie
        # et demande à l'utilisateur d'appuyer sur la touche 'f'
        # pour consulter ses produits péférés
        category_index_input = new_session.show_category_menu()
        category_input = input("Confirmer votre chiffre ou tapez 'f':")

        if category_input == 'f':
            new_session.show_fav()

        else:

            # Montre les produits de la catégorie choisie et retourne le produit sélectionné
            product_id_input = new_session.show_category_products(category_index_input)
            # Montre le produit de substitution qui est plus sain de grade A
            new_session.show_best_match(product_id_input[0]["PROD_id"], category_index_input)


if __name__ == '__main__':
    main(sys.argv)
