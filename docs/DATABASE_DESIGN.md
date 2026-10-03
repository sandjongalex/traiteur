# Conception de base de données — WATO EVENTS

## Principes

MySQL en production, SQLAlchemy comme ORM et Alembic/Flask-Migrate pour toute évolution. Les montants utilisent Decimal / NUMERIC et les invariants essentiels sont protégés côté DB.

## Domaine catalogue

Tables existantes :

- catalog_categories
- catalog_services
- catalog_dishes
- catalog_menus
- catalog_menu_items
- catalog_packs
- catalog_pack_dishes
- catalog_pack_menus
- catalog_pack_services

## Domaine QuoteRequest

### quote_request_sequences

Compteur annuel des références DEM.

Contrainte unique : `year`.

### quote_requests

Contient notamment :

- reference unique ;
- public_token unique ;
- submission_token unique ;
- status / source contrôlés ;
- coordonnées ;
- événement ;
- budget ;
- estimation ;
- devise ;
- timestamps.

Contraintes :

- guest_count > 0 ;
- budgets >= 0 ;
- budget_max >= budget_min ;
- estimated_total >= 0.

Index principaux : statut+création, event_date, phone, email.

### quote_request_items

Snapshot de la sélection au moment de l'envoi :

- item_type ;
- item_id ;
- label_snapshot ;
- quantity ;
- unit_price_snapshot ;
- pricing_unit_snapshot ;
- estimated_subtotal.

`item_type + item_id` n'est pas une FK polymorphique : l'intégrité de disponibilité est validée par PricingService à la création, tandis que le snapshot garantit l'historique.

FK `quote_request_id` utilise CASCADE car les items sont constitutifs de la demande. L'interface standard ne propose toutefois aucun hard delete de QuoteRequest.

## Migration

Chaîne actuelle :

`20261003_01_catalog → 20261003_02_quote_requests`

Aucune branche Alembic parallèle.

## Argent

- prix : NUMERIC(14,2) ;
- quantités snapshot : NUMERIC(12,2) ;
- Python : Decimal uniquement.

## Évolution future

QuoteRequest pourra être relié ultérieurement à Prospect/Customer puis à Quote, sans modifier ses snapshots historiques.
