# ADR-007 — Séparation Commande / Événement

## Contexte
WATO EVENTS peut exécuter une simple livraison de repas ou une prestation complexe comme un mariage avec personnel et matériel.

## Décision
`Order` et `Event` sont deux entités distinctes. Une commande peut exister sans événement ; un événement peut être rattaché à une commande.

## Raisons
- éviter de surcharger les livraisons simples ;
- isoler la planification logistique ;
- conserver un engagement commercial clair ;
- éviter la duplication des données de vente.

## Conséquences
Les lignes et montants commerciaux résident côté commande/devis. L'événement référence l'exécution opérationnelle et ne duplique pas le catalogue vendu.
