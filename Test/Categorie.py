import mysql.connector
import os

class Categorie:
    def __init__(self, nom):
        self.nom = nom

    def save(self):
        password = os.getenv("PASSWORD")
        self.cnx = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = password,
        database = "boutique"
)

        cursor = db.cursor()
        sql = "INSERT INTO categorie (nom) VALUES (%s)"
        values = (self.nom,)
        cursor.execute(sql, values)

        db.commit()
        print(cursor.rowcount, "record inserted.")

categorie = Categorie("Electronique")
categorie.save()
