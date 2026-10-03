# RBAC — WATO EVENTS

## 1. Décision MVP

Utiliser **Role + Permission** plutôt qu'un enum de rôle codé en dur, mais démarrer avec un jeu de rôles prédéfinis. Cela reste simple tout en permettant d'ajouter une permission sans migration de code métier.

Rôles initiaux :

- SUPER_ADMIN
- ADMIN
- COMMERCIAL
- CUISINE
- LOGISTIQUE
- COMPTABILITE
- PERSONNEL

Actions standardisées :

- VIEW
- CREATE
- EDIT
- DELETE
- VALIDATE
- EXPORT

Le contrôle doit toujours être effectué côté serveur.

## 2. Matrice initiale

Légende : ✓ autorisé, L limité au périmètre métier, — interdit par défaut.

| Module | SUPER_ADMIN | ADMIN | COMMERCIAL | CUISINE | LOGISTIQUE | COMPTABILITE | PERSONNEL |
|---|---|---|---|---|---|---|---|
| Dashboard VIEW | ✓ | ✓ | L | L | L | L | L |
| Prospects/Clients | ✓ | ✓ | ✓ CRUD | VIEW | VIEW | VIEW | — |
| Catalogue | ✓ | ✓ | VIEW | VIEW | VIEW | VIEW | — |
| Demandes/Devis | ✓ | ✓ | ✓ C/E/V | VIEW | VIEW | VIEW | — |
| Commandes | ✓ | ✓ | ✓ C/E | VIEW | VIEW | VIEW | — |
| Événements | ✓ | ✓ | ✓ C/E | VIEW | ✓ E | VIEW | L VIEW |
| Paiements | ✓ | ✓ | VIEW | — | — | ✓ C/E/V | — |
| Factures | ✓ | ✓ | VIEW | — | — | ✓ C/E/V/EXPORT | — |
| Stock | ✓ | ✓ | VIEW | L C/E | ✓ C/E/V | VIEW | — |
| Fournisseurs/Achats | ✓ | ✓ | VIEW | — | ✓ C/E | ✓ VIEW/V | — |
| Matériel | ✓ | ✓ | VIEW | VIEW | ✓ C/E/V | VIEW | — |
| Personnel/Planning | ✓ | ✓ | VIEW | VIEW | ✓ VIEW | VIEW | L VIEW |
| Galerie | ✓ | ✓ | L C/E | — | — | — | — |
| Rapports | ✓ | ✓ | L VIEW | L VIEW | L VIEW | ✓ VIEW/EXPORT | — |
| Utilisateurs/Rôles | ✓ | ✓ limité | — | — | — | — | — |
| Paramètres | ✓ | ✓ limité | — | — | — | VIEW | — |
| Audit | ✓ | VIEW | — | — | — | L VIEW | — |

`VALIDATE` couvre les transitions sensibles : accepter devis, confirmer réservation, valider paiement/achat/ajustement.

## 3. Règles

- aucun rôle standard ne devient administrateur implicitement ;
- SUPER_ADMIN gère les droits les plus sensibles ;
- ADMIN n'a pas automatiquement le droit de modifier les rôles SUPER_ADMIN ;
- DELETE doit rester rare ;
- les actions financières et stock sensibles doivent être auditées ;
- les permissions doivent être testées sur les routes et services, pas uniquement l'interface.
