# Sécurité — WATO EVENTS

## Authentification
Flask-Login, email normalisé unique, mots de passe hashés Werkzeug, minimum 12 caractères. Les erreurs de login restent génériques.

## Sessions
`SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE=Lax`, durée raisonnable ; `SESSION_COOKIE_SECURE=True` et `REMEMBER_COOKIE_SECURE=True` en production. La protection de session Flask-Login est `strong`.

## Autorisation
`permission_required()` vérifie authentification, utilisateur actif et permission serveur. Un utilisateur authentifié sans permission reçoit 403.

## CSRF
Conservé sur les mutations publiques et administratives, y compris logout.

## Open redirect
Le paramètre `next` n’est accepté que si son hôte correspond au site courant.

## Désactivation
Un utilisateur inactif ne peut pas se connecter. Une session admin existante d’un utilisateur devenu inactif est invalidée.

## SUPER_ADMIN
Le rôle SUPER_ADMIN est l’unique mécanisme de bypass. Le dernier SUPER_ADMIN actif est protégé.

## Audit
AuditLog est non éditable dans l’interface. Sont journalisés notamment : login réussi/échoué, logout, création/désactivation utilisateur, changement rôles, reset/changement mot de passe, changements de publication catalogue et statut QuoteRequest.

## Ancien bypass
`WATO_CATALOG_ADMIN_KEY`, le formulaire de clé, la route d’accès et la session `catalog_admin` ont été supprimés. Ils ne constituent plus un mécanisme d’accès.


## SQLite en production actuelle

Le fichier SQLite doit rester dans `instance/` ou un autre répertoire privé, jamais sous `app/static/` ou `uploads/`. Les permissions Unix doivent limiter lecture/écriture au compte PythonAnywhere concerné.

Ne jamais journaliser `DATABASE_URL` complet : une future URL MySQL peut contenir des identifiants.

Les sauvegardes SQLite doivent produire un snapshot cohérent via l'API backup SQLite ou pendant une fenêtre sans écriture. Les sauvegardes et fichiers DB sont exclus de Git.

`SECRET_KEY` reste obligatoire en `APP_ENV=production`, même avec SQLite.
