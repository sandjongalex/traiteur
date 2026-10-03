# Conception de base de données — WATO EVENTS

## 1. Principes

MySQL en production, SQLAlchemy comme ORM et Alembic/Flask-Migrate pour toute évolution.

Conventions :

- PK technique `id` ;
- FK explicites ;
- timestamps `created_at`, `updated_at` ;
- montants `NUMERIC/DECIMAL` ;
- contraintes DB pour l'intégrité ;
- index sur relations et filtres publics.

## 2. Domaine catalogue implémenté

### catalog_categories
Catégories typées via `category_type` : DISH, SERVICE, MENU, PACK.

### catalog_services
Prestations vendables avec prix optionnel, pricing_unit, publication et mise en avant.

### catalog_dishes
Plats vendables, catégorie optionnelle et mêmes contrôles de publication.

### catalog_menus
Compositions culinaires avec prix, unité de tarification et minimum de personnes.

### catalog_menu_items
Association Menu ↔ Dish avec quantité, section, ordre et caractère optionnel.

### catalog_packs
Offres groupées avec prix, minimum de personnes et publication.

### catalog_pack_dishes / catalog_pack_menus / catalog_pack_services
Associations explicites du contenu d'un pack.

## 3. Argent

Catalogue :

- Python : `Decimal` ;
- SQL : `NUMERIC(14,2)` ;
- quantités d'association : `NUMERIC(10,2)`.

Aucun `float`.

## 4. Contraintes importantes

- slug unique par table ;
- prix >= 0 ou NULL ;
- display_order >= 0 ;
- minimum_people > 0 ou NULL ;
- quantity > 0 ;
- pricing_unit limité aux valeurs supportées ;
- category_type limité aux valeurs supportées.

## 5. Cascades

- Menu → MenuItem : `CASCADE` car MenuItem est une composition interne du Menu ;
- Pack → associations : `CASCADE` pour la même raison ;
- Dish/Menu/Service référencés depuis associations : `RESTRICT` afin d'éviter une suppression accidentelle de l'élément source ;
- Category → Dish : `RESTRICT`.

Les offres métier sont destinées à être désactivées/dépubliées plutôt que supprimées.

## 6. Performance

Les listes publiques Menu/Pack utilisent `selectinload` pour éviter les N+1 sur leurs compositions.

Les index publics combinent notamment :

`is_active, is_public, display_order`.

## 7. Évolution future

QuoteItem n'existe pas encore. Il devra capturer un snapshot de label, quantité, prix unitaire, remise, taxe et total afin qu'un changement du catalogue ne modifie jamais un devis historique.
