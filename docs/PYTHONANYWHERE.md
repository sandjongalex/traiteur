# Architecture de déploiement PythonAnywhere — DNP DECO

La cible actuelle sur offre gratuite utilise SQLite. MySQL reste une cible future lorsque l'environnement et la charge le justifient.

## Composants

- Flask via WSGI ;
- virtualenv ;
- SQLAlchemy ;
- SQLite actuellement / MySQL futur ;
- Flask-Migrate/Alembic ;
- fichiers statiques et uploads locaux ;
- variables d'environnement.

Aucun Redis, Celery ou Docker obligatoire.

Pour la procédure opérationnelle actuelle, voir `PYTHONANYWHERE_SQLITE.md`.
