# Architecture — WATO EVENTS

## 1. Principes

WATO EVENTS sera construit comme une application Flask modulaire, orientée MVP mais préparée pour l'évolution.

Principes :

- application factory `create_app()` ;
- Blueprints par domaine ou surface ;
- logique métier dans des services ;
- modèles SQLAlchemy séparés des routes ;
- templates Jinja2 sans logique métier complexe ;
- migrations Alembic/Flask-Migrate ;
- configuration par environnement ;
- compatibilité PythonAnywhere ;
- dépendances limitées au nécessaire.

## 2. Structure cible initiale

```text
app/
    __init__.py
    extensions.py

    models/

    routes/
        public/
        auth/
        admin/

    services/

    templates/
        public/
        auth/
        admin/

    static/
        css/
        js/
        images/
        uploads/

    utils/

config.py
run.py
requirements.txt
migrations/
tests/
docs/
```

Cette structure pourra être adaptée lorsque les besoins réels du dépôt l'exigeront, sans créer prématurément les modules métier.

## 3. Couches applicatives

### Routes / contrôleurs

Responsables de :

- réception HTTP ;
- authentification/autorisation ;
- validation des entrées ;
- appel des services ;
- choix de la réponse ou du template.

### Services

Responsables de :

- règles métier ;
- calculs ;
- transitions de statut ;
- orchestration entre modèles ;
- opérations réutilisables.

### Modèles

Responsables de :

- persistance ;
- relations ;
- contraintes structurelles ;
- propriétés simples proches de la donnée.

## 4. Base de données

Production : **MySQL**.

ORM : **SQLAlchemy**.

Évolution du schéma : **Flask-Migrate / Alembic**.

Règles :

- clés étrangères explicites ;
- index sur recherches fréquentes et colonnes de relation ;
- contraintes d'unicité lorsqu'elles expriment une vraie règle ;
- timestamps cohérents ;
- éviter les suppressions en cascade non maîtrisées ;
- préférer l'archivage ou les statuts lorsque la traçabilité l'exige.

Champs communs à prévoir lorsque pertinents :

- `created_at` ;
- `updated_at` ;
- `created_by`.

## 5. Architecture métier conceptuelle

Entités futures principales :

- User / Role / Permission ;
- Prospect ;
- Client ;
- EventType ;
- Event ;
- Service ;
- Menu ;
- Pack ;
- QuoteRequest ;
- Quote ;
- QuoteLine ;
- Order ;
- Payment ;
- Invoice ;
- StockItem ;
- StockMovement ;
- Supplier ;
- Purchase ;
- Equipment ;
- EquipmentReservation ;
- StaffMember ;
- EventAssignment ;
- GalleryItem ;
- AppSetting.

Cette liste est conceptuelle pour le cadrage. Elle ne constitue pas une instruction d'implémentation immédiate.

## 6. RBAC

Rôles minimums :

- `SUPER_ADMIN`
- `ADMIN`
- `COMMERCIAL`
- `CUISINE`
- `LOGISTIQUE`
- `COMPTABILITE`
- `PERSONNEL`

Principes :

- aucun utilisateur standard ne reçoit automatiquement les droits administrateur ;
- les contrôles d'accès sont effectués côté serveur ;
- les permissions doivent être extensibles ;
- masquer un bouton n'est jamais une mesure de sécurité suffisante ;
- les futurs tests doivent couvrir les permissions critiques.

## 7. Argent

Devise principale : **XAF / FCFA**.

- Jamais de `float` pour l'argent.
- Utiliser `Decimal` côté Python.
- Utiliser `NUMERIC`/`DECIMAL` approprié en base.
- Centraliser arrondis et calculs.
- Recalculer les totaux à partir des lignes et règles métier fiables.

## 8. Dates et heures

L'activité initiale est au Cameroun.

- Centraliser les conversions temporelles.
- Éviter les conversions improvisées dans les routes/templates.
- Définir une convention claire entre stockage et affichage lors du PROMPT 1.

## 9. Sécurité

Prévoir :

- hash de mot de passe robuste ;
- Flask-Login ou équivalent ;
- protection CSRF ;
- validation serveur ;
- contrôles RBAC serveur ;
- secrets par variables d'environnement ;
- validation des fichiers uploadés ;
- noms de fichiers sécurisés ;
- limitation des extensions et tailles ;
- aucun secret réel dans Git.

## 10. Uploads

Les uploads concerneront notamment plats, menus, galerie et événements.

À terme :

- extensions autorisées explicites ;
- contrôle de taille ;
- renommage sécurisé ;
- organisation par catégorie ou contexte ;
- chemin de stockage configurable ;
- jamais de confiance dans le nom fourni par l'utilisateur.

## 11. Configuration applicative

Les éléments suivants doivent être centralisés :

- nom commercial ;
- logo ;
- téléphone ;
- WhatsApp ;
- email ;
- adresse ;
- réseaux sociaux ;
- devise ;
- conditions commerciales.

Le numéro WhatsApp ne doit pas être hardcodé dans plusieurs templates.

## 12. Déploiement

Cible initiale : **PythonAnywhere**.

La future documentation `docs/PYTHONANYWHERE.md` couvrira :

- virtualenv ;
- requirements ;
- MySQL ;
- variables d'environnement ;
- migrations ;
- WSGI ;
- fichiers statiques ;
- uploads ;
- procédure de mise à jour.
