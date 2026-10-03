# WATO EVENTS

**Traiteur & Événementiel professionnel à Yaoundé, Cameroun**

> « Vos moments, notre savoir-faire. »

WATO EVENTS est une plateforme web **mobile first** réunissant site public, acquisition commerciale et gestion opérationnelle.

## État du projet

- PROMPT 0 — Cadrage : **terminé**
- PROMPT 0.5 — Architecture globale : **terminé**
- PROMPT 1 — Fondations Flask + MySQL : **terminé**
- PROMPT 2 — Identité visuelle + site public : **terminé**
- Prochaine étape : **PROMPT 3 — Services + menus + plats + packs**

## Pages publiques

- `/` — Accueil
- `/a-propos`
- `/services`
- `/menus`
- `/realisations`
- `/contact`
- `/demande-de-devis`
- `/health`

Les pages publiques reposent sur des données éditoriales temporaires centralisées dans `app/presentation.py`. Aucun modèle SQLAlchemy de catalogue n'a été créé au PROMPT 2.

## Stack

- Python / Flask
- MySQL en production
- SQLAlchemy
- Flask-Migrate / Alembic
- Jinja2
- HTML5 / CSS / JavaScript
- PythonAnywhere

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

## Assets publics

- CSS : `app/static/css/`
- JavaScript : `app/static/js/`
- images temporaires : `app/static/images/`
- templates : `app/templates/`

Les SVG actuels sont des placeholders. Remplacez-les par les photographies professionnelles WATO EVENTS en conservant les noms ou en mettant à jour les références centralisées.

## Logo

Le wordmark/monogramme actuel est temporaire. Un futur `logo.svg` ou `logo.png` pourra remplacer facilement le composant de marque.

## Contact et WhatsApp

Les coordonnées sont centralisées par variables d'environnement :

- `WATO_PHONE`
- `WATO_WHATSAPP`
- `WATO_EMAIL`
- `WATO_ADDRESS`
- URLs sociales optionnelles.

Si une valeur n'est pas configurée, elle n'est pas affichée et aucun faux contact n'est généré.

## Documentation

- [Vision](docs/VISION.md)
- [Architecture globale](docs/ARCHITECTURE.md)
- [Design system](docs/DESIGN_SYSTEM.md)
- [ERD](docs/ERD.md)
- [Flux métier](docs/BUSINESS_FLOWS.md)
- [Conception DB](docs/DATABASE_DESIGN.md)
- [RBAC](docs/RBAC.md)
- [Sécurité](docs/SECURITY.md)
- [Stratégie de tests](docs/TEST_STRATEGY.md)
- [PythonAnywhere](docs/PYTHONANYWHERE.md)
- [Roadmap](docs/ROADMAP.md)

## Prochaine étape

**PROMPT 3 — SERVICES + MENUS + PLATS + PACKS**

Ne pas démarrer les prompts suivants par anticipation.
