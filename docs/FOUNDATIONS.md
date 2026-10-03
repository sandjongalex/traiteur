# Fondations Flask + MySQL

## Objectif

Le PROMPT 1 transforme le cadrage documentaire en socle Flask exécutable sans implémenter les modules métier futurs.

## Composants installés

- application factory `create_app()` ;
- configuration développement / test / production ;
- SQLAlchemy ;
- Flask-Migrate / Alembic ;
- support MySQL via PyMySQL ;
- protection CSRF ;
- Blueprint public minimal ;
- route de santé `/health` ;
- commande `flask db-check` ;
- base de tests pytest.

## Environnements

La variable `APP_ENV` accepte `development`, `testing` ou `production`.

En développement, SQLite local permet un démarrage sans serveur MySQL. En production, `SECRET_KEY` et `DATABASE_URL` sont obligatoires.

Exemple MySQL :

```env
DATABASE_URL=mysql+pymysql://user:password@host/database
```

## Démarrage local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app run.py run
```

Sous Windows :

```powershell
.venv\Scripts\activate
```

## Vérification de la base

```bash
flask --app run.py db-check
```

## Migrations

```bash
flask --app run.py db migrate -m "description"
flask --app run.py db upgrade
```

`db.create_all()` ne doit pas être utilisé comme stratégie d'évolution du schéma en production.

## Tests

```bash
pytest
```

Les tests utilisent SQLite en mémoire.

## Limites volontaires

Aucun modèle métier complet n'est créé au PROMPT 1. Les domaines devis, événements, paiements, stocks, matériel, personnel, CRM et authentification restent réservés aux prompts suivants.
