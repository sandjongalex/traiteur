# Stratégie de tests — WATO EVENTS

## 1. Arborescence cible

```text
tests/
  unit/
  services/
  routes/
  permissions/
  integration/
```

La structure actuelle minimale reste valide et sera migrée progressivement.

## 2. Catégories

### Unit tests
Calculs purs, enums, helpers, validation.

### Service tests
Règles métier et transitions, avec base de test.

### Route tests
HTTP, formulaires, réponses, redirections, erreurs.

### Permission tests
Chaque rôle face aux actions sensibles et tentatives d'accès direct.

### Integration tests
Scénarios multi-domaines et transactions.

## 3. Couverture renforcée

Priorités :

1. PricingService ;
2. PaymentService ;
3. InventoryService ;
4. permissions/RBAC ;
5. EquipmentService et conflits de réservation ;
6. NumberingService ;
7. acceptation devis → commande/événement.

## 4. Cas critiques

### Pricing
- quantités ;
- prix par personne ;
- remises ;
- taxes ;
- arrondis Decimal ;
- snapshot des prix.

### Paiements
- paiement partiel ;
- plusieurs paiements ;
- dépassement interdit ou contrôlé ;
- annulation/remboursement ;
- solde exact.

### Stock
- chaque opération crée un mouvement ;
- perte/retour/correction ;
- rollback en cas d'échec ;
- cohérence du solde.

### Permissions
- accès autorisé ;
- accès refusé par URL directe ;
- validation sensible ;
- rôle modifié.

### Matériel
- chevauchement temporel ;
- quantité insuffisante ;
- annulation libère la réservation ;
- matériel en maintenance indisponible.

## 5. Base de test

SQLite mémoire convient aux tests rapides existants, mais les opérations dépendant de comportements MySQL, verrous, contraintes ou transactions concurrentes doivent aussi être testées sur MySQL avant déploiement.

## 6. Règle de finition

Une fonctionnalité critique n'est pas terminée sans tests de succès, refus métier et permissions principales.
