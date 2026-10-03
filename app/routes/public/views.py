from flask import abort, current_app, jsonify, render_template
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ...extensions import db
from ...models.catalog import Menu, MenuItem, Pack, PackDish, PackMenu, PackService, Service
from ...presentation import (
    CULINARY_CATEGORIES,
    EVENT_TYPES,
    GALLERY_ITEMS,
    PROCESS_STEPS,
    SERVICES as EDITORIAL_SERVICES,
    WHY_US,
)
from ...services.catalog import CatalogService
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
    featured_services = CatalogService.public_services(featured=True)
    featured_menus = CatalogService.public_menus(featured=True)
    featured_packs = CatalogService.public_packs(featured=True)

    return render_template(
        "public/home.html",
        **_page_context(
            "Traiteur & Événementiel à Yaoundé",
            "WATO EVENTS accompagne vos réceptions à Yaoundé avec une approche culinaire et événementielle professionnelle.",
            featured_services=featured_services,
            featured_menus=featured_menus,
            featured_packs=featured_packs,
            editorial_services=EDITORIAL_SERVICES,
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
    items = CatalogService.public_services()
    return render_template(
        "public/services.html",
        **_page_context(
            "Nos services",
            "Mariages, cérémonies, buffets, cocktails et événements d’entreprise : découvrez les prestations WATO EVENTS à Yaoundé.",
            services=items,
        ),
    )


@public_bp.get("/services/<slug>")
def service_detail(slug):
    item = db.session.scalar(
        select(Service).where(
            Service.slug == slug,
            Service.is_active.is_(True),
            Service.is_public.is_(True),
        )
    )
    if item is None:
        abort(404)
    return render_template(
        "public/service_detail.html",
        **_page_context(
            item.name,
            item.short_description or f"Découvrez la prestation {item.name} proposée par WATO EVENTS à Yaoundé.",
            service=item,
        ),
    )


@public_bp.get("/menus")
def menus():
    items = CatalogService.public_menus()
    packs = CatalogService.public_packs()
    return render_template(
        "public/menus.html",
        **_page_context(
            "Menus & expérience culinaire",
            "Explorez les menus et offres culinaires publiés par WATO EVENTS à Yaoundé.",
            menus=items,
            packs=packs,
            culinary_categories=CULINARY_CATEGORIES,
        ),
    )


@public_bp.get("/menus/<slug>")
def menu_detail(slug):
    item = db.session.scalar(
        select(Menu)
        .options(selectinload(Menu.items).selectinload(MenuItem.dish))
        .where(
            Menu.slug == slug,
            Menu.is_active.is_(True),
            Menu.is_public.is_(True),
        )
    )
    if item is None:
        abort(404)
    return render_template(
        "public/menu_detail.html",
        **_page_context(
            item.name,
            item.short_description or f"Découvrez le menu {item.name} de WATO EVENTS.",
            menu=item,
        ),
    )


@public_bp.get("/packs")
def packs():
    items = CatalogService.public_packs()
    return render_template(
        "public/packs.html",
        **_page_context(
            "Packs événementiels",
            "Découvrez les packs publiés par WATO EVENTS pour simplifier l’organisation de votre réception.",
            packs=items,
        ),
    )


@public_bp.get("/packs/<slug>")
def pack_detail(slug):
    item = db.session.scalar(
        select(Pack)
        .options(
            selectinload(Pack.dish_items).selectinload(PackDish.dish),
            selectinload(Pack.menu_items).selectinload(PackMenu.menu),
            selectinload(Pack.service_items).selectinload(PackService.service),
        )
        .where(
            Pack.slug == slug,
            Pack.is_active.is_(True),
            Pack.is_public.is_(True),
        )
    )
    if item is None:
        abort(404)
    return render_template(
        "public/pack_detail.html",
        **_page_context(
            item.name,
            item.short_description or f"Découvrez le pack {item.name} de WATO EVENTS.",
            pack=item,
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
