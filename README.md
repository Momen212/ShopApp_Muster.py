# ShopApp_Muster.py

Elektronischer Shop – Python GUI Projekt (mit tkinter)

Funktionen:
- Verkäufer können sich registrieren, einloggen und Produkte verwalten.
- Kunden können Produkte sehen, in den Warenkorb legen und die Zahlungsmethode wählen.
- Produkte und Verkäufer werden dauerhaft in JSON-Dateien gespeichert.
- GUI mit tkinter: Buttons und einfache Dialoge.

Verkäufer:
- Registrierung/Login mit Name und Passwort.
- Produkte hinzufügen, bearbeiten und löschen.
- Produkte werden in 'produkte.json' gespeichert.

Kunden:
- Sehen verfügbare Produkte (inkl. Lagerbestand).
- Kaufen mit verschiedenen Zahlungsmethoden (Kreditkarte, PayPal etc.).
- Warenkorb zeigt Gesamtpreis, Mengenprüfung inklusive.

Technik:
- Objektorientierte Programmierung (Product, Seller, ShoppingCart, ShopApp)
- JSON für Datenhaltung
- Dynamische GUI mit klaren Benutzerpfaden
