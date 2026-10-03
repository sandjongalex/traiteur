# ADR-006 — Stock basé sur un ledger

## Contexte
Les achats, consommations, pertes, retours et inventaires doivent être traçables.

## Décision
La source de vérité du stock est `StockMovement`, jamais une simple décrémentation silencieuse de quantité.

## Raisons
- auditabilité ;
- reconstitution historique ;
- corrections explicites ;
- rapports pertes/consommation ;
- meilleure investigation des écarts.

## Conséquences
Toute variation de stock crée un mouvement. Un solde matérialisé éventuel n'est qu'un cache réconciliable avec le ledger.
