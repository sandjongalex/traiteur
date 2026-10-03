# Stratégie de tests — WATO EVENTS

## Niveaux

- modèles et contraintes ;
- services métier ;
- routes publiques ;
- routes admin ;
- permissions ;
- intégration / transactions.

SQLite mémoire est utilisé pour les tests rapides. Les verrous et comportements dépendants de MySQL doivent aussi être validés sur MySQL avant production.

## Catalogue

Tests existants : modèles, relations, publication, admin et uploads.

## QuoteRequest / PricingService

Cas critiques ajoutés :

- FIXED ;
- PER_PERSON ;
- PER_UNIT ;
- PER_HOUR ;
- ON_REQUEST ;
- Decimal ;
- minimum_people ;
- quantité invalide ;
- élément privé/inactif ;
- GET configurateur ;
- soumission valide ;
- contact manquant ;
- date passée ;
- snapshot de prix ;
- tentative de falsification `price=1` ;
- double submission_token ;
- confirmation avec token public ;
- absence de données personnelles sur confirmation ;
- admin protégé ;
- liste/détail ;
- statut valide/invalide ;
- absence de hard delete standard.

## Tests futurs prioritaires

1. exécution complète sur MySQL ;
2. concurrence sur première séquence DEM d'une année ;
3. User/RBAC au PROMPT 5 ;
4. conversion CRM ;
5. Quote officiel et snapshots contractuels.

## Règle

Ne jamais annoncer un test comme réussi s'il n'a pas été réellement exécuté.


## PROMPT 5 — Auth/RBAC

Tests ajoutés : hash/vérification mot de passe, unicité email, seed idempotent, login correct/incorrect/inexistant/inactif, logout, route protégée, open redirect, matrice RBAC, requête forgée directe, bypass SUPER_ADMIN, dernier SUPER_ADMIN, ancien `catalog_admin` inefficace, audit login/désactivation. Les anciens tests admin Catalogue et QuoteRequest ont été migrés vers de vrais comptes RBAC.

L’environnement conversationnel ne contient pas Flask ; aucun résultat pytest n’est revendiqué sans exécution réelle.
