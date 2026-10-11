{
    "name": "ONLYOFFICE — Créer un document",
    "version": "20.0.1.0.0",
    "category": "Productivity/Documents",
    "summary": "Créer un document Office vierge (Word, Excel, PowerPoint) et l'ouvrir dans ONLYOFFICE",
    "description": """
Comble le manque du connecteur ONLYOFFICE en édition Community : la création
de documents vierges (réservée à l'app Documents d'Odoo Enterprise).

Ajoute un assistant « Nouveau document » qui demande un type (docx/xlsx/pptx)
et un titre, crée une pièce jointe Office vierge et l'ouvre directement dans
l'éditeur ONLYOFFICE. Une vue « Mes documents » liste les fichiers créés.
    """,
    "author": "Benoît Vézina, Diverse-Cité",
    "website": "https://www.onlyoffice.com/office-for-odoo?utm_source=odoo_market",
    "license": "LGPL-3",
    "depends": ["onlyoffice_odoo"],
    "data": [
        "security/ir.access.csv",
        "wizards/onlyoffice_create_wizard_views.xml",
        "views/ir_attachment_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": False,
}
