# WATO EVENTS

**Traiteur & Événementiel professionnel à Yaoundé, Cameroun**

> « Vos moments, notre savoir-faire. »

WATO EVENTS est une plateforme web **mobile first** destinée à réunir progressivement le site public, l'acquisition commerciale et la gestion opérationnelle de l'activité.

## État du projet

Le dépôt est actuellement au stade **PROMPT 1 — Fondations Flask + MySQL**.

Le socle technique est installé :

- application factory Flask `create_app()` ;
- configuration développement / test / production ;
- SQLAlchemy ;
- Flask-Migrate / Alembic ;
- MySQL via PyMySQL ;
- protection CSRF ;
- Blueprint public minimal ;
- route `/health` ;
- commande `flask db-check` ;
- tests pytest.

Les modules métier (CRM, devis, événements, paiements, stocks, matériel, personnel, etc.) ne sont pas encore implémentés.

## Stack

- Python / Flask
- MySQL en production
- SQLAlchemy
- Flask-Migrate / Alembic
- Jinja2
- HTML5 / CSS / JavaScript
- Bootstrap 5
- Déploiement cible : PythonAnywhere

## Installation locale

```bash
python -m venv .venv
pip install -r requirements.txt
```

Activation sous Linux/macOS :

```bash
source .venv/bin/activate
```

Activation sous Windows :

```powershell
.venv\Scripts\activate
```

Copier ensuite `.env.example` vers `.env`, puis lancer :

```bash
flask --app run.py run
```

## Tests

```bash
pytest
```

## Vérification MySQL

Avec un `DATABASE_URL` valide :

```bash
flask --app run.py db-check
```

## Documentation

- [Vision](docs/VISION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Fonctionnalités](docs/FONCTIONNALITES.md)
- [Roadmap](docs/ROADMAP.md)
- [Conventions](docs/CONVENTIONS.md)
- [Fondations Flask + MySQL](docs/FOUNDATIONS.md)

## Prochaine étape

**PROMPT 2 — IDENTITÉ VISUELLE + SITE PUBLIC**

Cette étape ne doit pas être démarrée automatiquement.
