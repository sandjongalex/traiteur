# Roadmap — WATO EVENTS

Le projet est développé par sprints successifs. Chaque sprint suit le cycle :

**ANALYSER → IMPLÉMENTER → MIGRER → TESTER → CORRIGER → DOCUMENTER → RÉSUMER**

## PROMPT 0 — Cadrage maître
État : **TERMINÉ**.

Vision, périmètre, principes et conventions initiales.

## PROMPT 0.5 — Architecture globale et conception technique
État : **TERMINÉ**.

Ce sprint d'architecture a été documenté après la mise en place du socle PROMPT 1. Aucun module métier n'ayant encore été développé, l'ordre réel ne crée pas de dette fonctionnelle : les fondations existantes sont compatibles avec les décisions d'architecture.

Livrables : architecture globale, ERD, flux métier, conception DB, RBAC, sécurité, tests, PythonAnywhere et ADR.

## PROMPT 1 — Fondations Flask + MySQL
État : **TERMINÉ**.

Socle livré : application factory, configuration par environnement, SQLAlchemy, Flask-Migrate/Alembic, MySQL/PyMySQL, CSRF, route de santé, commande DB et tests de base.

## PROMPT 2 — Identité visuelle + site public
État : **PROCHAINE ÉTAPE**.

Construire le shell public mobile first : layout, navigation, accueil, pages institutionnelles, SEO de base et identité visuelle. Ne pas encore implémenter le catalogue métier complet.

## PROMPT 3 — Services + menus + plats + packs
Implémenter le catalogue administrable et son affichage public. C'est le premier vrai domaine métier persistant.

## PROMPT 4 — Configurateur + demandes de devis
Créer QuoteRequest, configurateur public, estimation indicative et capture prospect. Les calculs passent par PricingService.

## PROMPT 5 — Authentification + back-office + RBAC
Mettre en place User, Role, Permission, connexion, sessions, matrice d'accès et audit minimal.

## PROMPT 6 — CRM prospects / clients
Gérer Prospect, Customer, conversion, historique commercial et recherches.

## PROMPT 7 — Devis professionnels
Quote, QuoteItem, numérotation DEV, snapshots commerciaux, transitions, acceptation.

## PROMPT 8 — Commandes + événements
Créer Order séparé de Event. Gérer le passage devis accepté → commande, puis événement lorsque la prestation nécessite une planification.

## PROMPT 9 — Paiements + facturation
Paiements multiples, soldes, Invoice, numérotation FAC, reçus et règles financières.

## PROMPT 10 — Stocks + fournisseurs + achats
Ingredient, Supplier, Purchase, PurchaseItem et ledger StockMovement.

## PROMPT 11 — Matériel événementiel
Equipment, EquipmentReservation, disponibilité et conflits temporels.

## PROMPT 12 — Personnel + planning
Employee distinct de User, EventAssignment, disponibilités, horaires et coûts.

## PROMPT 13 — Dashboard + rapports
Agrégats en lecture : CA, encaissements, créances, conversion, événements, rentabilité, dépenses, stock et matériel.

## PROMPT 14 — Galerie + marketing + SEO
Galerie administrable, Open Graph, sitemap, contenu marketing et optimisation conversion.

## PROMPT 15 — Tests complets + sécurité + optimisation
Durcissement transversal, tests MySQL, permissions, concurrence, performance, uploads et revue sécurité.

## PROMPT 16 — Déploiement PythonAnywhere
WSGI, MySQL production, virtualenv, statiques, uploads, migrations, sauvegarde et procédure de mise à jour.

## Cohérence technique

L'ordre est retenu avec les précisions suivantes :

1. le catalogue précède le configurateur afin que QuoteRequest référence des offres réelles ;
2. les demandes publiques peuvent être collectées avant l'authentification du back-office ;
3. RBAC est installé avant CRM et documents commerciaux privés ;
4. Quote précède Order/Event ;
5. Billing suit l'engagement commercial ;
6. Inventory/Equipment/Staff arrivent après Event car ils s'y rattachent ;
7. Reporting arrive après la création des sources de données.

Chaque sprint doit laisser une application fonctionnelle et préserver les données existantes.

**Prochaine étape : PROMPT 2 — IDENTITÉ VISUELLE + SITE PUBLIC.**
