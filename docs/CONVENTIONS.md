# Conventions de développement — WATO EVENTS

## 1. Travail incrémental

Avant chaque modification :

1. inspecter le dépôt ;
2. comprendre l'existant ;
3. vérifier migrations et tests ;
4. préserver les fonctionnalités existantes ;
5. limiter le changement au périmètre du sprint.

## 2. Git

- Commits courts et explicites.
- Ne pas mélanger refactor massif et fonctionnalité sans nécessité.
- Ne pas supprimer une fonctionnalité existante sans justification documentée.
- Vérifier le diff avant fin de sprint.

## 3. Python

- Noms explicites en anglais dans le code.
- Fonctions courtes lorsque possible.
- Une responsabilité principale par fonction/service.
- Éviter les effets de bord cachés.
- Préférer des constantes ou enums pour les statuts.
- Type hints lorsque cela améliore la lisibilité.

## 4. Flask

- Application factory `create_app()`.
- Extensions initialisées hors de l'application puis liées dans la factory.
- Blueprints pour séparer les surfaces/domaines.
- Pas de logique métier importante dans les routes.
- Pas de requêtes métier complexes directement dans les templates.

## 5. SQLAlchemy et migrations

- Migrations obligatoires en production.
- Ne pas utiliser `db.create_all()` comme mécanisme d'évolution du schéma.
- Définir les relations explicitement.
- Ajouter index et contraintes en fonction des accès réels.
- Éviter les suppressions destructrices accidentelles.

## 6. Argent

- `Decimal` côté Python.
- `NUMERIC`/`DECIMAL` côté SQL.
- Jamais de `float` pour les montants.
- Centraliser les règles d'arrondi.
- Tester les calculs de total, remise, acompte, paiement, solde et marge.

## 7. Dates et heures

- Définir une convention commune pour stockage et affichage.
- Centraliser les transformations.
- Ne pas disperser de conversions manuelles dans les templates.

## 8. Sécurité

- Aucun secret réel dans le dépôt.
- Secrets par variables d'environnement.
- CSRF activé pour les formulaires concernés.
- Contrôle d'accès serveur systématique.
- Validation serveur des entrées.
- Hash de mots de passe sécurisé.
- Uploads validés et renommés côté serveur.

## 9. Fichiers de configuration

`.env.example` documente uniquement les noms de variables avec valeurs factices ou vides.

Exemples d'informations configurables :

- environnement Flask ;
- secret de session ;
- URL MySQL ;
- nom WATO EVENTS ;
- téléphone ;
- WhatsApp ;
- email ;
- adresse ;
- devise ;
- limites d'upload.

## 10. UI/UX

- Mobile first.
- Bootstrap 5.
- Contraste et lisibilité prioritaires.
- Site public visuel et orienté conversion.
- Back-office dense mais non surchargé.
- Actions principales accessibles facilement sur smartphone.

## 11. Tests

Ajouter progressivement :

- tests modèles ;
- tests services ;
- tests routes ;
- tests permissions ;
- tests calculs ;
- tests de non-régression.

Une fonctionnalité critique n'est pas terminée si son scénario principal et ses cas d'erreur essentiels ne sont pas testés.

## 12. Documentation

Chaque sprint doit :

- mettre à jour la documentation affectée ;
- documenter les migrations ou commandes nécessaires ;
- signaler les décisions architecturales ;
- résumer les tests effectués ;
- annoncer la prochaine étape sans la démarrer automatiquement.
