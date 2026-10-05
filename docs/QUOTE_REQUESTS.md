# Demandes de devis — DNP DECO

## Concepts

`QuoteRequest` est une demande commerciale entrante. Ce n'est pas un devis officiel.

Référence : `DEM-AAAA-NNNNNN`.

Le futur devis officiel utilisera une numérotation distincte `DEV-...`.

## Modèles

### QuoteRequest
Contient référence, statut, source, coordonnées, informations événement, budget, estimation connue, indicateur d'éléments sur devis, devise et timestamps.

### QuoteRequestItem
Snapshot d'un Service, Dish, Menu ou Pack : type, ID catalogue, libellé, quantité, prix unitaire, unité de tarification et sous-total estimé.

### QuoteRequestSequence
Compteur annuel pour les références DEM. La ligne annuelle est verrouillée lors de l'incrément. Un risque de concurrence subsiste uniquement lors de la création simultanée de la toute première ligne d'une année ; la contrainte unique protège l'intégrité mais ce cas devra être retesté sous MySQL en charge.

## Event type

Le module Event n'existe pas encore. Le type d'événement est donc une valeur applicative contrôlée par `EventType`, stockée en snapshot texte dans QuoteRequest.

## Pricing

`PricingService` est la source de vérité.

- FIXED : prix fixe ;
- PER_PERSON : prix × guest_count ;
- PER_UNIT : prix × quantité ;
- PER_HOUR : prix × nombre d'heures ;
- ON_REQUEST : aucun faux montant.

Si `guest_count` est inférieur au `minimum_people` d'un Menu/Pack, la demande reste possible mais le sous-total devient « à confirmer » et n'est pas ajouté au total connu.

## Plats

Le modèle et PricingService supportent DISH pour compatibilité future, mais le configurateur public du MVP ne propose pas les plats individuellement. Cette décision évite de surcharger l'UX alors que l'offre actuelle est structurée principalement autour des services, menus et packs.

## Sécurité

- CSRF ;
- honeypot ;
- validation serveur ;
- date passée refusée ;
- au moins un moyen de contact ;
- quantités bornées ;
- catalogue rechargé au POST ;
- prix navigateur ignorés ;
- transaction unique pour demande + items ;
- submission_token unique contre double soumission ;
- public_token aléatoire pour la confirmation ;
- aucune donnée personnelle affichée sur la confirmation publique.

## Administration

`/admin/demandes-de-devis`

Fonctions : liste, recherche, filtre statut, détail, consultation estimation et changement de statut. Pas de hard delete.

La protection temporaire réutilise la session catalogue et doit être supprimée au PROMPT 5.
