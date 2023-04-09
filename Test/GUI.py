import mysql.connector
from dotenv import load_dotenv
import os
import tkinter as tk
import tkinter.ttk as ttk
from Produit import *
from Categorie import *


load_dotenv()

class Boutique:
    def __init__(self):
        password = os.getenv("PASSWORD")
        self.cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="boutique"
        )
        self.cursor = self.cnx.cursor()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Gestion des stocks")
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        # Créer un widget Label pour afficher le titre de l'application
        self.title_label = tk.Label(self, text="Gestion des stocks")
        self.title_label.pack()

        # Créer un widget Button pour ajouter un produit
        self.add_button = tk.Button(self, text="Ajouter un produit", command=self.add_produit)
        self.add_button.pack()

        # Créer un widget Button pour supprimer un produit
        self.delete_button = tk.Button(self, text="Supprimer un produit", command=self.delete_produit)
        self.delete_button.pack()

        # Créer un widget Button pour modifier un produit
        self.edit_button = tk.Button(self, text="Modifier un produit", command=self.edit_produit)
        self.edit_button.pack()

        # Créer un widget Label pour afficher la liste des produits
        self.produit_label = tk.Label(self, text="Liste des produits :")
        self.produit_label.pack()

        # Créer un widget Listbox pour afficher les produits
        self.produit_listbox = tk.Listbox(self)
        self.produit_listbox.pack()

        # Charger les produits depuis la base de données
        self.load_produits()

    def load_produits(self):
        # Se connecter à la base de données et récupérer les produits
        password = os.getenv("PASSWORD")
        self.cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="boutique"
        )
        self.cursor = self.cnx.cursor()

        self.cursor.execute("SELECT id, nom, description, prix, quantite, id_categorie FROM produit")
        produits = self.cursor.fetchall()

        # Ajouter les produits à la Listbox
        for produit in produits:
            self.produit_listbox.insert(tk.END, produit)

    def add_produit(self):
            # Créer une nouvelle fenêtre pour ajouter un produit
            top = tk.Toplevel(self)

            # Créer des widgets pour saisir les informations du produit
            nom_label = tk.Label(top, text="Nom :")
            nom_label.pack()
            nom_entry = tk.Entry(top)
            nom_entry.pack()

            description_label = tk.Label(top, text="Description :")
            description_label.pack()
            description_entry = tk.Entry(top)
            description_entry.pack()

            prix_label = tk.Label(top, text="Prix :")
            prix_label.pack()
            prix_entry = tk.Entry(top)
            prix_entry.pack()

            quantite_label = tk.Label(top, text="Quantité :")
            quantite_label.pack()
            quantite_entry = tk.Entry(top)
            quantite_entry.pack()

            # Ajouter le produit en cliquant sur le bouton "Ajouter"
            ajouter_button = tk.Button(top, text="Ajouter", command=lambda: self.save_produit(nom_entry.get(), description_entry.get(), prix_entry.get(), quantite_entry.get()))
            ajouter_button.pack()

            # Créer un widget Combobox pour sélectionner la catégorie
            categorie_combobox = ttk.Combobox(top, values=["Electronique", "Mode", "Maison"])
            categorie_combobox.pack()

            # Créer un widget Button pour enregistrer le produit
            save_button = tk.Button(top, text="Enregistrer", command=lambda: self.save_produit(
                nom_entry.get(),
                description_entry.get(),
                prix_entry.get(),
                quantite_entry.get(),
                categorie_combobox.get()
            ))
            save_button.pack()


    def save_produit(self, nom, description, prix, quantite):
        # Sauvegarder le produit dans la liste des produits
        self.produits.append({
            "nom": nom,
            "description": description,
            "prix": prix,
            "quantite": quantite
        })

        # Mettre à jour l'affichage des produits
        self.display_produits()


    def delete_produit(self):
        # Vérifier si un produit est sélectionné dans la Listbox
        selected_produit = self.produit_listbox.curselection()
        if not selected_produit:
            return

        # Récupérer l'ID du produit sélectionné
        produit_id = self.produit_listbox.get(selected_produit)[0]

        # Se connecter à la base de données et supprimer le produit
        password = os.getenv("PASSWORD")
        self.cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="boutique"
        )

        self.cursor = self.cnx.cursor()
        sql = "DELETE FROM produit WHERE id = %s"
        values = (produit_id,)
        self.cursor.execute(sql, values)
        self.cnx.commit()

        # Rafraîchir la liste des produits
        self.produit_listbox.delete(0, tk.END)
        self.load_produits()



    def edit_produit(self):
        # Vérifier si un produit est sélectionné dans la Listbox
        selected_produit = self.produit_listbox.curselection()
        if not selected_produit:
            return

        # Récupérer les informations du produit sélectionné
        produit = self.produit_listbox.get(selected_produit)[0]

        # Créer une nouvelle fenêtre pour modifier le produit
        top = tk.Toplevel(self)

        # Créer des widgets pour saisir les informations du produit
        nom_label = tk.Label(top, text="Nom :")
        nom_label.pack()
        nom_entry = tk.Entry(top, text=produit[1])
        nom_entry.pack()

        description_label = tk.Label(top, text="Description :")
        description_label.pack()
        description_entry = tk.Entry(top, text=produit[2])
        description_entry.pack()

        prix_label = tk.Label(top, text="Prix :")
        prix_label.pack()
        prix_entry = tk.Entry(top, text=produit[3])
        prix_entry.pack()

        quantite_label = tk.Label(top, text="Quantité :")
        quantite_label.pack()
        quantite_entry = tk.Entry(top, text=produit[4])
        quantite_entry.pack()

        categorie_label = tk.Label(top, text="Catégorie :")
        categorie_label.pack()

        # Créer un widget Combobox pour sélectionner la catégorie
        categorie_combobox = ttk.Combobox(top, values=["Electronique", "Mode", "Maison"], text=produit[5])
        categorie_combobox.pack()

        # Créer un widget Button pour enregistrer les modifications
        save_button = tk.Button(top, text="Enregistrer", command=lambda: self.update_produit(
            produit[0],
            nom_entry.get(),
            description_entry.get(),
            prix_entry.get(),
            quantite_entry.get(),
            categorie_combobox.current()+1
            ))
        save_button.pack()
    
    def update_produit(self, id, nom, description, prix, quantite, categorie):
    # Se connecter à la base de données et mettre à jour le produit
        password = os.getenv("PASSWORD")
        self.cnx = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = password,
        database = "boutique"
)

        cursor = db.cursor()
        sql = "UPDATE produit SET nom = %s, description = %s, prix = %s, quantite = %s, id_categorie = %s WHERE id = %s"
        values = (nom, description, prix, quantite, categorie, id)
        cursor.execute(sql, values)
        db.commit()

        # Rafraîchir la liste des produits
        self.produit_listbox.delete(0, tk.END)
        self.load_produits()

#Créer une instance de l'application et l'exécuter
app()
app.mainloop()




