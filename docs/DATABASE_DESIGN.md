# Conception de base de données — WATO EVENTS

## 1. Principes

MySQL en production, SQLAlchemy comme ORM et Alembic/Flask-Migrate pour toute évolution.

Conventions :

- PK technique `id` ;
- FK explicites ;
- `created_at`, `updated_at` lorsque pertinent ;
- `created_by` pour les objets sensibles ;
- montants en `NUMERIC/DECIMAL` ;
- enums applicatifs ou colonnes de statut validées ;
- index sur relations, statuts, dates et recherches fréquentes.

## 2. Entités cibles

### Identité et sécurité
- User
- Role
- Permission
- AuditLog

### Configuration
- BusinessSettings

### CRM
- Prospect
- Customer

### Catalogue
- EventType
- Service
- Dish
- Menu
- MenuItem
- Pack

### Commerce
- QuoteRequest
- Quote
- QuoteItem
- Order
- OrderItem

### Opérations
- Event
- Employee
- EventAssignment
- Equipment
- EquipmentReservation

### Finance
- Payment
- Invoice
- InvoiceItem

### Approvisionnement
- Ingredient
- StockMovement
- Supplier
- Purchase
- PurchaseItem

### Contenu / communication
- GalleryItem
- Notification

## 3. Snapshots commerciaux

Les lignes de devis, commande et facture conservent les données commerciales utilisées au moment de l'émission :

- description ;
- type d'élément ;
- quantité ;
- unité ;
- prix unitaire ;
- remise ;
- taxe ;
- total.

Une modification future du catalogue ne doit pas altérer un document historique.

## 4. Argent

Exemple recommandé : `NUMERIC(14, 2)` pour les montants génériques, même si XAF est généralement sans décimales dans l'usage. Cela évite d'enfermer le système dans une hypothèse de devise.

Python : `Decimal` uniquement.

## 5. Stock

`StockMovement` contient au minimum :

- ingredient_id ;
- type ;
- quantity_delta ;
- unit_cost optionnel ;
- source_type/source_id ou références explicites ;
- occurred_at ;
- created_by ;
- note.

Le stock théorique est la somme des mouvements signés.

## 6. Réservations matériel

`EquipmentReservation` contient :

- event_id ;
- equipment_id ;
- quantity ;
- starts_at ;
- ends_at ;
- status.

Index composite recommandé sur `equipment_id, starts_at, ends_at, status`.

## 7. Affectations personnel

`EventAssignment` contient :

- event_id ;
- employee_id ;
- mission ;
- starts_at ;
- ends_at ;
- cost ;
- status.

La disponibilité est contrôlée par chevauchement temporel.

## 8. Numérotation commerciale

Prévoir une petite table de séquences métier :

- document_type ;
- year ;
- last_value.

Contrainte unique `(document_type, year)`. Incrément sous transaction/verrou afin d'éviter les collisions.

## 9. Archivage

Préférer `archived_at` ou statuts terminaux pour les données métier ayant une histoire. Les paiements, factures, mouvements de stock et audits sont immuables ou corrigés par opérations compensatoires.

## 10. Index prioritaires

- User.email / username ;
- Customer.phone, email ;
- Prospect.phone, email ;
- Quote.reference, status, valid_until ;
- Order.reference, status ;
- Event.reference, event_date, status ;
- Payment.created_at/status ;
- Invoice.reference/status ;
- StockMovement.ingredient_id + occurred_at ;
- Purchase.supplier_id + date ;
- EquipmentReservation.equipment_id + fenêtre ;
- EventAssignment.employee_id + fenêtre.
