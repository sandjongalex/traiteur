# Catalogue métier — DNP DECO

## 1. Périmètre implémenté

Le PROMPT 3 introduit le premier domaine métier persistant de DNP DECO.

Entités réellement implémentées :

- Category
- Service
- Dish
- Menu
- MenuItem
- Pack
- PackDish
- PackMenu
- PackService

Le catalogue alimente désormais le site public et dispose d'un back-office minimal protégé.

## 2. Décision Category

Une table générique `Category` avec `category_type` a été retenue.

Types supportés :

- DISH
- SERVICE
- MENU
- PACK

Motif : garder une structure simple et extensible sans créer plusieurs tables de catégorie presque identiques. Pour le moment, la relation physique est surtout utilisée par `Dish.category_id`; les autres types restent prêts pour une extension future sans obliger l'application à les exploiter prématurément.

## 3. Pricing units

Enum applicatif centralisé :

- FIXED
- PER_PERSON
- PER_UNIT
- PER_HOUR
- ON_REQUEST

Les prix utilisent `Decimal` en Python et `NUMERIC(14,2)` en base.

`ON_REQUEST` implique un prix nul autorisé et un affichage public « Sur devis », jamais « 0 FCFA ».

## 4. Publication

Les éléments vendables distinguent :

- `is_active` : utilisable dans l'application ;
- `is_public` : visible sur le site public ;
- `is_featured` : mis en avant ;
- `display_order` : ordre de présentation.

Le public filtre systématiquement `is_active=True` et `is_public=True`.

## 5. Slugs

Les slugs sont générés côté serveur via `app/utils/catalog.py`.

Principes :

- normalisation sans accent ;
- minuscules ;
- tirets ;
- unicité par type d'entité ;
- suffixes automatiques en cas de doublon.

Les pages publiques détaillées utilisent les slugs.

## 6. Menus

`MenuItem` est une vraie table d'association entre Menu et Dish.

Elle porte :

- quantity ;
- section ;
- display_order ;
- is_optional.

La suppression d'un Menu supprime ses MenuItem compositifs, mais la suppression d'un Dish référencé est bloquée par FK `RESTRICT`.

## 7. Packs

Le choix retenu est volontairement **non polymorphique** :

- PackDish ;
- PackMenu ;
- PackService.

Cette approche crée plus de tables mais apporte :

- intégrité référentielle SQL ;
- relations SQLAlchemy explicites ;
- migrations lisibles ;
- requêtes simples ;
- meilleure maintenabilité pour le MVP.

Les futurs modules Employee/Equipment ne sont pas anticipés ici.

## 8. Images

Chaque Service, Dish, Menu et Pack possède un `image_path` optionnel.

Uploads catalogue :

- jpg/jpeg/png/webp ;
- extension contrôlée ;
- MIME contrôlé ;
- `secure_filename` utilisé sur le nom entrant ;
- nom final remplacé par UUID ;
- stockage sous `uploads/catalog/`.

En absence d'image, le site public utilise `images/catalog-placeholder.svg`.

## 9. Back-office

Préfixe :

`/admin/catalogue`

Fonctions disponibles :

- dashboard ;
- listes catégories/services/plats/menus/packs ;
- création ;
- édition ;
- activation/désactivation ;
- publication/dépublication ;
- featured ;
- composition Menu ↔ Dish ;
- composition Pack ↔ Dish/Menu/Service.

Comme User/RBAC n'existe pas encore, une protection temporaire minimale repose sur `WATO_CATALOG_ADMIN_KEY`.

Cette clé est uniquement une barrière transitoire jusqu'au PROMPT 5. Elle ne doit pas être considérée comme le futur système d'authentification.

## 10. Site public

Pages alimentées par la DB :

- `/services`
- `/services/<slug>`
- `/menus`
- `/menus/<slug>`
- `/packs`
- `/packs/<slug>`
- accueil pour les éléments featured.

Lorsque la DB est vide, les pages affichent des états vides propres et l'accueil conserve son contenu éditorial temporaire pour éviter une page cassée.

## 11. Migration

Révision :

`20261003_01_catalog`

Tables :

- catalog_categories
- catalog_services
- catalog_dishes
- catalog_menus
- catalog_menu_items
- catalog_packs
- catalog_pack_dishes
- catalog_pack_menus
- catalog_pack_services

Contraintes DB couvrent notamment slugs uniques, prix non négatifs, minimum_people positif, quantités positives et display_order non négatif.

## 12. Tests

Les tests catalogue couvrent :

- Decimal ;
- slugs uniques ;
- relations Menu/Dish ;
- relations Pack ;
- publication publique ;
- featured ;
- états vides ;
- protection admin ;
- création/toggle admin ;
- sécurité upload.

Les tests utilisent `db.create_all()` uniquement dans l'environnement de test en mémoire. Les évolutions de production restent exclusivement gérées par Alembic.
