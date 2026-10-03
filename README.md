# WATO EVENTS

**Traiteur & Événementiel professionnel à Yaoundé, Cameroun**

> « Vos moments, notre savoir-faire. »

WATO EVENTS est un projet de plateforme web **mobile first** réunissant progressivement :

- un site public orienté acquisition, conversion et demandes de devis ;
- un back-office de gestion commerciale et opérationnelle ;
- les futurs modules clients, événements, devis, commandes, paiements, stocks, fournisseurs, matériel, personnel et rapports.

## État du projet

Le dépôt est actuellement en **PROMPT 0 — Cadrage maître**.

Cette étape pose uniquement les fondations documentaires et les conventions. Les modules métier complets ne sont pas encore implémentés.

## Stack cible

- Python / Flask
- MySQL en production
- SQLAlchemy
- Flask-Migrate / Alembic
- Jinja2
- HTML5 / CSS / JavaScript
- Bootstrap 5
- Déploiement cible : PythonAnywhere

## Principes structurants

- Application Flask avec `create_app()` et Blueprints.
- Architecture mobile first.
- Contrôle d'accès serveur avec RBAC extensible.
- Migrations obligatoires pour l'évolution de la base.
- Montants financiers en `Decimal` / `NUMERIC`, jamais en `float`.
- Mouvements de stock traçables, sans modification silencieuse des quantités.
- Paiements fractionnés : un paiement existant ne signifie pas qu'un événement est soldé.
- Configuration centralisée des coordonnées, du WhatsApp, de la devise et des conditions commerciales.
- Aucun secret réel commité.
- Développement incrémental par prompts/sprints.

## Documentation

- [Vision](docs/VISION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Fonctionnalités](docs/FONCTIONNALITES.md)
- [Roadmap](docs/ROADMAP.md)
- [Conventions](docs/CONVENTIONS.md)

## Roadmap

Le développement suivra des sprints successifs, du cadrage jusqu'au déploiement PythonAnywhere. Le détail est disponible dans [docs/ROADMAP.md](docs/ROADMAP.md).

**Prochaine étape prévue : PROMPT 1 — FONDATIONS FLASK + MYSQL.**

Le PROMPT 1 ne doit pas être lancé automatiquement depuis cette étape.
