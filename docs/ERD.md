# ERD global — WATO EVENTS

Ce diagramme décrit le modèle relationnel cible. Il est volontairement lisible et n'affiche que les relations structurantes.

```mermaid
erDiagram
  USER ||--o| EMPLOYEE : "optional profile"
  CUSTOMER ||--o{ QUOTE : receives
  CUSTOMER ||--o{ ORDER : places
  CUSTOMER ||--o{ EVENT : owns
  PROSPECT ||--o{ QUOTE_REQUEST : submits
  PROSPECT ||--o{ QUOTE : receives

  EVENT_TYPE ||--o{ EVENT : classifies

  MENU ||--o{ MENU_ITEM : contains
  DISH ||--o{ MENU_ITEM : included
  PACK ||--o{ QUOTE_ITEM : referenced
  SERVICE ||--o{ QUOTE_ITEM : referenced
  DISH ||--o{ QUOTE_ITEM : referenced
  MENU ||--o{ QUOTE_ITEM : referenced

  QUOTE_REQUEST ||--o{ QUOTE : may_generate
  QUOTE ||--|{ QUOTE_ITEM : contains
  QUOTE ||--o| ORDER : accepted_as

  ORDER ||--|{ ORDER_ITEM : contains
  ORDER ||--o| EVENT : may_require
  EVENT ||--o{ PAYMENT : receives
  ORDER ||--o{ PAYMENT : receives
  EVENT ||--o{ INVOICE : billed
  ORDER ||--o{ INVOICE : billed

  SUPPLIER ||--o{ PURCHASE : supplies
  PURCHASE ||--|{ PURCHASE_ITEM : contains
  INGREDIENT ||--o{ PURCHASE_ITEM : purchased
  INGREDIENT ||--o{ STOCK_MOVEMENT : moves
  PURCHASE ||--o{ STOCK_MOVEMENT : generates
  EVENT ||--o{ STOCK_MOVEMENT : may_consume

  EVENT ||--o{ EQUIPMENT_RESERVATION : reserves
  EQUIPMENT ||--o{ EQUIPMENT_RESERVATION : allocated

  EVENT ||--o{ EVENT_ASSIGNMENT : staffs
  EMPLOYEE ||--o{ EVENT_ASSIGNMENT : assigned

  USER ||--o{ AUDIT_LOG : performs
  USER ||--o{ NOTIFICATION : receives

  BUSINESS_SETTINGS ||--o{ GALLERY_ITEM : contextualizes
```

## Clés et contraintes structurantes

Les PK utilisent des identifiants techniques internes. Les références commerciales restent séparées et uniques.

FK importantes :

- `Quote.customer_id` ou `Quote.prospect_id` selon le stade commercial ;
- `Quote.quote_request_id` optionnel ;
- `Order.quote_id` optionnel mais unique si une acceptation crée une seule commande ;
- `Event.order_id` optionnel et unique pour le MVP ;
- `Payment.event_id` / `Payment.order_id` selon le contexte ;
- `EquipmentReservation.event_id` et `equipment_id` ;
- `EventAssignment.event_id` et `employee_id` ;
- `StockMovement.ingredient_id` obligatoire.

Contraintes recommandées :

- références commerciales uniques ;
- quantité strictement positive sur lignes de vente/achat ;
- montant non négatif sauf lignes/mouvements explicitement signés ;
- dates de fin >= dates de début ;
- unicité logique sur certaines affectations événement/personnel ;
- index sur statuts, dates d'événements, FK, références commerciales et dates de création.
