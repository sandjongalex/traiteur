# RBAC — DNP DECO

## Source de vérité
Le serveur applique les permissions sous forme `resource.action`. Le masquage d’un bouton ne remplace jamais le contrôle serveur.

SUPER_ADMIN est **un rôle système**, pas un booléen concurrent. Un utilisateur actif possédant ce rôle bénéficie d’un bypass explicite de permissions.

## Rôles initiaux
SUPER_ADMIN, ADMIN, COMMERCIAL, CUISINE, LOGISTIQUE, COMPTABILITE, PERSONNEL.

## Permissions actuellement implémentées
`dashboard.view`, `catalog.view`, `catalog.create`, `catalog.edit`, `catalog.validate`, `quote_request.view`, `quote_request.edit`, `quote_request.validate`, `user.view`, `user.create`, `user.edit`, `role.view`, `role.manage`, `audit.view`, `settings.view`.

## Matrice appliquée
- SUPER_ADMIN : toutes les permissions implicitement.
- ADMIN : dashboard, catalogue complet hors suppression, demandes, gestion utilisateurs, lecture rôles/audit/settings.
- COMMERCIAL : dashboard, lecture catalogue, consultation/traitement/validation demandes.
- CUISINE : dashboard + lecture catalogue.
- LOGISTIQUE : dashboard + lecture catalogue + lecture demandes.
- COMPTABILITE : dashboard + lecture catalogue/demandes + audit.
- PERSONNEL : dashboard uniquement.

Seul SUPER_ADMIN possède `role.manage` dans le seed initial.

## Dernier SUPER_ADMIN
Le dernier SUPER_ADMIN actif ne peut pas être désactivé ni perdre son rôle.

## Seed
`flask --app run.py seed-rbac` est idempotent et synchronise rôles/permissions.
