from secrets import token_urlsafe

from flask import (
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ...extensions import db
from ...forms.quote_request import QuoteRequestForm
from ...models.catalog import (
    Menu,
    MenuItem,
    Pack,
    PackDish,
    PackMenu,
    PackService,
    PricingUnit,
    Service,
)
from ...models.quote_request import QuoteRequest, QuoteRequestItemType
from ...presentation import (
    CULINARY_CATEGORIES,
    EVENT_TYPES,
    GALLERY_ITEMS,
    PROCESS_STEPS,
    SERVICES as EDITORIAL_SERVICES,
    WHY_US,
)
from ...services.catalog import CatalogService
from ...services.pricing import PricingError, PricingService
from ...services.quote_requests import DuplicateSubmissionError, QuoteRequestService
from . import public_bp


def _page_context(title: str, description: str, **extra):
    context = {
        "page_title": title,
        "meta_description": description,
    }
    context.update(extra)
    return context


def _selection_from_form():
    selections = []
    field_map = {
        QuoteRequestItemType.SERVICE.value: "service_ids",
        QuoteRequestItemType.MENU.value: "menu_ids",
        QuoteRequestItemType.PACK.value: "pack_ids",
    }
    for item_type, field_name in field_map.items():
        for raw_id in request.form.getlist(field_name):
            try:
                item_id = int(raw_id)
            except (TypeError, ValueError):
                raise PricingError("Sélection catalogue invalide.")
            quantity = request.form.get(
                f"quantity_{item_type.lower()}_{item_id}", "1"
            )
            selections.append(
                {
                    "item_type": item_type,
                    "item_id": item_id,
                    "quantity": quantity,
                }
            )
    return selections


def _catalog_for_configurator():
    return {
        "services": CatalogService.public_services(),
        "menus": CatalogService.public_menus(),
        "packs": CatalogService.public_packs(),
    }


def _preselected_ids():
    selected = {"services": set(), "menus": set(), "packs": set()}
    lookups = [
        ("service", Service, "services"),
        ("menu", Menu, "menus"),
        ("pack", Pack, "packs"),
    ]
    for query_name, model, key in lookups:
        slug = request.args.get(query_name, "").strip()
        if not slug:
            continue
        item = db.session.scalar(
            select(model).where(
                model.slug == slug,
                model.is_active.is_(True),
                model.is_public.is_(True),
            )
        )
        if item is not None:
            selected[key].add(item.id)
    return selected


@public_bp.get("/")
def index():
    homepage_services = CatalogService.public_services()[:4]
    featured_menus = CatalogService.public_menus(featured=True)
    featured_packs = CatalogService.public_packs(featured=True)

    return render_template(
        "public/home.html",
        **_page_context(
            "Traiteur & Événementiel à Yaoundé",
            "DNP DECO accompagne vos réceptions à Yaoundé avec une approche culinaire et événementielle professionnelle.",
            homepage_services=homepage_services,
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
            "Découvrez l’approche DNP DECO : une expérience traiteur et événementielle professionnelle à Yaoundé.",
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
            "Mariages, cérémonies, buffets, cocktails et événements d’entreprise : découvrez les prestations DNP DECO à Yaoundé.",
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
            item.short_description
            or f"Découvrez la prestation {item.name} proposée par DNP DECO à Yaoundé.",
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
            "Explorez les menus et offres culinaires publiés par DNP DECO à Yaoundé.",
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
            item.short_description or f"Découvrez le menu {item.name} de DNP DECO.",
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
            "Découvrez les packs publiés par DNP DECO pour simplifier l’organisation de votre réception.",
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
            item.short_description or f"Découvrez le pack {item.name} de DNP DECO.",
            pack=item,
        ),
    )


@public_bp.get("/realisations")
def gallery():
    return render_template(
        "public/gallery.html",
        **_page_context(
            "Nos réalisations",
            "Aperçu visuel de l’univers DNP DECO et de nos formats de réception à Yaoundé.",
            gallery_items=GALLERY_ITEMS,
        ),
    )


@public_bp.get("/contact")
def contact():
    return render_template(
        "public/contact.html",
        **_page_context(
            "Contact",
            "Contactez DNP DECO à Yaoundé pour parler de votre réception ou de votre besoin traiteur.",
        ),
    )


@public_bp.route("/demande-de-devis", methods=["GET", "POST"])
def quote_request():
    catalog = _catalog_for_configurator()
    form = QuoteRequestForm()

    if request.method == "GET":
        form.submission_token.data = token_urlsafe(24)
        preselected = _preselected_ids()
    else:
        preselected = {
            "services": {int(v) for v in request.form.getlist("service_ids") if v.isdigit()},
            "menus": {int(v) for v in request.form.getlist("menu_ids") if v.isdigit()},
            "packs": {int(v) for v in request.form.getlist("pack_ids") if v.isdigit()},
        }

    if form.validate_on_submit():
        try:
            selections = _selection_from_form()
            estimate = PricingService.estimate_selection(
                selections,
                guest_count=form.guest_count.data,
                currency=current_app.config.get("CURRENCY", "XAF"),
            )
            saved = QuoteRequestService.create_from_public(
                form=form,
                estimate=estimate,
                submission_token=form.submission_token.data,
            )
            return redirect(
                url_for(
                    "public.quote_request_confirmation",
                    reference=saved.reference,
                    token=saved.public_token,
                )
            )
        except PricingError as exc:
            flash(str(exc), "error")
        except DuplicateSubmissionError:
            existing = db.session.scalar(
                select(QuoteRequest).where(
                    QuoteRequest.submission_token == form.submission_token.data
                )
            )
            if existing is not None:
                return redirect(
                    url_for(
                        "public.quote_request_confirmation",
                        reference=existing.reference,
                        token=existing.public_token,
                    )
                )
            flash("Cette demande a déjà été envoyée.", "error")

    return render_template(
        "public/quote_request.html",
        **_page_context(
            "Configurer mon événement",
            "Configurez votre événement et obtenez une estimation indicative avant d’envoyer votre demande à DNP DECO.",
            form=form,
            services=catalog["services"],
            menus=catalog["menus"],
            packs=catalog["packs"],
            preselected=preselected,
            pricing_unit=PricingUnit,
        ),
    )


@public_bp.get("/demande-de-devis/confirmation/<reference>/<token>")
def quote_request_confirmation(reference, token):
    saved = db.session.scalar(
        select(QuoteRequest).where(
            QuoteRequest.reference == reference,
            QuoteRequest.public_token == token,
        )
    )
    if saved is None:
        abort(404)
    return render_template(
        "public/quote_request_confirmation.html",
        **_page_context(
            "Demande enregistrée",
            "Confirmation d’enregistrement de votre demande DNP DECO.",
            quote_request=saved,
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
