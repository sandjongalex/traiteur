# WATO EVENTS

Plateforme Flask/MySQL mobile-first pour WATO EVENTS — Traiteur & Événementiel à Yaoundé.

## État
PROMPT 0 à 5 : **terminés**.  
Prochaine étape : **PROMPT 6 — CRM PROSPECTS + CLIENTS**.

## Back-office sécurisé
- login : `/admin/login`
- dashboard : `/admin/`
- catalogue : `/admin/catalogue`
- demandes : `/admin/demandes-de-devis`
- utilisateurs : `/admin/users`
- rôles : `/admin/roles`
- audit : `/admin/audit`
- profil : `/admin/profile`

L’ancien accès par `WATO_CATALOG_ADMIN_KEY` a été supprimé. Le seul mécanisme valide est désormais Flask-Login + RBAC.

## Mise en route
```bash
pip install -r requirements.txt
flask --app run.py db upgrade
flask --app run.py seed-rbac
flask --app run.py create-superadmin
flask --app run.py run
```

`create-superadmin` demande les informations et le mot de passe de manière interactive ; aucun mot de passe par défaut n’est fourni.

## Sécurité
- mots de passe hashés avec Werkzeug ;
- longueur minimale : 12 caractères ;
- cookies HttpOnly/SameSite, Secure en production ;
- CSRF maintenu ;
- permissions contrôlées côté serveur ;
- SUPER_ADMIN via rôle système unique ;
- protection du dernier SUPER_ADMIN actif ;
- journal d’audit minimal ;
- open redirect bloqué.

## Documentation
Voir `docs/AUTHENTICATION.md`, `docs/RBAC.md`, `docs/SECURITY.md`, `docs/ERD.md`, `docs/DATABASE_DESIGN.md`, `docs/TEST_STRATEGY.md` et `docs/ROADMAP.md`.
