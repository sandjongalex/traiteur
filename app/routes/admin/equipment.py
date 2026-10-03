from __future__ import annotations

from decimal import Decimal

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from ...extensions import db
from ...forms.equipment import EquipmentCategoryForm, EquipmentForm, EquipmentMovementForm
from ...models.equipment import Equipment, EquipmentCategory, EquipmentMovement
from ...services.audit import AuditService
from ...services.equipment import EquipmentService
from ...services.rbac import permission_required
from ...utils.files import save_equipment_image
from . import equipment_admin_bp


def _category_choices():
    categories = db.session.scalars(
        select(EquipmentCategory)
        .where(EquipmentCategory.is_active.is_(True))
        .order_by(EquipmentCategory.name)
    ).all()
    return [(category.id, category.name) for category in categories]


def _commit_or_flash(success_message: str) -> bool:
    try:
        db.session.commit()
        flash(success_message, "success")
        return True
    except IntegrityError:
        db.session.rollback()
        flash("Impossible d’enregistrer : une contrainte est violée.", "error")
        return False


@equipment_admin_bp.get("/")
@permission_required("equipment.view")
def dashboard():
    items = EquipmentService.list_items()
    balances = {item.id: EquipmentService.balance(item) for item in items}
    total_types = len(items)
    total_units = sum((b.total for b in balances.values()), Decimal("0.00"))
    available_units = sum((b.available for b in balances.values()), Decimal("0.00"))
    out_units = sum((b.out for b in balances.values()), Decimal("0.00"))
    maintenance_units = sum((b.maintenance for b in balances.values()), Decimal("0.00"))
    return render_template(
        "admin/equipment/dashboard.html",
        items=items[:8],
        balances=balances,
        total_types=total_types,
        total_units=total_units,
        available_units=available_units,
        out_units=out_units,
        maintenance_units=maintenance_units,
    )


@equipment_admin_bp.get("/categories")
@permission_required("equipment.view")
def category_list():
    categories = db.session.scalars(
        select(EquipmentCategory).order_by(EquipmentCategory.name)
    ).all()
    return render_template("admin/equipment/categories.html", categories=categories)


@equipment_admin_bp.route("/categories/new", methods=["GET", "POST"])
@permission_required("equipment.create")
def category_create():
    form = EquipmentCategoryForm()
    if form.validate_on_submit():
        category = EquipmentCategory(
            name=form.name.data.strip(),
            code=form.code.data.strip().upper().replace(" ", "_"),
            description=(form.description.data or "").strip() or None,
            is_active=bool(form.is_active.data),
        )
        db.session.add(category)
        if _commit_or_flash("Catégorie matériel créée."):
            AuditService.log(
                "equipment.category_create", "EquipmentCategory", category.id,
                "Création catégorie matériel", user=current_user
            )
            db.session.commit()
            return redirect(url_for("equipment_admin.category_list"))
    return render_template("admin/equipment/form.html", form=form, title="Nouvelle catégorie")


@equipment_admin_bp.route("/categories/<int:item_id>/edit", methods=["GET", "POST"])
@permission_required("equipment.edit")
def category_edit(item_id):
    category = db.get_or_404(EquipmentCategory, item_id)
    form = EquipmentCategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data.strip()
        category.code = form.code.data.strip().upper().replace(" ", "_")
        category.description = (form.description.data or "").strip() or None
        category.is_active = bool(form.is_active.data)
        AuditService.log(
            "equipment.category_edit", "EquipmentCategory", category.id,
            "Modification catégorie matériel", user=current_user
        )
        if _commit_or_flash("Catégorie matériel mise à jour."):
            return redirect(url_for("equipment_admin.category_list"))
    return render_template("admin/equipment/form.html", form=form, title="Modifier la catégorie")


@equipment_admin_bp.get("/items")
@permission_required("equipment.view")
def item_list():
    items = EquipmentService.list_items()
    balances = {item.id: EquipmentService.balance(item) for item in items}
    return render_template("admin/equipment/items.html", items=items, balances=balances)


@equipment_admin_bp.route("/items/new", methods=["GET", "POST"])
@permission_required("equipment.create")
def item_create():
    form = EquipmentForm()
    form.category_id.choices = _category_choices()
    if not form.category_id.choices:
        flash("Créez d’abord une catégorie de matériel.", "error")
        return redirect(url_for("equipment_admin.category_create"))

    if form.validate_on_submit():
        image_path = None
        try:
            image_path = save_equipment_image(form.image.data)
        except ValueError as exc:
            form.image.errors.append(str(exc))
        else:
            item = Equipment(
                category_id=form.category_id.data,
                name=form.name.data.strip(),
                reference=(form.reference.data or "").strip() or None,
                description=(form.description.data or "").strip() or None,
                unit=form.unit.data.strip(),
                initial_quantity=form.initial_quantity.data,
                purchase_price=form.purchase_price.data,
                replacement_value=form.replacement_value.data,
                condition=form.condition.data,
                image_path=image_path,
                notes=(form.notes.data or "").strip() or None,
                is_active=bool(form.is_active.data),
            )
            db.session.add(item)
            try:
                db.session.flush()
                AuditService.log(
                    "equipment.create", "Equipment", item.id,
                    f"Création matériel : {item.name}", user=current_user
                )
                db.session.commit()
                flash("Matériel créé.", "success")
                return redirect(url_for("equipment_admin.item_detail", item_id=item.id))
            except IntegrityError:
                db.session.rollback()
                flash("Référence déjà utilisée ou données invalides.", "error")
    return render_template("admin/equipment/form.html", form=form, title="Nouveau matériel")


@equipment_admin_bp.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
@permission_required("equipment.edit")
def item_edit(item_id):
    item = db.session.scalar(
        select(Equipment)
        .where(Equipment.id == item_id)
        .options(selectinload(Equipment.movements))
    )
    if item is None:
        return ("", 404)

    form = EquipmentForm(obj=item)
    form.category_id.choices = _category_choices()
    if request.method == "GET":
        form.category_id.data = item.category_id

    if form.validate_on_submit():
        item.category_id = form.category_id.data
        item.name = form.name.data.strip()
        item.reference = (form.reference.data or "").strip() or None
        item.description = (form.description.data or "").strip() or None
        item.unit = form.unit.data.strip()
        if item.movements and form.initial_quantity.data != item.initial_quantity:
            flash(
                "La quantité initiale ne peut plus être modifiée après des mouvements. "
                "Utilisez un ajustement.",
                "error",
            )
            form.initial_quantity.data = item.initial_quantity
        else:
            item.initial_quantity = form.initial_quantity.data
        item.purchase_price = form.purchase_price.data
        item.replacement_value = form.replacement_value.data
        item.condition = form.condition.data
        item.notes = (form.notes.data or "").strip() or None
        item.is_active = bool(form.is_active.data)

        try:
            image_path = save_equipment_image(form.image.data)
            if image_path:
                item.image_path = image_path
        except ValueError as exc:
            form.image.errors.append(str(exc))
            return render_template("admin/equipment/form.html", form=form, title="Modifier le matériel")

        AuditService.log(
            "equipment.edit", "Equipment", item.id,
            f"Modification matériel : {item.name}", user=current_user
        )
        if _commit_or_flash("Matériel mis à jour."):
            return redirect(url_for("equipment_admin.item_detail", item_id=item.id))

    return render_template("admin/equipment/form.html", form=form, title="Modifier le matériel")


@equipment_admin_bp.get("/items/<int:item_id>")
@permission_required("equipment.view")
def item_detail(item_id):
    item = db.session.scalar(
        select(Equipment)
        .where(Equipment.id == item_id)
        .options(
            selectinload(Equipment.category),
            selectinload(Equipment.movements).selectinload(EquipmentMovement.equipment),
        )
    )
    if item is None:
        return ("", 404)
    balance = EquipmentService.balance(item)
    movements = list(reversed(item.movements))
    return render_template(
        "admin/equipment/detail.html",
        item=item,
        balance=balance,
        movements=movements,
    )


@equipment_admin_bp.route("/items/<int:item_id>/movement", methods=["GET", "POST"])
@permission_required("equipment.move")
def movement_create(item_id):
    item = db.session.scalar(
        select(Equipment)
        .where(Equipment.id == item_id)
        .options(selectinload(Equipment.movements))
    )
    if item is None:
        return ("", 404)

    form = EquipmentMovementForm()
    if form.validate_on_submit():
        try:
            movement = EquipmentService.add_movement(
                item,
                form.movement_type.data,
                form.quantity.data,
                form.note.data,
                current_user.id,
            )
            db.session.flush()
            AuditService.log(
                "equipment.movement",
                "Equipment",
                item.id,
                f"Mouvement {movement.movement_type} : {movement.quantity} {item.unit}",
                metadata={"movement_id": movement.id, "movement_type": movement.movement_type},
                user=current_user,
            )
            db.session.commit()
            flash("Mouvement enregistré.", "success")
            return redirect(url_for("equipment_admin.item_detail", item_id=item.id))
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc), "error")

    return render_template(
        "admin/equipment/movement_form.html",
        form=form,
        item=item,
        balance=EquipmentService.balance(item),
    )
