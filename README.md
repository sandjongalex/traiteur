# WATO EVENTS

**Traiteur & Événementiel professionnel à Yaoundé, Cameroun**

> « Vos moments, notre savoir-faire. »

WATO EVENTS est une plateforme web **mobile first** réunissant progressivement site public, acquisition commerciale et gestion opérationnelle.

## État du projet

- PROMPT 0 — Cadrage : **terminé**
- PROMPT 0.5 — Architecture globale : **terminé**
- PROMPT 1 — Fondations Flask + MySQL : **terminé**
- Prochaine étape : **PROMPT 2 — Identité visuelle + site public**

Aucun module métier complet (devis, CRM, événements, paiements, stocks, matériel, personnel) n'est encore implémenté.

## Stack

- Python / Flask
- MySQL en production
- SQLAlchemy
- Flask-Migrate / Alembic
- Jinja2
- HTML5 / CSS / JavaScript
- Bootstrap 5
- PythonAnywhere

## Fondations existantes

- application factory `create_app()` ;
- configuration développement/test/production ;
- SQLAlchemy et migrations ;
- PyMySQL ;
- CSRF ;
- Blueprint public minimal ;
- `/health` ;
- commande `flask db-check` ;
- tests pytest de base.

## Installation locale

```bash
python -m venv .venv
pip install -r requirements.txt
```

Activation Linux/macOS :

```bash
source .venv/bin/activate
```

Activation Windows :

```powershell
.venv\Scripts\activate
```

Copier `.env.example` vers `.env`, puis :

```bash
flask --app run.py run
```

## Tests

```bash
pytest
```

## Documentation

- [Vision](docs/VISION.md)
- [Architecture globale](docs/ARCHITECTURE.md)
- [ERD](docs/ERD.md)
- [Flux métier](docs/BUSINESS_FLOWS.md)
- [Conception DB](docs/DATABASE_DESIGN.md)
- [RBAC](docs/RBAC.md)
- [Sécurité](docs/SECURITY.md)
- [Stratégie de tests](docs/TEST_STRATEGY.md)
- [PythonAnywhere](docs/PYTHONANYWHERE.md)
- [Fonctionnalités](docs/FONCTIONNALITES.md)
- [Conventions](docs/CONVENTIONS.md)
- [Fondations](docs/FOUNDATIONS.md)
- [Roadmap](docs/ROADMAP.md)
- [ADR](docs/adr/)

## Architecture

Le MVP suit un **monolithe Flask modulaire**. La structure métier cible est documentée mais sera créée progressivement, domaine par domaine.

## Prochaine étape

**PROMPT 2 — IDENTITÉ VISUELLE + SITE PUBLIC**

Ne pas démarrer les modules métier des prompts suivants par anticipation.
