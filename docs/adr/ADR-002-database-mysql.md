# ADR-002 — Portabilité base de données : SQLite aujourd'hui, MySQL demain

## Contexte
L'environnement PythonAnywhere gratuit actuellement disponible ne fournit pas de base MySQL utilisable pour WATO EVENTS. Le MVP doit néanmoins être exécutable avec persistance relationnelle, contraintes et migrations.

## Décision
SQLAlchemy reste l'abstraction unique et Alembic/Flask-Migrate reste le mécanisme de schéma.

- SQLite est le moteur opérationnel actuel.
- MySQL reste la cible recommandée lorsque la concurrence et le volume d'écritures augmentent.
- `DATABASE_URL` sélectionne le moteur.
- Aucun modèle ou service métier n'est dupliqué par moteur.

## SQLite
La DB fichier reste dans `instance/`, hors contenu statique. Les connexions activent FK, busy timeout et WAL par défaut.

## Conséquences
SQLite convient au MVP actuel mais conserve une concurrence d'écriture limitée. Les signaux de migration vers MySQL incluent : erreurs `database locked`, nombreux opérateurs simultanés, stock/paiements temps réel, réservations concurrentes, forte croissance ou besoin de haute disponibilité.

La migration future de données sera une opération séparée : Alembic crée le schéma MySQL, mais changer `DATABASE_URL` ne transfère pas les données SQLite.
