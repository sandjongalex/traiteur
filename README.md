# WATO EVENTS

**Traiteur & Événementiel professionnel à Yaoundé, Cameroun**

> « Vos moments, notre savoir-faire. »

WATO EVENTS est une plateforme web mobile first réunissant site public, catalogue commercial et gestion progressive des demandes événementielles.

## État du projet

- PROMPT 0 — Cadrage : **terminé**
- PROMPT 0.5 — Architecture globale : **terminé**
- PROMPT 1 — Fondations Flask + MySQL : **terminé**
- PROMPT 2 — Identité visuelle + site public : **terminé**
- PROMPT 3 — Catalogue métier : **terminé**
- PROMPT 4 — Configurateur + demandes de devis : **terminé**
- Prochaine étape : **PROMPT 5 — Authentification + back-office + RBAC**

## Configurateur public

Route principale :

`/demande-de-devis`

Le parcours collecte événement, invités, prestations, budget et coordonnées, puis affiche un récapitulatif avant envoi.

Une demande enregistrée reçoit une référence :

`DEM-AAAA-000001`

Cette référence appartient à `QuoteRequest` et ne doit pas être confondue avec un futur devis officiel `DEV-...`.

## Estimation

`PricingService` recharge les éléments publiés depuis la base et calcule avec `Decimal` :

- FIXED ;
- PER_PERSON ;
- PER_UNIT ;
- PER_HOUR ;
- ON_REQUEST.

Le prix envoyé par le navigateur n'est jamais utilisé comme source de vérité.

## Administration temporaire

- catalogue : `/admin/catalogue`
- demandes : `/admin/demandes-de-devis`

Les deux utilisent temporairement la même protection `WATO_CATALOG_ADMIN_KEY`. Le PROMPT 5 doit remplacer ce mécanisme par User/Role/Permission/Flask-Login.

## Installation

```bash
python -m venv .venv
pip install -r requirements.txt
flask --app run.py db upgrade
flask --app run.py run
```

## Tests

```bash
pytest
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Catalogue](docs/CATALOG.md)
- [Demandes de devis](docs/QUOTE_REQUESTS.md)
- [ERD](docs/ERD.md)
- [Flux métier](docs/BUSINESS_FLOWS.md)
- [Conception DB](docs/DATABASE_DESIGN.md)
- [Sécurité](docs/SECURITY.md)
- [Tests](docs/TEST_STRATEGY.md)
- [Roadmap](docs/ROADMAP.md)

## Prochaine étape

**PROMPT 5 — AUTHENTIFICATION + BACK-OFFICE + RBAC**
