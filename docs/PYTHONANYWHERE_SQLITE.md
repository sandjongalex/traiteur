# PythonAnywhere gratuit + SQLite — DNP DECO

## 1. Objectif

Faire fonctionner l'application actuelle sans MySQL, en conservant exactement les mêmes modèles SQLAlchemy et migrations Alembic.

## 2. Emplacement de la base

Créer un dossier privé dans le projet :

```bash
cd ~/traiteur
mkdir -p instance
```

Exemple de chemin :

`/home/YOUR_USERNAME/traiteur/instance/wato_events.db`

Remplacer `YOUR_USERNAME` par le nom du compte PythonAnywhere. Ne jamais placer la DB sous `app/static`.

## 3. Variables d'environnement

Exemple :

```bash
export APP_ENV=production
export SECRET_KEY='VALEUR_FORTE_A_GENERER_HORS_GIT'
export DATABASE_URL='sqlite:////home/YOUR_USERNAME/traiteur/instance/wato_events.db'
export APP_TIMEZONE='Africa/Douala'
export WATO_CURRENCY='XAF'
export SQLITE_BUSY_TIMEOUT_MS='5000'
export SQLITE_WAL_ENABLED='1'
```

Ne pas commiter les valeurs réelles.

## 4. Initialisation

```bash
cd ~/traiteur
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

flask --app run.py db heads
flask --app run.py db upgrade
flask --app run.py db current
flask --app run.py db-check

flask --app run.py seed-rbac
flask --app run.py seed-rbac
flask --app run.py create-superadmin
```

Le second `seed-rbac` vérifie l'idempotence.

La HEAD attendue après le PROMPT 5 est :

`20261003_03_auth_rbac`

## 5. WSGI minimal

Le projet expose déjà `create_app()` et `run.py`. Un fichier WSGI PythonAnywhere peut importer :

```python
import sys
sys.path.insert(0, "/home/YOUR_USERNAME/traiteur")

from app import create_app
application = create_app()
```

Les variables d'environnement doivent être disponibles au processus WSGI avant la création de l'application.

## 6. Vérifications fonctionnelles

Sans authentification :

- `/`
- `/services`
- `/menus`
- `/packs`
- `/demande-de-devis`
- `/admin/login`
- `/health`

Après connexion SUPER_ADMIN :

- `/admin/`
- `/admin/catalogue/`
- `/admin/demandes-de-devis/`
- `/admin/users/`
- `/admin/roles/`
- `/admin/audit/`

## 7. SQLite : réglages appliqués

À chaque connexion SQLite :

- `PRAGMA foreign_keys=ON`
- `PRAGMA busy_timeout=5000` par défaut
- `PRAGMA journal_mode=WAL` si `SQLITE_WAL_ENABLED=1`

WAL améliore les lectures simultanées avec une écriture, mais SQLite reste limité pour les écritures concurrentes.

## 8. Sauvegarde

Méthode recommandée : API backup SQLite vers un nouveau fichier daté.

Exemple depuis le dossier projet, idéalement pendant une période calme :

```bash
python - <<'PY'
import sqlite3
from datetime import datetime
from pathlib import Path

src = Path("instance/wato_events.db")
dst = Path("instance") / f"backup-{datetime.now():%Y%m%d-%H%M%S}.db"

with sqlite3.connect(src) as source, sqlite3.connect(dst) as target:
    source.backup(target)

print(dst)
PY
```

Ne pas versionner les backups.

## 9. Restauration

1. éviter/arrêter les écritures ;
2. sauvegarder la DB actuelle ;
3. restaurer le fichier choisi à la place de `instance/wato_events.db` ;
4. vérifier les permissions ;
5. exécuter `flask --app run.py db current` ;
6. lancer `flask --app run.py db-check` ;
7. recharger l'application.

## 10. Migration future SQLite → MySQL

1. sauvegarder SQLite ;
2. provisionner MySQL ;
3. définir temporairement une `DATABASE_URL` MySQL sur une base vierge ;
4. appliquer toutes les migrations Alembic ;
5. transférer les données via un script/outil contrôlé ;
6. vérifier IDs, FK, Decimal et dates ;
7. comparer les comptes par table ;
8. basculer `DATABASE_URL` ;
9. exécuter les tests et smoke tests ;
10. conserver la sauvegarde SQLite.

**Changer uniquement `DATABASE_URL` ne transfère aucune donnée.**

## 11. Quand quitter SQLite

Réévaluer MySQL si apparaissent :

- écritures concurrentes fréquentes ;
- erreurs `database is locked` ;
- plusieurs opérateurs actifs en permanence ;
- paiements simultanés ;
- stock temps réel ;
- réservations concurrentes ;
- volume événementiel important ;
- besoin de haute disponibilité.
