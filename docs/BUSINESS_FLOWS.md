# Flux métier — WATO EVENTS

## 1. Flux réel après PROMPT 4

```mermaid
flowchart LR
  V[Visiteur] --> C[Catalogue]
  C --> CFG[Configurateur]
  CFG --> EST[Estimation indicative]
  EST --> QR[QuoteRequest]
  QR --> REV[Revue interne]
  REV --> FUT[Flux futur]
  FUT --> P[Prospect]
  P --> Q[Quote officiel]
  Q --> O[Order]
  O --> E[Event si nécessaire]
```

## 2. Séparation fondamentale

### QuoteRequest
Expression entrante du besoin, accompagnée d'une estimation indicative et de snapshots du catalogue.

### Quote
Futur document commercial officiel, avec numéro DEV, validité, conditions et prix contractuels. Il n'est pas encore implémenté.

### Order
Futur engagement commercial confirmé.

### Event
Futur objet opérationnel de planification.

Une QuoteRequest ne doit jamais être présentée au visiteur comme un devis définitif.

## 3. Flux configurateur

1. informations événement ;
2. sélection Services / Menus / Packs ;
3. estimation indicative ;
4. budget et coordonnées ;
5. récapitulatif ;
6. recalcul serveur depuis le catalogue ;
7. création atomique QuoteRequest + QuoteRequestItem ;
8. confirmation publique limitée à la référence.

## 4. Prix et catalogue

Les valeurs envoyées par le navigateur ne sont jamais fiables. Au POST final, le serveur recharge les éléments actifs/publics puis PricingService recalcule.

Les QuoteRequestItem sont des snapshots : une modification ultérieure du catalogue n'altère pas une ancienne demande.

## 5. Administration

Le statut commence à NEW. L'administration minimale permet ensuite REVIEWING, CONTACTED, QUALIFIED, CONVERTED, REJECTED ou ARCHIVED.

Le passage CONVERTED n'implémente pas encore le CRM ni Quote : il s'agit uniquement d'un état préparatoire.
