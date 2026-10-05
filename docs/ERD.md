# ERD — DNP DECO

## Domaines réellement implémentés après PROMPT 4

```mermaid
erDiagram
  CATEGORY ||--o{ DISH : classifies
  MENU ||--o{ MENU_ITEM : contains
  DISH ||--o{ MENU_ITEM : included
  PACK ||--o{ PACK_DISH : contains
  DISH ||--o{ PACK_DISH : included
  PACK ||--o{ PACK_MENU : contains
  MENU ||--o{ PACK_MENU : included
  PACK ||--o{ PACK_SERVICE : contains
  SERVICE ||--o{ PACK_SERVICE : included

  QUOTE_REQUEST_SEQUENCE {
    int id PK
    int year UK
    int last_value
  }

  QUOTE_REQUEST ||--o{ QUOTE_REQUEST_ITEM : contains

  QUOTE_REQUEST {
    int id PK
    string reference UK
    string public_token UK
    string submission_token UK
    string status
    string source
    string customer_name
    string phone
    string whatsapp
    string email
    string event_type
    date event_date
    time event_time
    string location
    int guest_count
    decimal budget_min
    decimal budget_max
    decimal estimated_total
    bool has_on_request_items
    string currency
  }

  QUOTE_REQUEST_ITEM {
    int id PK
    int quote_request_id FK
    string item_type
    int item_id
    string label_snapshot
    decimal quantity
    decimal unit_price_snapshot
    string pricing_unit_snapshot
    decimal estimated_subtotal
  }
```

## Référence catalogue dans QuoteRequestItem

`item_type + item_id` identifie l'élément catalogue sélectionné, sans FK polymorphique. Les snapshots conservent le libellé, le prix et l'unité utilisés au moment de la demande.

## Non implémenté

`Quote`, `QuoteItem`, `Prospect`, `Customer`, `Order`, `Event`, `Payment` et les domaines opérationnels restent futurs.


## Authentification/RBAC — implémenté au PROMPT 5

```mermaid
erDiagram
 USER }o--o{ ROLE : user_roles
 ROLE }o--o{ PERMISSION : role_permissions
 USER ||--o{ AUDIT_LOG : produces
 USER { int id PK
 string email UK
 string password_hash
 bool is_active
 bool must_change_password
 }
 ROLE { int id PK
 string code UK
 bool is_system
 bool is_active
 }
 PERMISSION { int id PK
 string code UK
 }
 AUDIT_LOG { int id PK
 int user_id FK
 string action
 string resource_type
 string resource_id
 datetime created_at
 }
```

User est un compte d’accès applicatif. **User ≠ Employee** ; Employee reste futur au PROMPT 12.
