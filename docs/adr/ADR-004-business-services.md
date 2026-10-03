# ADR-004 — Services métier

## Contexte
Les règles de devis, prix, paiement, stock, événement et réservation seront trop importantes pour être placées dans les routes.

## Décision
La logique métier est portée par des services explicites. Les routes gèrent HTTP et délèguent.

## Raisons
- tests indépendants ;
- réutilisation ;
- transactions cohérentes ;
- réduction de la duplication ;
- séparation interface / métier.

## Conséquences
Une route ne doit pas contenir un calcul financier complexe ni orchestrer directement plusieurs écritures DB critiques.
