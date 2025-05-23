import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Klasse für Produkte im Shop
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    # Umwandeln in Dictionary für JSON-Speicherung
    def to_dict(self):
        return {"name": self.name, "price": self.price, "quantity": self.quantity}

    # Erstellen eines Produkts aus Dictionary-Daten (z.B. aus JSON)
    @staticmethod
    def from_dict(data):
        return Product(data["name"], data["price"], data["quantity"])

# Klasse für den Einkaufswagen
class ShoppingCart:
    def __init__(self):
        self.items = []

    # Produkt zum Warenkorb hinzufügen, wenn Menge verfügbar
    def add(self, product):
        if product.quantity <= 0:
            return False
        self.items.append(product)
        return True

    # Gesamtsumme aller Produkte im Warenkorb berechnen
    def total(self):
        return sum(item.price for item in self.items)

    # Warenkorb leeren
    def clear(self):
        self.items = []

    # Liste der Produkte im Warenkorb als String zurückgeben
    def list_items(self):
        return "\n".join([f"{item.name} - {item.price:.2f} €" for item in self.items])

# Klasse zur Verwaltung von Verkäufern
class Seller:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    # Umwandeln in Dictionary für JSON-Speicherung
    def to_dict(self):
        return {"email": self.email, "password": self.password}

    # Erstellen eines Verkäufers aus Dictionary-Daten
    @staticmethod
    def from_dict(data):
        return Seller(data["email"], data["password"])

# Hauptklasse der Shop-Anwendung
class ShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛍️ Elektronischer Shop")

        # Schriftarten definieren (größer und besser lesbar)
        self.default_font = ("Arial", 18, "bold")
        self.button_font = ("Arial", 16, "bold")
        self.label_font = ("Arial", 18, "bold")

        self.cart = ShoppingCart()
        self.products = []
        self.sellers = []
        self.logged_in_seller = None
        self.load_products()
        self.load_sellers()
        self.main_menu()

    # Hauptmenü des Shops anzeigen
    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Willkommen im Shop", font=self.label_font).pack(pady=15)

        tk.Button(self.root, text="🛒 Zum Kundenbereich", font=self.button_font, command=self.customer_view, width=25).pack(pady=8)
        tk.Button(self.root, text="🧾 Verkäufer Login", font=self.button_font, command=self.seller_login_view, width=25).pack(pady=8)
        tk.Button(self.root, text="📝 Verkäufer Registrierung", font=self.button_font, command=self.seller_register_view, width=25).pack(pady=8)

    # Alle Widgets im Fenster löschen
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Produkte in JSON-Datei speichern
    def save_products(self):
        with open("produkte.json", "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.products], f, ensure_ascii=False, indent=4)

    # Produkte aus JSON-Datei laden
    def load_products(self):
        if os.path.exists("produkte.json"):
            with open("produkte.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.products = [Product.from_dict(p) for p in data]

    # Verkäuferdaten in JSON-Datei speichern
    def save_sellers(self):
        with open("verkaeufer.json", "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.sellers], f, ensure_ascii=False, indent=4)

    # Verkäuferdaten aus JSON-Datei laden
    def load_sellers(self):
        if os.path.exists("verkaeufer.json"):
            with open("verkaeufer.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.sellers = [Seller.from_dict(s) for s in data]

    # Ansicht für Verkäuferregistrierung
    def seller_register_view(self):
        self.clear_window()
        tk.Label(self.root, text="Verkäufer Registrierung", font=self.label_font).pack(pady=15)

        tk.Button(self.root, text="⬅ Zurück", font=self.button_font, command=self.main_menu).pack(side=tk.BOTTOM, pady=10)

        # E-Mail abfragen, abbrechen bei None (Cancel)
        email = simpledialog.askstring("E-Mail", "Bitte geben Sie Ihr Name ein:")
        if email is None:
            self.main_menu()
            return

        # Passwort abfragen, abbrechen bei None (Cancel)
        password = simpledialog.askstring("Passwort", "Bitte geben Sie Ihr Passwort ein:", show='*')
        if password is None:
            self.main_menu()
            return

        # Prüfen ob E-Mail schon registriert ist
        for seller in self.sellers:
            if seller.email == email:
                messagebox.showerror("Fehler", "Name bereits registriert!")
                self.main_menu()
                return

        # Neuen Verkäufer anlegen und speichern
        new_seller = Seller(email, password)
        self.sellers.append(new_seller)
        self.save_sellers()
        messagebox.showinfo("Erfolg", "Registrierung erfolgreich! Bitte melden Sie sich an.")
        self.main_menu()

    # Ansicht für Verkäufer-Login
    def seller_login_view(self):
        self.clear_window()
        tk.Label(self.root, text="Verkäufer Login", font=self.label_font).pack(pady=15)

        tk.Button(self.root, text="⬅ Zurück", font=self.button_font, command=self.main_menu).pack(side=tk.BOTTOM, pady=10)

        # E-Mail abfragen, abbrechen bei None (Cancel)
        email = simpledialog.askstring("E-Mail", "Bitte geben Sie Ihr Name ein:")
        if email is None:
            self.main_menu()
            return

        # Passwort abfragen, abbrechen bei None (Cancel)
        password = simpledialog.askstring("Passwort", "Bitte geben Sie Ihr Passwort ein:", show='*')
        if password is None:
            self.main_menu()
            return

        # Überprüfen der Anmeldedaten
        for seller in self.sellers:
            if seller.email == email and seller.password == password:
                self.logged_in_seller = seller
                self.seller_view()
                return

        # Fehlermeldung bei falschen Daten
        messagebox.showerror("Fehler", "Ungültige Anmeldedaten!")
        self.main_menu()

    # Verkäuferbereich zur Produktverwaltung
    def seller_view(self):
        self.clear_window()
        tk.Label(self.root, text=f"Verkäuferbereich - {self.logged_in_seller.email}", font=self.label_font).pack(pady=15)

        frame = tk.Frame(self.root)
        frame.pack()

        # Produkte auflisten mit Bearbeiten- und Löschen-Buttons
        for idx, product in enumerate(self.products):
            tk.Label(frame, text=f"{product.name} - {product.price:.2f} € - {product.quantity} Stück", font=("Arial", 14)).grid(row=idx, column=0, sticky='w', padx=10, pady=4)
            tk.Button(frame, text="Bearbeiten", font=self.button_font, command=lambda i=idx: self.edit_product(i)).grid(row=idx, column=1, padx=5)
            tk.Button(frame, text="Löschen", font=self.button_font, command=lambda i=idx: self.delete_product(i)).grid(row=idx, column=2, padx=5)

        # Button zum Hinzufügen neuer Produkte
        tk.Button(self.root, text="➕ Neues Produkt hinzufügen", font=self.button_font, command=self.add_product).pack(pady=8)
        tk.Button(self.root, text="⬅ Abmelden", font=self.button_font, command=self.logout_seller).pack(pady=8)

    # Neues Produkt hinzufügen
    def add_product(self):
        name = simpledialog.askstring("Produktname", "Geben Sie den Produktnamen ein:")
        if name is None:
            self.seller_view()
            return
        try:
            price_str = simpledialog.askstring("Preis", "Geben Sie den Preis in Euro ein:")
            if price_str is None:
                self.seller_view()
                return
            price = float(price_str)

            quantity_str = simpledialog.askstring("Menge", "Geben Sie die Menge ein:")
            if quantity_str is None:
                self.seller_view()
                return
            quantity = int(quantity_str)

            if quantity < 0:
                raise ValueError("Negative Menge nicht erlaubt")

            self.products.append(Product(name, price, quantity))
            self.save_products()
            messagebox.showinfo("Hinzugefügt", f"'{name}' wurde erfolgreich hinzugefügt.")
            self.seller_view()
        except Exception:
            messagebox.showerror("Fehler", "Ungültige Eingabe! Bitte überprüfen Sie Ihre Daten.")
            self.seller_view()

    # Produkt bearbeiten
    def edit_product(self, index):
        product = self.products[index]
        name = simpledialog.askstring("Produktname bearbeiten", "Neuer Name:", initialvalue=product.name)
        if name is None:
            self.seller_view()
            return
        try:
            price_str = simpledialog.askstring("Preis bearbeiten", "Neuer Preis in Euro:", initialvalue=str(product.price))
            if price_str is None:
                self.seller_view()
                return
            price = float(price_str)

            quantity_str = simpledialog.askstring("Menge bearbeiten", "Neue Menge:", initialvalue=str(product.quantity))
            if quantity_str is None:
                self.seller_view()
                return
            quantity = int(quantity_str)

            if quantity < 0:
                raise ValueError("Negative Menge nicht erlaubt")

            product.name = name
            product.price = price
            product.quantity = quantity
            self.save_products()
            messagebox.showinfo("Aktualisiert", "Produkt wurde erfolgreich aktualisiert.")
            self.seller_view()
        except Exception:
            messagebox.showerror("Fehler", "Ungültige Eingabe!")
            self.seller_view()

    # Produkt löschen
    def delete_product(self, index):
        if messagebox.askyesno("Löschen", "Möchten Sie dieses Produkt wirklich löschen?"):
            del self.products[index]
            self.save_products()
            self.seller_view()

    # Verkäufer abmelden
    def logout_seller(self):
        self.logged_in_seller = None
        self.main_menu()

    # Kundenbereich mit Produktübersicht
    def customer_view(self):
        self.clear_window()
        tk.Label(self.root, text="Kundenbereich - Produkte", font=self.label_font).pack(pady=15)

        frame = tk.Frame(self.root)
        frame.pack()

        # Produkte anzeigen mit Verfügbarkeitsstatus
        for idx, product in enumerate(self.products):
            status = f"{product.name} - {product.price:.2f} € - {product.quantity} Stück verfügbar"
            if product.quantity == 0:
                status = f"{product.name} - Ausverkauft"
            tk.Label(frame, text=status, font=("Arial", 14)).grid(row=idx, column=0, sticky='w', padx=10, pady=4)
            if product.quantity > 0:
                tk.Button(frame, text="In den Warenkorb", font=self.button_font, command=lambda p=product: self.add_to_cart(p)).grid(row=idx, column=1, padx=5)
            else:
                tk.Label(frame, text="Nicht verfügbar", fg="red", font=("Arial", 14, "bold")).grid(row=idx, column=1, padx=5)

        # Button zum Anzeigen des Warenkorbs und zur Rückkehr zum Hauptmenü
        tk.Button(self.root, text="🛒 Warenkorb anzeigen", font=self.button_font, bg="green", fg="white", command=self.show_cart).pack(pady=15)
        tk.Button(self.root, text="⬅ Zurück zum Hauptmenü", font=self.button_font, command=self.main_menu).pack(pady=8)

    # Produkt zum Warenkorb hinzufügen
    def add_to_cart(self, product):
        if product.quantity <= 0:
            messagebox.showwarning("Nicht verfügbar", "Dieses Produkt ist ausverkauft.")
            return
        self.cart.add(product)
        messagebox.showinfo("Hinzugefügt", f"'{product.name}' wurde zum Warenkorb hinzugefügt.")

    # Warenkorb anzeigen und zur Bezahlung weiterleiten
    def show_cart(self):
        if not self.cart.items:
            messagebox.showinfo("Warenkorb leer", "Sie haben noch keine Produkte hinzugefügt.")
            return

        cart_content = self.cart.list_items()
        total_price = self.cart.total()

        result = messagebox.askyesno("Warenkorb", f"{cart_content}\n\nGesamtsumme: {total_price:.2f} €\n\nMöchten Sie zur Bezahlung fortfahren?")

        if result:
            self.payment()

    # Bezahlvorgang mit Auswahl der Zahlungsmethode
    def payment(self):
        self.clear_window()
        tk.Label(self.root, text="Wählen Sie die Zahlungsmethode:", font=self.label_font).pack(pady=15)

        def choose_method(method):
            # Produkte im Warenkorb vom Lagerbestand abziehen
            for item in self.cart.items:
                for product in self.products:
                    if product.name == item.name:
                        if product.quantity < 1:
                            messagebox.showerror("Fehler", f"'{product.name}' ist nicht mehr verfügbar.")
                            self.customer_view()
                            return
                        product.quantity -= 1

            self.save_products()
            self.cart.clear()
            messagebox.showinfo("Bestellung abgeschlossen", f"🎉 Vielen Dank für Ihre Bestellung!\nZahlungsmethode: {method}")
            self.main_menu()

        # Buttons für Zahlungsmethoden anzeigen
        methods = ["Kreditkarte", "Banküberweisung", "PayPal"]
        for m in methods:
            tk.Button(self.root, text=m, font=self.button_font, width=25, command=lambda method=m: choose_method(method)).pack(pady=5)

        tk.Button(self.root, text="⬅ Abbrechen", font=self.button_font, width=25, command=self.customer_view).pack(pady=20)

# Programmstart
if __name__ == "__main__":
    root = tk.Tk()
    app = ShopApp(root)
    root.mainloop()
