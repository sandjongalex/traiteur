from decimal import Decimal

from app.extensions import db
from app.models.catalog import Dish, Menu, MenuItem, Pack, PricingUnit, Service


def test_services_show_only_active_public_items(client, app):
    db.session.add_all(
        [
            Service(
                name="Visible",
                slug="visible",
                is_active=True,
                is_public=True,
                base_price=Decimal("1000"),
                pricing_unit=PricingUnit.FIXED.value,
            ),
            Service(name="Privé", slug="prive", is_active=True, is_public=False),
            Service(name="Inactif", slug="inactif", is_active=False, is_public=True),
        ]
    )
    db.session.commit()

    response = client.get("/services")
    text = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Visible" in text
    assert "Privé" not in text
    assert "Inactif" not in text


def test_published_menu_is_visible_with_composition(client, app):
    dish = Dish(name="Poulet DG", slug="poulet-dg", is_active=True, is_public=True)
    menu = Menu(
        name="Menu réception",
        slug="menu-reception",
        is_active=True,
        is_public=True,
        pricing_unit=PricingUnit.PER_PERSON.value,
        price=Decimal("7500"),
    )
    menu.items.append(MenuItem(dish=dish))
    db.session.add(menu)
    db.session.commit()

    response = client.get("/menus/menu-reception")
    text = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Menu réception" in text
    assert "Poulet DG" in text
    assert "7 500 FCFA" in text


def test_private_menu_detail_returns_404(client, app):
    menu = Menu(
        name="Menu privé",
        slug="menu-prive",
        is_active=True,
        is_public=False,
        pricing_unit=PricingUnit.ON_REQUEST.value,
    )
    db.session.add(menu)
    db.session.commit()

    response = client.get("/menus/menu-prive")
    assert response.status_code == 404


def test_featured_catalog_can_appear_on_home(client, app):
    service = Service(
        name="Service vedette",
        slug="service-vedette",
        is_active=True,
        is_public=True,
        is_featured=True,
    )
    db.session.add(service)
    db.session.commit()

    response = client.get("/")
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Service vedette" in text


def test_empty_catalog_does_not_break_public_pages(client):
    assert client.get("/services").status_code == 200
    assert client.get("/menus").status_code == 200
    assert client.get("/packs").status_code == 200
