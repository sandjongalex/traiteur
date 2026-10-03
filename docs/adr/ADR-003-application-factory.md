# ADR-003 — Application Factory

## Contexte
L'application doit supporter plusieurs environnements, les tests et une croissance modulaire.

## Décision
Conserver `create_app()` comme point de construction de l'application et initialiser les extensions séparément.

## Raisons
- testabilité ;
- configuration par environnement ;
- absence d'état global prématuré ;
- enregistrement progressif des Blueprints.

## Conséquences
Tout nouveau module Flask doit s'intégrer via la factory ou un mécanisme appelé par elle, sans créer une seconde application globale concurrente.
