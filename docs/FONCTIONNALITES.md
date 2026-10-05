# Fonctionnalités — DNP DECO

Ce document décrit les modules fonctionnels prévus. Il s'agit d'un cadrage ; les modules ne sont pas implémentés au PROMPT 0.

## 1. Site public

Pages prévues :

- Accueil ;
- À propos ;
- Services ;
- Menus ;
- Packs événementiels ;
- Galerie / Réalisations ;
- Demande de devis ;
- Contact ;
- accès WhatsApp.

## 2. Configurateur de besoin / devis

Données possibles :

- type d'événement ;
- date ;
- lieu ;
- nombre de personnes ;
- budget éventuel ;
- menu ;
- pack ;
- plats ;
- boissons ;
- service ;
- personnel ;
- matériel ;
- options ;
- commentaires.

Le système pourra fournir une estimation indicative. Celle-ci ne constitue pas automatiquement un devis contractuel ou définitif.

## 3. Back-office

Modules futurs :

- Dashboard ;
- Prospects ;
- Clients ;
- Demandes de devis ;
- Devis ;
- Commandes ;
- Événements ;
- Menus ;
- Packs ;
- Stocks ;
- Fournisseurs ;
- Achats ;
- Matériel ;
- Personnel ;
- Paiements ;
- Factures ;
- Galerie ;
- Rapports ;
- Utilisateurs ;
- Paramètres.

## 4. Prospects et clients

Le système devra distinguer :

- un prospect issu d'une demande ;
- un client confirmé ;
- l'historique commercial ;
- les événements associés ;
- les devis, paiements et factures associés.

## 5. Devis

Contenu possible :

- client ;
- événement ;
- prestations ;
- menus ;
- quantités ;
- matériel ;
- personnel ;
- options ;
- remises ;
- taxes éventuelles ;
- total ;
- acompte ;
- conditions ;
- date de validité ;
- statut.

Statuts :

- `BROUILLON`
- `ENVOYE`
- `ACCEPTE`
- `REFUSE`
- `EXPIRE`
- `ANNULE`

## 6. Événements

Données possibles :

- client ;
- type ;
- date ;
- heure ;
- adresse ;
- nombre de personnes ;
- responsable ;
- menu ;
- prestations ;
- matériel ;
- personnel ;
- notes ;
- statut.

Statuts :

- `PLANIFIE`
- `CONFIRME`
- `PREPARATION`
- `EN_COURS`
- `TERMINE`
- `ANNULE`

## 7. Paiements

Méthodes initiales :

- espèces ;
- Mobile Money ;
- virement ;
- autres méthodes extensibles.

Règle fondamentale :

`SOLDE_RESTANT = TOTAL - SOMME(PAIEMENTS_VALIDES)`

Un paiement partiel ne marque pas automatiquement un événement comme payé.

## 8. Stocks

Fonctionnalités futures :

- matières premières ;
- unités ;
- catégories ;
- entrées ;
- sorties ;
- ajustements ;
- pertes ;
- inventaires ;
- fournisseurs ;
- seuils d'alerte.

Principe : les mouvements sont tracés. La quantité courante ne doit pas être modifiée silencieusement sans historique.

## 9. Matériel événementiel

Exemples :

- tables ;
- chaises ;
- nappes ;
- vaisselle ;
- verres ;
- couverts ;
- chafing dishes ;
- glacières ;
- équipements cuisine ;
- décoration.

États de quantité à distinguer :

- totale ;
- disponible ;
- réservée ;
- endommagée ;
- maintenance.

Le matériel pourra être affecté à des événements.

## 10. Personnel

Profils possibles :

- cuisiniers ;
- serveurs ;
- responsables ;
- chauffeurs ;
- logisticiens ;
- personnel temporaire.

Affectations :

- disponibilité ;
- événement ;
- mission ;
- horaires ;
- coût éventuel.

## 11. Tableau de bord et rapports

Indicateurs futurs :

- chiffre d'affaires ;
- montant encaissé ;
- créances ;
- demandes de devis ;
- taux de transformation ;
- événements futurs ;
- événements terminés ;
- dépenses ;
- rentabilité par événement ;
- stock faible ;
- matériel indisponible.

## 12. SEO et marketing

Cibles initiales :

- Traiteur Yaoundé ;
- Traiteur mariage Yaoundé ;
- Service traiteur Yaoundé ;
- Buffet Yaoundé ;
- Traiteur événementiel Cameroun ;
- Événementiel Yaoundé.

Prévoir :

- titres et meta descriptions ;
- Open Graph ;
- URLs propres ;
- structure H1/H2 ;
- sitemap futur ;
- robots.txt ;
- galerie et contenus de réalisations ;
- intégration WhatsApp configurable.
