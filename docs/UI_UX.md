# UI / UX — DNP DECO

## Direction
DNP DECO utilise une direction premium, chaleureuse et professionnelle adaptée à un service de traiteur et d’événementiel à Yaoundé. Le public privilégie l’émotion, la gastronomie et la conversion ; le back-office privilégie la clarté, la vitesse et la lisibilité.

## Design tokens
Les tokens centraux résident dans `app/static/css/app.css` :
- couleurs sémantiques `--color-*` ;
- espacements `--space-1` à `--space-10` ;
- rayons `--radius-*` ;
- ombres `--shadow-*` ;
- hauteur standard des contrôles `--control-h` ;
- transitions `--transition-*`.

Les anciens tokens `--wato-*` restent aliasés pour préserver la compatibilité avec les templates existants.

## Palette
- vert profond : identité et actions principales ;
- or/champagne : accent premium ;
- ivoire/crème : fonds chaleureux ;
- anthracite : texte principal ;
- couleurs sémantiques success/info/warning/danger pour les états.

## Typographie
Deux familles maximum :
- titres : Georgia / Times New Roman / serif ;
- interface : pile système sans-serif.

Les tailles principales utilisent `clamp()` pour rester lisibles de 360 px au desktop.

## Boutons
Les variantes partagées sont :
- `.btn-primary`
- `.btn-secondary`
- `.btn-gold`
- `.btn-outline`
- `.btn-ghost`
- `.btn-danger`

Les cibles tactiles principales visent environ 44–48 px.

## Cards
Les cartes utilisent bordure fine, rayon généreux, ombre légère et élévation discrète au survol. Les images ont un ratio stable et `object-fit: cover`.

## Formulaires
Chaque champ conserve un label visible. Les erreurs restent proches du champ lorsqu’elles sont disponibles. Les contrôles partagent une hauteur, un rayon, un focus et des couleurs cohérents. L’upload catalogue affiche le visuel actuel lorsqu’il existe et rappelle les formats acceptés.

## Badges
Les états partagent les classes :
- `.badge-success`
- `.badge-info`
- `.badge-warning`
- `.badge-danger`
- `.badge-muted`

Les statuts QuoteRequest utilisent cette sémantique visuelle sans modifier leurs valeurs métier.

## Site public
Le hero met en avant :
- DNP DECO ;
- traiteur & événementiel à Yaoundé ;
- la signature « Vos moments, notre savoir-faire. » ;
- un CTA principal vers le configurateur ;
- un CTA secondaire vers les prestations.

Les services, menus et packs utilisent des cartes visuelles cohérentes. Une image de catalogue réelle est prioritaire ; sinon le placeholder local est utilisé.

## Configurateur
Les quatre étapes restent :
1. Événement
2. Prestations
3. Coordonnées
4. Récapitulatif

Les sélections sont présentées sous forme de cartes, l’estimation est mise en évidence, et une barre récapitulative mobile complète l’étape de sélection. La validation métier reste côté serveur.

## Back-office
Le back-office utilise :
- sidebar desktop ;
- drawer mobile ;
- topbar ;
- zone de contenu large ;
- navigation filtrée par permissions existantes ;
- cartes KPI ;
- tableaux transformés en cartes sur petits écrans ;
- actions rapides et états vides.

Le shell reste relié à l’identité DNP DECO sans reproduire le site marketing.

## Login
Le login adopte un split-screen sur desktop et un formulaire simple sur mobile. Aucune information sensible n’est affichée.

## Responsive
Cibles de contrôle :
- 360 px
- 390 px
- 412 px
- 768 px
- 1024 px
- 1366 px

Sous 680 px, les tableaux administratifs deviennent des cartes structurées plutôt qu’un tableau horizontal de grande largeur.

## Accessibilité
Principes appliqués :
- skip links ;
- focus visible ;
- labels explicites ;
- `aria-expanded` sur les menus ;
- fermeture clavier Escape ;
- `aria-live` pour les estimations/messages ;
- support `prefers-reduced-motion` ;
- contrastes sémantiques ;
- aucune information critique transmise uniquement par la couleur.

## Performance
Aucun framework SPA ni bibliothèque frontend lourde n’a été ajouté. Le JavaScript reste ciblé sur la navigation, le configurateur et le feedback de soumission.
