# ADR-002 — MySQL en production

## Contexte
La plateforme doit fonctionner sur PythonAnywhere avec persistance relationnelle, contraintes, transactions et migrations.

## Décision
MySQL est la base de production. SQLAlchemy est l'ORM et Alembic/Flask-Migrate gère le schéma.

## Raisons
- support natif PythonAnywhere ;
- modèle relationnel adapté aux domaines WATO EVENTS ;
- transactions ;
- contraintes et index ;
- écosystème Flask mature.

## Conséquences
Les fonctionnalités critiques doivent être vérifiées sur MySQL avant production, même si SQLite mémoire reste utile pour certains tests rapides.
