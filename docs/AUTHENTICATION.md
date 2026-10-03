# Authentification — WATO EVENTS

## Connexion
`/admin/login` avec email + mot de passe. Message générique en cas d’échec. `next` est validé contre les redirections externes.

## Mot de passe
Hash Werkzeug. Minimum 12 caractères. Aucun mot de passe en clair ou hash n’est affiché dans le back-office.

## Premier compte
1. `flask --app run.py db upgrade`
2. `flask --app run.py seed-rbac`
3. `flask --app run.py create-superadmin`

Aucun mot de passe par défaut.

## Utilisateurs
Liste/création/édition, activation/désactivation, rôles et reset de mot de passe. Un reset admin place `must_change_password=True`.

## Profil
`/admin/profile` affiche identité/rôles/dernière connexion et permet le changement du mot de passe avec vérification du mot de passe actuel.

## Super admin
SUPER_ADMIN est un rôle système et fournit le bypass. Le dernier compte actif portant ce rôle est protégé.
