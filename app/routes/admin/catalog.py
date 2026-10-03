from decimal import Decimal

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from ...extensions import db
from ...forms.catalog import (
    CategoryForm,
    DishForm,
    MenuForm,
    PackForm,
    ServiceForm,
)
from ...models.catalog import (
    Category,
    CategoryType,
    Dish,
    Menu,
    MenuItem,
    Pack,
    PackDish,
    PackMenu,
    PackService,
    PricingUnit,
    Service,
)
from ...utils.catalog import unique_slug
from ...utils.files import save_catalog_image
from ...services.rbac import permission_required
from ...services.audit import AuditService
from flask_login import current_user
from . import catalog_admin_bp


@catalog_admin_bp.get("/")
@permission_required("catalog.view")
def dashboard():
    counts = {
        "categories": db.session.scalar(select(db.func.count(Category.id))) or 0,
        "services": db.session.scalar(select(db.func.count(Service.id))) or 0,
        "dishes": db.session.scalar(select(db.func.count(Dish.id))) or 0,
        "menus": db.session.scalar(select(db.func.count(Menu.id))) or 0,
        "packs": db.session.scalar(select(db.func.count(Pack.id))) or 0,
    }
    return render_template("admin/catalog/dashboard.html", counts=counts)


def _apply_common(item, form, price_field: str):
    item.name = form.name.data.strip()
    item.slug = unique_slug(type(item), form.slug.data or item.name, item.id)
    item.short_description = form.short_description.data or None
    item.description = form.description.data or None
    item.pricing_unit = form.pricing_unit.data
    price = getattr(form, price_field).data
    setattr(
        item,
        price_field,
        None if form.pricing_unit.data == PricingUnit.ON_REQUEST.value else price,
    )
    item.is_featured = bool(form.is_featured.data)
    item.is_active = bool(form.is_active.data)
    item.is_public = bool(form.is_public.data)
    item.display_order = form.display_order.data or 0

    image_path = save_catalog_image(form.image.data)
    if image_path:
        item.image_path = image_path


def _commit_or_flash(message: str):
    try:
        db.session.commit()
        flash(message, "success")
        return True
    except IntegrityError:
        db.session.rollback()
        flash("Impossible d’enregistrer : une contrainte du catalogue est violée.", "error")
        return False


@catalog_admin_bp.get("/categories")
@permission_required("catalog.view")
def category_list():
    items = db.session.scalars(
        select(Category).order_by(Category.category_type, Category.display_order, Category.name)
    ).all()
    return render_template("admin/catalog/list.html", kind="categories", title="Catégories", items=items)


@catalog_admin_bp.route("/categories/new", methods=["GET", "POST"])
@permission_required("catalog.edit")
def category_create():
    form = CategoryForm()
    if form.validate_on_submit():
        item = Category(
            name=form.name.data.strip(),
            slug=unique_slug(Category, form.slug.data or form.name.data),
            description=form.description.data or None,
            category_type=form.category_type.data,
            display_order=form.display_order.data or 0,
            is_active=bool(form.is_active.data),
        )
        db.session.add(item)
        if _commit_or_flash("Catégorie créée."):
            return redirect(url_for("catalog_admin.category_list"))
    return render_template("admin/catalog/form.html", form=form, title="Nouvelle catégorie")


@catalog_admin_bp.route("/categories/<int:item_id>/edit", methods=["GET", "POST"])
@permission_required("catalog.edit")
def category_edit(item_id):
    item = db.get_or_404(Category, item_id)
    form = CategoryForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data.strip()
        item.slug = unique_slug(Category, form.slug.data or item.name, item.id)
        item.description = form.description.data or None
        item.category_type = form.category_type.data
        item.display_order = form.display_order.data or 0
        item.is_active = bool(form.is_active.data)
        if _commit_or_flash("Catégorie mise à jour."):
            return redirect(url_for("catalog_admin.category_list"))
    return render_template("admin/catalog/form.html", form=form, title="Modifier la catégorie")


@catalog_admin_bp.get("/services")
@permission_required("catalog.view")
def service_list():
    items = db.session.scalars(select(Service).order_by(Service.display_order, Service.name)).all()
    return render_template("admin/catalog/list.html", kind="services", title="Services", items=items)


@catalog_admin_bp.route("/services/new", methods=["GET", "POST"])
@permission_required("catalog.edit")
def service_create():
    form = ServiceForm()
    if form.validate_on_submit():
        item = Service()
        _apply_common(item, form, "base_price")
        db.session.add(item)
        if _commit_or_flash("Service créé."):
            return redirect(url_for("catalog_admin.service_list"))
    return render_template("admin/catalog/form.html", form=form, title="Nouveau service")


@catalog_admin_bp.route("/services/<int:item_id>/edit", methods=["GET", "POST"])
@permission_required("catalog.edit")
def service_edit(item_id):
    item = db.get_or_404(Service, item_id)
    form = ServiceForm(obj=item)
    if form.validate_on_submit():
        _apply_common(item, form, "base_price")
        if _commit_or_flash("Service mis à jour."):
            return redirect(url_for("catalog_admin.service_list"))
    return render_template("admin/catalog/form.html", form=form, title="Modifier le service", item=item)


@catalog_admin_bp.get("/plats")
@permission_required("catalog.view")
def dish_list():
    items = db.session.scalars(
        select(Dish).options(selectinload(Dish.category)).order_by(Dish.display_order, Dish.name)
    ).all()
    return render_template("admin/catalog/list.html", kind="dishes", title="Plats", items=items)


def _dish_category_choices():
    categories = db.session.scalars(
        select(Category)
        .where(Category.category_type == CategoryType.DISH.value, Category.is_active.is_(True))
        .order_by(Category.display_order, Category.name)
    ).all()
    return [(0, "— Sans catégorie —")] + [(item.id, item.name) for item in categories]


@catalog_admin_bp.route("/plats/new", methods=["GET", "POST"])
@permission_required("catalog.edit")
def dish_create():
    form = DishForm()
    form.category_id.choices = _dish_category_choices()
    if form.validate_on_submit():
        item = Dish()
        _apply_common(item, form, "base_price")
        item.category_id = form.category_id.data or None
        db.session.add(item)
        if _commit_or_flash("Plat créé."):
            return redirect(url_for("catalog_admin.dish_list"))
    return render_template("admin/catalog/form.html", form=form, title="Nouveau plat")


@catalog_admin_bp.route("/plats/<int:item_id>/edit", methods=["GET", "POST"])
@permission_required("catalog.edit")
def dish_edit(item_id):
    item = db.get_or_404(Dish, item_id)
    form = DishForm(obj=item)
    form.category_id.choices = _dish_category_choices()
    if request.method == "GET":
        form.category_id.data = item.category_id or 0
    if form.validate_on_submit():
        _apply_common(item, form, "base_price")
        item.category_id = form.category_id.data or None
        if _commit_or_flash("Plat mis à jour."):
            return redirect(url_for("catalog_admin.dish_list"))
    return render_template("admin/catalog/form.html", form=form, title="Modifier le plat", item=item)


def _published_choices(model):
    items = db.session.scalars(select(model).order_by(model.display_order, model.name)).all()
    return [(item.id, item.name) for item in items]


def _sync_menu_items(menu: Menu, dish_ids: list[int]):
    dishes = db.session.scalars(select(Dish).where(Dish.id.in_(dish_ids))).all() if dish_ids else []
    valid_ids = {dish.id for dish in dishes}
    if valid_ids != set(dish_ids):
        raise ValueError("Un plat sélectionné est invalide.")
    menu.items.clear()
    for order, dish in enumerate(dishes):
        menu.items.append(MenuItem(dish=dish, display_order=order, quantity=Decimal("1.00")))


@catalog_admin_bp.get("/menus")
@permission_required("catalog.view")
def menu_list():
    items = db.session.scalars(
        select(Menu).options(selectinload(Menu.items).selectinload(MenuItem.dish)).order_by(Menu.display_order, Menu.name)
    ).unique().all()
    return render_template("admin/catalog/list.html", kind="menus", title="Menus", items=items)


@catalog_admin_bp.route("/menus/new", methods=["GET", "POST"])
@permission_required("catalog.edit")
def menu_create():
    form = MenuForm()
    form.dish_ids.choices = _published_choices(Dish)
    if form.validate_on_submit():
        item = Menu()
        _apply_common(item, form, "price")
        item.minimum_people = form.minimum_people.data
        db.session.add(item)
        _sync_menu_items(item, form.dish_ids.data)
        if _commit_or_flash("Menu créé."):
            return redirect(url_for("catalog_admin.menu_list"))
    return render_template("admin/catalog/form.html", form=form, title="Nouveau menu")


@catalog_admin_bp.route("/menus/<int:item_id>/edit", methods=["GET", "POST"])
@permission_required("catalog.edit")
def menu_edit(item_id):
    item = db.session.get(Menu, item_id)
    if item is None:
        abort(404)
    form = MenuForm(obj=item)
    form.dish_ids.choices = _published_choices(Dish)
    if request.method == "GET":
        form.dish_ids.data = [link.dish_id for link in item.items]
    if form.validate_on_submit():
        _apply_common(item, form, "price")
        item.minimum_people = form.minimum_people.data
        _sync_menu_items(item, form.dish_ids.data)
        if _commit_or_flash("Menu mis à jour."):
            return redirect(url_for("catalog_admin.menu_list"))
    return render_template("admin/catalog/form.html", form=form, title="Modifier le menu", item=item)


def _sync_pack(pack: Pack, dish_ids: list[int], menu_ids: list[int], service_ids: list[int]):
    dishes = db.session.scalars(select(Dish).where(Dish.id.in_(dish_ids))).all() if dish_ids else []
    menus = db.session.scalars(select(Menu).where(Menu.id.in_(menu_ids))).all() if menu_ids else []
    services = db.session.scalars(select(Service).where(Service.id.in_(service_ids))).all() if service_ids else []
    if {item.id for item in dishes} != set(dish_ids):
        raise ValueError("Un plat sélectionné est invalide.")
    if {item.id for item in menus} != set(menu_ids):
        raise ValueError("Un menu sélectionné est invalide.")
    if {item.id for item in services} != set(service_ids):
        raise ValueError("Un service sélectionné est invalide.")

    pack.dish_items.clear()
    pack.menu_items.clear()
    pack.service_items.clear()
    for order, item in enumerate(dishes):
        pack.dish_items.append(PackDish(dish=item, display_order=order, quantity=Decimal("1.00")))
    for order, item in enumerate(menus):
        pack.menu_items.append(PackMenu(menu=item, display_order=order, quantity=Decimal("1.00")))
    for order, item in enumerate(services):
        pack.service_items.append(PackService(service=item, display_order=order, quantity=Decimal("1.00")))


@catalog_admin_bp.get("/packs")
@permission_required("catalog.view")
def pack_list():
    items = db.session.scalars(select(Pack).order_by(Pack.display_order, Pack.name)).all()
    return render_template("admin/catalog/list.html", kind="packs", title="Packs", items=items)


@catalog_admin_bp.route("/packs/new", methods=["GET", "POST"])
@permission_required("catalog.edit")
def pack_create():
    form = PackForm()
    form.dish_ids.choices = _published_choices(Dish)
    form.menu_ids.choices = _published_choices(Menu)
    form.service_ids.choices = _published_choices(Service)
    if form.validate_on_submit():
        item = Pack()
        _apply_common(item, form, "price")
        item.minimum_people = form.minimum_people.data
        db.session.add(item)
        _sync_pack(item, form.dish_ids.data, form.menu_ids.data, form.service_ids.data)
        if _commit_or_flash("Pack créé."):
            return redirect(url_for("catalog_admin.pack_list"))
    return render_template("admin/catalog/form.html", form=form, title="Nouveau pack")


@catalog_admin_bp.route("/packs/<int:item_id>/edit", methods=["GET", "POST"])
@permission_required("catalog.edit")
def pack_edit(item_id):
    item = db.session.get(Pack, item_id)
    if item is None:
        abort(404)
    form = PackForm(obj=item)
    form.dish_ids.choices = _published_choices(Dish)
    form.menu_ids.choices = _published_choices(Menu)
    form.service_ids.choices = _published_choices(Service)
    if request.method == "GET":
        form.dish_ids.data = [link.dish_id for link in item.dish_items]
        form.menu_ids.data = [link.menu_id for link in item.menu_items]
        form.service_ids.data = [link.service_id for link in item.service_items]
    if form.validate_on_submit():
        _apply_common(item, form, "price")
        item.minimum_people = form.minimum_people.data
        _sync_pack(item, form.dish_ids.data, form.menu_ids.data, form.service_ids.data)
        if _commit_or_flash("Pack mis à jour."):
            return redirect(url_for("catalog_admin.pack_list"))
    return render_template("admin/catalog/form.html", form=form, title="Modifier le pack", item=item)


@catalog_admin_bp.post("/<kind>/<int:item_id>/toggle/<field>")
@permission_required("catalog.validate")
def toggle(kind, item_id, field):
    mapping = {
        "services": Service,
        "dishes": Dish,
        "menus": Menu,
        "packs": Pack,
        "categories": Category,
    }
    if kind not in mapping or field not in {"is_active", "is_public", "is_featured"}:
        abort(404)
    if kind == "categories" and field != "is_active":
        abort(404)

    item = db.get_or_404(mapping[kind], item_id)
    setattr(item, field, not bool(getattr(item, field)))
    AuditService.log("catalog.state_change", type(item).__name__, item.id, f"{field} modifié", user=current_user)
    if _commit_or_flash("État mis à jour."):
        return redirect(request.referrer or url_for("catalog_admin.dashboard"))
    return redirect(request.referrer or url_for("catalog_admin.dashboard"))
