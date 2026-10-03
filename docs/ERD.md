# ERD — WATO EVENTS

## Domaine réellement implémenté au PROMPT 3

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

  CATEGORY {
    int id PK
    string name
    string slug UK
    string category_type
    int display_order
    bool is_active
  }

  SERVICE {
    int id PK
    string name
    string slug UK
    decimal base_price
    string pricing_unit
    bool is_featured
    bool is_active
    bool is_public
    int display_order
  }

  DISH {
    int id PK
    int category_id FK
    string name
    string slug UK
    decimal base_price
    string pricing_unit
    bool is_featured
    bool is_active
    bool is_public
  }

  MENU {
    int id PK
    string name
    string slug UK
    decimal price
    string pricing_unit
    int minimum_people
    bool is_featured
    bool is_active
    bool is_public
  }

  MENU_ITEM {
    int id PK
    int menu_id FK
    int dish_id FK
    decimal quantity
    string section
    int display_order
    bool is_optional
  }

  PACK {
    int id PK
    string name
    string slug UK
    decimal price
    string pricing_unit
    int minimum_people
    bool is_featured
    bool is_active
    bool is_public
  }

  PACK_DISH {
    int pack_id FK
    int dish_id FK
    decimal quantity
    int display_order
  }

  PACK_MENU {
    int pack_id FK
    int menu_id FK
    decimal quantity
    int display_order
  }

  PACK_SERVICE {
    int pack_id FK
    int service_id FK
    decimal quantity
    int display_order
  }
```

## Domaines futurs

Les entités QuoteRequest, Quote, Order, Event, Payment, Invoice, Inventory, Equipment, Employee et autres restent conceptuelles et ne sont pas encore présentes dans la base.

Le futur `QuoteItem` pourra référencer une entité catalogue puis capturer un snapshot commercial sans dépendre du prix courant.
