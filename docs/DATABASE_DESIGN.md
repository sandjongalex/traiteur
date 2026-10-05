# Conception de base de données — DNP DECO

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


## Domaine authentification/RBAC

Migration `20261003_03_auth_rbac`, après `20261003_02_quote_requests`.

Tables : `users`, `roles`, `permissions`, `user_roles`, `role_permissions`, `audit_logs`.

Contraintes : email unique, role.code unique, permission.code unique, associations many-to-many uniques. Les FK d’association utilisent CASCADE ; AuditLog → User utilise SET NULL afin de préserver l’historique.


## Portabilité SQLite / MySQL

Moteurs supportés par la même couche SQLAlchemy :

- SQLite aujourd'hui ;
- MySQL/PyMySQL demain.

Les montants conservent `Decimal` + `NUMERIC`; aucun passage à `float` n'est autorisé. Les booléens, dates, FK, contraintes uniques et checks passent par SQLAlchemy/Alembic.

SQLite applique les FK uniquement si `PRAGMA foreign_keys=ON`; l'application l'active à chaque connexion SQLite. `busy_timeout` réduit certains échecs transitoires `database is locked`. WAL est activé par défaut pour les DB fichier et améliore la coexistence lectures/écriture, sans supprimer la limitation fondamentale d'un seul écrivain à la fois.

Les timestamps actuels sont écrits par l'application en UTC. Les colonnes `DateTime` restent portables ; elles doivent être interprétées comme UTC côté métier, les conversions d'affichage restant séparées.

`AuditLog.metadata_json` reste du texte JSON sérialisé et n'utilise aucune requête JSON spécifique à un moteur.

### Chaîne Alembic

`20261003_01_catalog → 20261003_02_quote_requests → 20261003_03_auth_rbac`

Aucune migration supplémentaire n'est nécessaire au PROMPT 5.5 car aucun changement de schéma métier n'est introduit.
