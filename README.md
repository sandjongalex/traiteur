# WATO EVENTS

Plateforme Flask/SQLAlchemy mobile-first pour WATO EVENTS — Traiteur & Événementiel à Yaoundé.

## État
PROMPT 0 à 5 : **terminés**.  
PROMPT 5.5 — SQLite + environnement PythonAnywhere gratuit : **terminé côté code/documentation**.  
PROMPT 5.6 — Refonte UI/UX premium + design system : **implémenté côté code/documentation**.

Prochaine étape : **VALIDATION VISUELLE ET FONCTIONNELLE DE WATO EVENTS**.

## Base de données

Le code métier reste indépendant du moteur :

```text
WATO EVENTS
   ↓
SQLAlchemy
   ├─ SQLite — environnement actuel / PythonAnywhere gratuit
   └─ MySQL  — cible future lorsque la concurrence augmente
```

En développement, sans `DATABASE_URL`, l'application utilise automatiquement :

`instance/wato_events.db`

La base est hors `static/` et les fichiers `*.db`, `*.sqlite`, `*.sqlite3` sont ignorés par Git.

### Développement rapide avec SQLite

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export APP_ENV=development
flask --app run.py db upgrade
flask --app run.py seed-rbac
flask --app run.py create-superadmin
flask --app run.py run
```

## Back-office sécurisé
- login : `/admin/login`
- dashboard : `/admin/`
- catalogue : `/admin/catalogue`
- demandes : `/admin/demandes-de-devis`
- utilisateurs : `/admin/users`
- rôles : `/admin/roles`
- audit : `/admin/audit`

## PythonAnywhere gratuit

Le déploiement actuel peut utiliser SQLite via une URL absolue, par exemple :

```env
APP_ENV=production
DATABASE_URL=sqlite:////home/YOUR_USERNAME/traiteur/instance/wato_events.db
```

Voir [docs/PYTHONANYWHERE_SQLITE.md](docs/PYTHONANYWHERE_SQLITE.md).

## MySQL futur

Le passage futur vers MySQL se fera en changeant `DATABASE_URL` **après** création du schéma MySQL avec Alembic et transfert contrôlé des données. Changer uniquement l'URL ne migre pas les données existantes.

## Tests

```bash
pytest
```

Les tests SQLite couvrent notamment migrations sur base vierge, FK, WAL/timeout, Decimal, RBAC et création du super-admin.


## UI / UX

La direction visuelle, les tokens, le responsive, le configurateur et le shell admin sont documentés dans [docs/UI_UX.md](docs/UI_UX.md).
