import mysql.connector
import os
class Produit:
    def __init__(self, nom, description, prix, quantite, id_categorie):
        self.nom = nom
        self.description = description
        self.prix = prix
        self.quantite = quantite
        self.id_categorie = id_categorie

    def save(self):
        password = os.getenv("PASSWORD")
        self.cnx = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = password,
        database = "boutique"
)

        cursor = db.cursor()
        sql = "INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)"
        values = (self.nom, self.description, self.prix, self.quantite, self.id_categorie)
        cursor.execute(sql, values)

        db.commit()
        print(cursor.rowcount, "record inserted.")

produit = Produit("Ordinateur portable", "Un ordinateur portable rapide et performant", 1000, 10, 1)
produit.save()