# ADR-005 — Argent en Decimal / NUMERIC

## Contexte
DNP DECO manipulera devis, acomptes, paiements, remises, taxes, coûts et marges.

## Décision
Utiliser `Decimal` en Python et `NUMERIC/DECIMAL` en base. Interdire `float` pour l'argent.

## Raisons
- précision déterministe ;
- calculs financiers fiables ;
- réduction des erreurs d'arrondi.

## Conséquences
Le PricingService centralisera les règles d'arrondi. Les tests financiers doivent comparer des Decimal et non des floats.
