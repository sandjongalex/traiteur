# WATO EVENTS

**Traiteur & Événementiel professionnel à Yaoundé, Cameroun**

> « Vos moments, notre savoir-faire. »

WATO EVENTS est une plateforme web mobile first réunissant site public, catalogue commercial et, progressivement, gestion opérationnelle.

## État du projet

- PROMPT 0 — Cadrage : **terminé**
- PROMPT 0.5 — Architecture globale : **terminé**
- PROMPT 1 — Fondations Flask + MySQL : **terminé**
- PROMPT 2 — Identité visuelle + site public : **terminé**
- PROMPT 3 — Catalogue métier : **terminé**
- Prochaine étape : **PROMPT 4 — Configurateur + demandes de devis**

## Catalogue métier

Le catalogue persistant comprend :

- catégories ;
- services ;
- plats ;
- menus ;
- composition Menu ↔ Plat ;
- packs ;
- composition Pack ↔ Plat/Menu/Service.

Les pages publiques utilisent désormais la base de données pour les éléments publiés.

Routes principales :

- `/services`
- `/services/<slug>`
- `/menus`
- `/menus/<slug>`
- `/packs`
- `/packs/<slug>`

Administration temporaire du catalogue :

- `/admin/catalogue`

La protection actuelle repose temporairement sur `WATO_CATALOG_ADMIN_KEY` tant que le système User/RBAC du PROMPT 5 n'existe pas.

## Installation

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

Copier `.env.example` vers `.env`, puis lancer les migrations :

```bash
flask --app run.py db upgrade
flask --app run.py run
```

## Tests

```bash
pytest
```

## Configuration catalogue

Variable temporaire d'accès admin :

```env
WATO_CATALOG_ADMIN_KEY=une-cle-secrete-locale
```

Ne jamais commiter la vraie valeur.

## Images catalogue

Formats acceptés :

- jpg
- jpeg
- png
- webp

Les fichiers sont renommés par UUID et stockés sous `app/static/uploads/catalog/`.

En absence d'image, `app/static/images/catalog-placeholder.svg` est utilisé.

## Prix

Unités :

- FIXED
- PER_PERSON
- PER_UNIT
- PER_HOUR
- ON_REQUEST

Les montants utilisent `Decimal` / `NUMERIC`. `ON_REQUEST` est affiché comme « Sur devis ».

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Catalogue](docs/CATALOG.md)
- [ERD réel](docs/ERD.md)
- [Conception DB](docs/DATABASE_DESIGN.md)
- [Design system](docs/DESIGN_SYSTEM.md)
- [Sécurité](docs/SECURITY.md)
- [Tests](docs/TEST_STRATEGY.md)
- [Roadmap](docs/ROADMAP.md)

## Prochaine étape

**PROMPT 4 — CONFIGURATEUR + DEMANDES DE DEVIS**
