# Sécurité — WATO EVENTS

## 1. Authentification

Prévoir Flask-Login ou équivalent, mots de passe hashés avec une primitive moderne, cookies de session sécurisés en production et protection contre les comptes désactivés.

## 2. Autorisation

RBAC côté serveur sur chaque opération privée. Une route ne doit jamais se fier uniquement au masquage d'un bouton.

## 3. CSRF

Flask-WTF/CSRFProtect est déjà initialisé. Tous les formulaires mutatifs doivent être protégés.

## 4. Entrées

- validation serveur systématique ;
- longueurs maximales ;
- formats email/téléphone/dates ;
- contraintes métier dans les services ;
- requêtes via SQLAlchemy, jamais concaténées manuellement.

## 5. Secrets

- aucun secret commité ;
- `.env` ignoré ;
- `.env.example` uniquement factice ;
- `SECRET_KEY`, URL MySQL et futurs tokens via environnement.

## 6. Uploads

- extensions et MIME autorisés ;
- taille maximale ;
- nom généré côté serveur ;
- jamais exécuter un fichier uploadé ;
- séparer documents publics et privés ;
- vérifier l'autorisation avant téléchargement d'un document privé.

## 7. Audit

Journaliser au minimum :

- modification/acceptation/annulation de devis ;
- paiements et remboursements ;
- émission/modification/annulation facture ;
- ajustements et corrections stock ;
- annulations événement/commande ;
- réservation/libération matériel sensible ;
- changement de rôle ;
- modification paramètres critiques.

AuditLog doit contenir : acteur, action, type/id ressource, timestamp, avant/après ou delta pertinent, adresse IP/metadata raisonnable.

## 8. Suppressions

Données financières, historiques et audit non supprimables par les opérations courantes. Utiliser archivage ou opérations compensatoires.

## 9. Production

- DEBUG=False ;
- SECRET_KEY obligatoire ;
- base MySQL avec utilisateur applicatif limité ;
- HTTPS fourni par l'hébergement ;
- sauvegardes DB et uploads ;
- logs sans secrets ni données sensibles inutiles.

## 10. Menaces principales

- élévation de privilèges ;
- IDOR / accès à l'objet d'un autre périmètre ;
- falsification de montants côté client ;
- doubles validations/paiements ;
- collision de numérotation ;
- upload malveillant ;
- pertes de données par suppression ;
- concurrence sur stock/réservations.

Les tests de sécurité fonctionnelle doivent cibler ces scénarios.
