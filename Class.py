import mysql.connector
from dotenv import load_dotenv
import os



load_dotenv()

class Boutique:
    def __init__(self):
        password = os.getenv("PASSWORD")
        self.cnx = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = password,
        database = "boutique"
)
        self.cursor = self.cnx.cursor()

    def get_all_produits(self):
        query = "SELECT * FROM produit"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_categories(self):
        query = "SELECT * FROM categorie"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_produit(self, nom, description, prix, quantite):
        query = "INSERT INTO produit (nom, description, prix, quantite) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (nom, description, prix, quantite))
        self.cnx.commit()
        return self.cursor.lastrowid

    def remove_produit(self, id_produit):
        query = "DELETE FROM produit WHERE id_produit = %s"
        self.cursor.execute(query, (id_produit,))
        self.cnx.commit()

    def update_produit(self, id_produit, nom, description, prix, quantite, id_categorie):
        query = "SELECT COUNT(*) FROM categorie WHERE id_categorie = %s"
        self.cursor.execute(query, (id_categorie,))
        count = self.cursor.fetchone()[0]
        if count > 0:
            query = "UPDATE produit SET nom = %s, description = %s, prix = %s, quantite = %s, id_categorie = %s WHERE id_produit = %s"
            self.cursor.execute(query, (nom, description, prix, quantite, id_categorie, id_produit))
            self.cnx.commit()
            print("Produit modifié avec succès !")
        else:
            print("La catégorie spécifiée n'existe pas.")


    def __del__(self):
        self.cursor.close()
        self.cnx.close()

boutique = Boutique()

while True:
    print("Que souhaitez-vous faire ?")
    print("1 - Ajouter un produit")
    print("2 - Supprimer un produit")
    print("3 - Modifier un produit")

    choix = input("Votre choix : ")

    if choix == '1':
        nom = input("Nom du produit : ")
        description = input("Description du produit : ")
        prix = input("Prix du produit: ")
        quantite = input("Quantité de produits : ")
        boutique.add_produit(nom, description, prix, quantite)
        print("Produit ajouté avec succès !")

    elif choix == '2':
        id_produit = input("ID du produit à supprimer : ")
        boutique.remove_produit(id_produit)
        print("Produit supprimé avec succès !")

    elif choix == '3':
        id_produit = input("ID du produit : ")
        nom = input("Nouveau nom produit : ")
        description = input("Nouvelle description de produit : ")
        prix = input("Nouveau prix du produit : ")
        quantite = input("Nouvelle quantité de produit : ")
        id_categorie = input("Nouvel ID de categorie du produit : ")
        boutique.update_produit(id_produit, nom, description, prix, quantite, id_categorie)
        print("Produit modifié avec succès !")


    else:
        print("Choix invalide.")


