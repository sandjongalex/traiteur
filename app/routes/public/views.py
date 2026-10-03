from flask import current_app, jsonify, render_template

from ...presentation import (
    CULINARY_CATEGORIES,
    EVENT_TYPES,
    GALLERY_ITEMS,
    PROCESS_STEPS,
    SERVICES,
    WHY_US,
)
from . import public_bp


def _page_context(title: str, description: str, **extra):
    context = {
        "page_title": title,
        "meta_description": description,
    }
    context.update(extra)
    return context


@public_bp.get("/")
def index():
    return render_template(
        "public/home.html",
        **_page_context(
            "Traiteur & Événementiel à Yaoundé",
            "WATO EVENTS accompagne vos réceptions à Yaoundé avec une approche culinaire et événementielle professionnelle.",
            services=SERVICES,
            culinary_categories=CULINARY_CATEGORIES,
            event_types=EVENT_TYPES,
            process_steps=PROCESS_STEPS,
            why_us=WHY_US,
            gallery_items=GALLERY_ITEMS[:4],
        ),
    )


@public_bp.get("/a-propos")
def about():
    return render_template(
        "public/about.html",
        **_page_context(
            "À propos",
            "Découvrez l’approche WATO EVENTS : une expérience traiteur et événementielle professionnelle à Yaoundé.",
            why_us=WHY_US,
        ),
    )


@public_bp.get("/services")
def services():
    return render_template(
        "public/services.html",
        **_page_context(
            "Nos services",
            "Mariages, cérémonies, buffets, cocktails et événements d’entreprise : découvrez les prestations WATO EVENTS à Yaoundé.",
            services=SERVICES,
        ),
    )


@public_bp.get("/menus")
def menus():
    return render_template(
        "public/menus.html",
        **_page_context(
            "Menus & expérience culinaire",
            "Explorez l’univers culinaire WATO EVENTS. Le catalogue détaillé des menus sera enrichi prochainement.",
            culinary_categories=CULINARY_CATEGORIES,
        ),
    )


@public_bp.get("/realisations")
def gallery():
    return render_template(
        "public/gallery.html",
        **_page_context(
            "Nos réalisations",
            "Aperçu visuel de l’univers WATO EVENTS et de nos formats de réception à Yaoundé.",
            gallery_items=GALLERY_ITEMS,
        ),
    )


@public_bp.get("/contact")
def contact():
    return render_template(
        "public/contact.html",
        **_page_context(
            "Contact",
            "Contactez WATO EVENTS à Yaoundé pour parler de votre réception ou de votre besoin traiteur.",
        ),
    )


@public_bp.get("/demande-de-devis")
def quote_request():
    return render_template(
        "public/quote_request.html",
        **_page_context(
            "Demander un devis",
            "Préparez votre demande de devis WATO EVENTS : événement, date, lieu, invités, menus et options.",
            event_types=EVENT_TYPES,
        ),
    )


@public_bp.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "application": current_app.config["APP_NAME"],
        }
    )
