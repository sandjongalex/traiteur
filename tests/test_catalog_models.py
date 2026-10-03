from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.catalog import (
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


def test_create_service_with_decimal_price(app):
    service = Service(
        name="Buffet entreprise",
        slug="buffet-entreprise",
        base_price=Decimal("5000.00"),
        pricing_unit=PricingUnit.PER_PERSON.value,
        is_active=True,
        is_public=True,
    )
    db.session.add(service)
    db.session.commit()

    saved = db.session.get(Service, service.id)
    assert saved.base_price == Decimal("5000.00")
    assert saved.is_public is True


def test_slug_is_unique(app):
    db.session.add(Service(name="Service A", slug="service-a"))
    db.session.commit()
    db.session.add(Service(name="Service B", slug="service-a"))

    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_menu_contains_dishes(app):
    dish = Dish(name="Plat test", slug="plat-test")
    menu = Menu(name="Menu test", slug="menu-test", pricing_unit=PricingUnit.ON_REQUEST.value)
    menu.items.append(MenuItem(dish=dish, quantity=Decimal("1.00"), display_order=0))
    db.session.add(menu)
    db.session.commit()

    saved = db.session.get(Menu, menu.id)
    assert len(saved.items) == 1
    assert saved.items[0].dish.name == "Plat test"


def test_pack_can_reference_dish_menu_and_service(app):
    dish = Dish(name="Plat", slug="plat")
    menu = Menu(name="Menu", slug="menu", pricing_unit=PricingUnit.ON_REQUEST.value)
    service = Service(name="Service", slug="service")
    pack = Pack(name="Pack", slug="pack", pricing_unit=PricingUnit.ON_REQUEST.value)
    pack.dish_items.append(PackDish(dish=dish))
    pack.menu_items.append(PackMenu(menu=menu))
    pack.service_items.append(PackService(service=service))
    db.session.add(pack)
    db.session.commit()

    saved = db.session.get(Pack, pack.id)
    assert saved.dish_items[0].dish.name == "Plat"
    assert saved.menu_items[0].menu.name == "Menu"
    assert saved.service_items[0].service.name == "Service"


def test_dish_category_relation(app):
    category = Category(
        name="Plats",
        slug="plats",
        category_type=CategoryType.DISH.value,
    )
    dish = Dish(name="Ndolè", slug="ndole", category=category)
    db.session.add(dish)
    db.session.commit()

    saved = db.session.get(Dish, dish.id)
    assert saved.category.name == "Plats"
