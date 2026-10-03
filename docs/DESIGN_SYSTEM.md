# Design System — WATO EVENTS

## Direction artistique

WATO EVENTS adopte une identité premium, chaleureuse et contemporaine, avec une influence africaine subtile portée par les matières, les contrastes et la sobriété plutôt que par des motifs clichés.

## Palette

Les couleurs sont centralisées dans `app/static/css/app.css`.

| Token | Valeur | Usage |
|---|---|---|
| `--wato-green` | `#173f35` | marque, boutons, sections fortes |
| `--wato-green-dark` | `#0e2b24` | footer, contrastes |
| `--wato-gold` | `#c79a4a` | accent premium, CTA |
| `--wato-gold-dark` | `#9a7435` | texte accent |
| `--wato-cream` | `#f7f2e8` | fonds chaleureux |
| `--wato-ivory` | `#fffdf8` | fond principal |
| `--wato-charcoal` | `#252824` | texte principal |

## Typographie

Deux familles logiques maximum :

- titres : Georgia / Times New Roman / serif ;
- interface et texte : pile système sans-serif.

Aucune police distante n'est indispensable au fonctionnement.

## Logo

Le site utilise actuellement un **wordmark temporaire** WATO EVENTS accompagné du monogramme WE. Il ne constitue pas le logo définitif.

Le futur logo pourra remplacer le composant de marque par un fichier local `logo.svg` ou `logo.png`.

## Boutons

- `.btn-primary` : action principale institutionnelle ;
- `.btn-gold` : CTA conversion fort ;
- `.btn-outline` : action secondaire ;
- `.btn-outline-light` : action secondaire sur fond sombre.

Tous les boutons conservent une zone tactile adaptée au mobile et un focus visible.

## Cards

Rayons généreux mais sobres, ombres légères et bordures fines. Le contenu reste prioritaire sur les effets.

## Responsive

Approche mobile-first avec points de rupture principaux autour de :

- 600 px ;
- 860 px ;
- 980 px.

Cibles prioritaires : 360, 375, 390, 412 px, puis tablette et desktop.

## Images

Les SVG présents dans `app/static/images/` sont des **visuels temporaires locaux**.

Ils doivent être remplacés progressivement par les vraies photos WATO EVENTS en conservant :

- ratios ;
- `object-fit: cover` ;
- dimensions explicites ;
- textes alternatifs ;
- lazy loading hors visuel principal.

## Mouvement

Animations légères uniquement : apparition douce et micro-interactions. `prefers-reduced-motion` est respecté.

## Accessibilité

- skip link ;
- focus visible ;
- HTML sémantique ;
- navigation clavier ;
- contrastes lisibles ;
- alt sur images ;
- labels sur formulaires ;
- pas de contenu critique uniquement transmis par la couleur.
