# Sécurité — WATO EVENTS

## 1. Authentification / autorisation

Le vrai système User/Role/Permission n'est pas encore implémenté. Catalogue et demandes utilisent temporairement une seule protection `WATO_CATALOG_ADMIN_KEY` et la même session. Ce mécanisme doit être supprimé au PROMPT 5.

## 2. CSRF

Flask-WTF/CSRFProtect protège les formulaires mutatifs publics et administratifs.

## 3. QuoteRequest : données personnelles

QuoteRequest peut contenir nom, téléphone, WhatsApp, email, lieu et notes.

Règles :

- ne pas logger le formulaire complet ;
- ne pas mettre les coordonnées dans l'URL ;
- ne pas exposer une demande complète publiquement ;
- la confirmation utilise référence + token aléatoire ;
- la page de confirmation n'affiche aucune coordonnée personnelle.

## 4. Prix

Le navigateur n'est jamais source de vérité.

Le client transmet uniquement IDs et quantités. Le serveur recharge Service/Menu/Pack/Dish actifs et publics puis PricingService recalcule avant enregistrement.

## 5. Anti-abus MVP

Le configurateur utilise :

- CSRF ;
- honeypot ;
- limites de longueur ;
- bornes sur guest_count et quantités ;
- validation date ;
- submission_token unique pour réduire les doubles soumissions.

Aucun Redis ni service externe n'est ajouté pour du rate limiting à ce stade.

## 6. Confirmation

Une référence DEM séquentielle n'est pas suffisante pour consulter une confirmation. Un `public_token` aléatoire est exigé en plus.

## 7. Uploads catalogue

Extensions et MIME contrôlés, noms sécurisés puis remplacés par UUID.

## 8. Secrets et production

- aucun secret commité ;
- `.env` ignoré ;
- DEBUG=False en production ;
- SECRET_KEY obligatoire ;
- WATO_CATALOG_ADMIN_KEY fournie par environnement tant que le mécanisme temporaire existe.

## 9. Risques à surveiller

- concurrence de numérotation DEM ;
- données personnelles ;
- falsification de sélection/prix ;
- double soumission ;
- futur passage QuoteRequest → Prospect/Quote ;
- remplacement impératif de la clé temporaire au PROMPT 5.
