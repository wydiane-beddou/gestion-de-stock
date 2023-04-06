import tkinter as tk
import tkinter.messagebox as tkmessagebox
import Gestion_de_stock


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        # centrer la fenêtre principale
        width = 400
        height = 300
        x = (self.master.winfo_screenwidth() - width) // 2
        y = (self.master.winfo_screenheight() - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.add_button = tk.Button(self, text="Ajouter un produit", command=self.add_produit)
        self.add_button.pack(side="top")

        self.remove_button = tk.Button(self, text="Supprimer un produit", command=self.remove_produit)
        self.remove_button.pack(side="top")

        self.update_button = tk.Button(self, text="Modifier un produit", command=self.update_produit)
        self.update_button.pack(side="top")

    def add_produit(self):
        self.top = tk.Toplevel(self)
        self.top.title("Ajouter un produit")

        tk.Label(self.top, text="Nom du produit : ").grid(row=0, column=0)
        self.nom_entry = tk.Entry(self.top)
        self.nom_entry.grid(row=0, column=1)

        tk.Label(self.top, text="Description du produit : ").grid(row=1, column=0)
        self.description_entry = tk.Entry(self.top)
        self.description_entry.grid(row=1, column=1)

        tk.Label(self.top, text="Prix du produit : ").grid(row=2, column=0)
        self.prix_entry = tk.Entry(self.top)
        self.prix_entry.grid(row=2, column=1)

        tk.Label(self.top, text="Quantité de produits : ").grid(row=3, column=0)
        self.quantite_entry = tk.Entry(self.top)
        self.quantite_entry.grid(row=3, column=1)

        self.submit_button = tk.Button(self.top, text="Ajouter", command=self.add_produit_db)
        self.submit_button.grid(row=4, column=0, columnspan=2)

    def add_produit_db(self):
        nom = self.nom_entry.get()
        description = self.description_entry.get()
        prix = float(self.prix_entry.get())
        quantite = int(self.quantite_entry.get())
        Gestion_de_stock.boutique.add_produit(nom, description, prix, quantite)
        self.top.destroy()

    def remove_produit(self):
        self.top = tk.Toplevel(self)
        self.top.title("Supprimer un produit")

        tk.Label(self.top, text="ID du produit à supprimer : ").grid(row=0, column=0)
        self.id_produit_entry = tk.Entry(self.top)
        self.id_produit_entry.grid(row=0, column=1)

        self.submit_button = tk.Button(self.top, text="Supprimer", command=self.remove_produit_db)
        self.submit_button.grid(row=1, column=0, columnspan=2)

    def remove_produit_db(self):
        id_produit = int(self.id_produit_entry.get())
        try:
            Gestion_de_stock.boutique.remove_produit(id_produit)
            tkmessagebox.showinfo("Suppression réussie", "Le produit a été supprimé avec succès")
        except ValueError:
            tkmessagebox.showerror("Suppression échouée", "Le produit avec cet ID n'existe pas")
        self.top.destroy()

    def update_produit(self):
        self.top = tk.Toplevel(self)
        self.top.title("Modifier un produit")

        tk.Label(self.top, text="ID du produit : ").grid(row=0, column=0)
        self.id_produit_entry = tk.Entry(self.top)
        self.id_produit_entry.grid(row=0, column=1)

        tk.Label(self.top, text="Nouveau prix du produit : ").grid(row=2, column=0)
        self.prix_entry = tk.Entry(self.top)
        self.prix_entry.grid(row=2, column=1)

        tk.Button(self.top, text="Modifier", command=self.modify_produit).grid(row=3, column=1, sticky=tk.E)


    def modify_produit(self):
        id_produit = self.id_produit_entry.get()
        nom = self.nom_entry.get()
        prix = self.prix_entry.get()

        # Vérification si les champs sont remplis
        if not id_produit or not nom or not prix:
            tk.messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        # Vérification si l'ID du produit existe dans la base de données
        if not self.db.check_id_produit(id_produit):
            tk.messagebox.showerror("Erreur", "ID de produit invalide")
            return

        # Vérification si le nom du produit est unique
        if self.db.check_nom_produit(nom) and not self.db.check_nom_produit_for_id(id_produit, nom):
            tk.messagebox.showerror("Erreur", "Le nom du produit doit être unique")
            return

        # Vérification si le prix est un nombre valide
        try:
            prix = float(prix)
        except ValueError:
            tk.messagebox.showerror("Erreur", "Le prix doit être un nombre valide")
            return

        # Mise à jour du produit
        self.db.update_produit(id_produit, nom, prix)
        tk.messagebox.showinfo("Succès", "Produit mis à jour avec succès")

        # Rafraîchissement de l'affichage
        self.refresh_table()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
