# Roadmap — WATO EVENTS

Le projet est développé par sprints successifs. Chaque sprint suit le cycle :

**ANALYSER → IMPLÉMENTER → MIGRER → TESTER → CORRIGER → DOCUMENTER → RÉSUMER**

## PROMPT 0 — Cadrage maître

Objectif : vision, architecture, règles fondamentales, conventions, roadmap, préparation du dépôt.

État : **cadrage documentaire**.

## PROMPT 1 — Fondations Flask + MySQL

Prévoir :

- squelette Flask ;
- application factory ;
- extensions ;
- configuration par environnement ;
- SQLAlchemy ;
- Flask-Migrate ;
- connexion MySQL ;
- base des tests ;
- commandes de démarrage ;
- premiers contrôles de qualité.

## PROMPT 2 — Identité visuelle + site public

Accueil, navigation, structure publique, responsive mobile first, identité WATO EVENTS.

## PROMPT 3 — Services + menus + packs

Gestion et affichage des offres structurées.

## PROMPT 4 — Configurateur + demandes de devis

Parcours de configuration, estimation indicative, enregistrement des demandes.

## PROMPT 5 — Authentification + back-office + rôles

Connexion, sessions, RBAC, protections d'accès.

## PROMPT 6 — CRM prospects/clients

Cycle prospect → client et historique commercial.

## PROMPT 7 — Devis professionnels

Création, lignes, calculs, statuts, validité, génération/partage futur.

## PROMPT 8 — Commandes + événements

Transformation opérationnelle des engagements clients.

## PROMPT 9 — Paiements + facturation

Paiements multiples, acomptes, solde, facturation.

## PROMPT 10 — Stocks + fournisseurs + achats

Traçabilité des mouvements, inventaires, approvisionnement.

## PROMPT 11 — Matériel événementiel

Disponibilité, réservation, maintenance, affectation.

## PROMPT 12 — Personnel + planning

Disponibilités, affectations, missions, horaires et coûts.

## PROMPT 13 — Dashboard + rapports

KPI commerciaux, opérationnels et financiers.

## PROMPT 14 — Galerie + marketing + SEO

Réalisations, optimisation SEO, conversion, intégrations marketing.

## PROMPT 15 — Tests complets + sécurité + optimisation

Durcissement global, couverture critique, performance, revue sécurité.

## PROMPT 16 — Déploiement PythonAnywhere

Déploiement, WSGI, MySQL, statiques, uploads, migrations et procédure de mise à jour.

## Règles de roadmap

- Chaque sprint inspecte l'état réel du dépôt avant modification.
- Une fonctionnalité d'un sprint futur ne doit pas être développée par anticipation, sauf dépendance architecturale indispensable.
- Toute modification du schéma passe par migration.
- Toute fonctionnalité critique doit être testée.
- La roadmap peut évoluer si l'état réel du projet le justifie.

**Prochaine étape : PROMPT 1 — FONDATIONS FLASK + MYSQL.**
