# ONLYOFFICE — Créer un document

Ce module permet de créer un document Office vierge (Word, Excel ou PowerPoint) et de l'ouvrir aussitôt dans l'éditeur
ONLYOFFICE. Il complète le connecteur `onlyoffice_odoo` de l'édition Community, qui ne sait pas créer de document
vierge.

## Utilisation

- Le menu **ONLYOFFICE** est visible des utilisateurs internes.
- **ONLYOFFICE → Nouveau document** ouvre un assistant : choisir le type (`.docx`, `.xlsx` ou `.pptx`) et saisir un
  titre, puis cliquer **Créer et ouvrir**.
- L'assistant crée une pièce jointe vierge marquée « Créé via ONLYOFFICE ». L'extension est ajoutée au titre si elle
  manque. Le document s'ouvre dans un nouvel onglet, à l'adresse `/onlyoffice/editor/<id>` fournie par le connecteur.
- **ONLYOFFICE → Mes documents** liste les pièces jointes créées par l'assistant, filtrées par défaut sur celles de
  l'utilisateur. Le bouton **Ouvrir** relance l'éditeur. Un regroupement par créateur est disponible.

## Fonctionnement

Les fichiers vierges sont assemblés en mémoire (`utils.py`), sans dépendance externe : un paragraphe vide, une feuille «
Feuille1 » ou une diapositive vierge. L'enregistrement des modifications passe ensuite par le connecteur
`onlyoffice_odoo`.

## Configuration

Aucune configuration propre. Le serveur ONLYOFFICE se règle dans le connecteur `onlyoffice_odoo`.

## Accès et limites

- La liste ne permet ni de créer ni de modifier : la création passe par l'assistant.
- Les pièces jointes ne sont rattachées à aucun enregistrement. Les règles d'accès standard des pièces jointes d'Odoo
  s'appliquent.

## Dépendances et tests

Dépend de `onlyoffice_odoo`, du même dépôt. Le module n'a pas de tests.
