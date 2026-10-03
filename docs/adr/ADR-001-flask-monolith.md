# ADR-001 — Monolithe Flask modulaire

## Contexte
WATO EVENTS doit couvrir site public, commerce, opérations et finance tout en restant simple à déployer sur PythonAnywhere.

## Décision
Utiliser un monolithe Flask modulaire dans une application unique et une base MySQL unique pour le MVP.

## Raisons
- simplicité d'exploitation ;
- transactions multi-domaines faciles ;
- faible coût opérationnel ;
- déploiement PythonAnywhere naturel ;
- équipe/projet encore de taille MVP.

## Conséquences
Les domaines sont séparés par Blueprints, modèles et services, mais partagent le même processus. Toute extraction future en service séparé devra être justifiée par un besoin réel.
