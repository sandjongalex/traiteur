# Architecture de déploiement PythonAnywhere — WATO EVENTS

Ce document décrit la cible de déploiement. Il ne constitue pas encore le sprint de mise en production.

## 1. Composants compatibles

- Flask via WSGI ;
- virtualenv ;
- MySQL PythonAnywhere ;
- SQLAlchemy/PyMySQL ;
- Flask-Migrate/Alembic ;
- fichiers statiques ;
- uploads locaux ;
- variables d'environnement.

Aucun Redis, Celery, Docker, microservice ou Kubernetes obligatoire.

## 2. Structure

Le code applicatif est cloné dans un répertoire utilisateur. Le WSGI importe `create_app` ou `app` depuis `run.py`.

## 3. Variables

Production requiert au minimum :

- APP_ENV=production
- SECRET_KEY
- DATABASE_URL
- APP_TIMEZONE=Africa/Douala
- WATO_CURRENCY=XAF

Les valeurs réelles ne sont jamais commitées.

## 4. Base

MySQL en production. Les changements de schéma passent par :

```bash
flask --app run.py db upgrade
```

Une sauvegarde doit précéder les migrations risquées.

## 5. Statiques et uploads

- statiques servis via configuration PythonAnywhere ;
- uploads persistants dans un dossier dédié ;
- permissions d'écriture limitées ;
- sauvegarde des uploads ;
- futurs documents privés servis via route autorisée, pas par exposition publique brute.

## 6. Mise à jour future

Procédure cible :

1. sauvegarde ;
2. pull Git ;
3. activation virtualenv ;
4. `pip install -r requirements.txt` ;
5. migrations ;
6. tests/smoke checks ;
7. reload web app.

## 7. Contraintes d'architecture

Le monolithe modulaire évite les services d'infrastructure supplémentaires et reste adapté au MVP WATO EVENTS.
