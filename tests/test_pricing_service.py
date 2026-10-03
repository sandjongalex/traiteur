from decimal import Decimal

import pytest

from app.extensions import db
from app.models.catalog import Menu, Pack, PricingUnit, Service
from app.services.pricing import PricingError, PricingService


def _service(name, slug, unit, price=None):
    item = Service(
        name=name,
        slug=slug,
        pricing_unit=unit,
        base_price=price,
        is_active=True,
        is_public=True,
    )
    db.session.add(item)
    db.session.commit()
    return item


def test_pricing_fixed(app):
    item = _service("Fixe", "fixe", PricingUnit.FIXED.value, Decimal("10000"))
    result = PricingService.estimate_selection(
        [{"item_type": "SERVICE", "item_id": item.id, "quantity": 7}],
        guest_count=50,
        currency="XAF",
    )
    assert result.known_total == Decimal("10000.00")
    assert result.items[0].quantity == Decimal("1")


def test_pricing_per_person(app):
    item = _service("Par personne", "par-personne", PricingUnit.PER_PERSON.value, Decimal("5000"))
    result = PricingService.estimate_selection(
        [{"item_type": "SERVICE", "item_id": item.id, "quantity": 1}],
        guest_count=100,
        currency="XAF",
    )
    assert result.known_total == Decimal("500000.00")
    assert result.items[0].quantity == Decimal("100")


@pytest.mark.parametrize("unit", [PricingUnit.PER_UNIT.value, PricingUnit.PER_HOUR.value])
def test_pricing_quantity_units(app, unit):
    item = _service("Quantité", f"quantite-{unit.lower()}", unit, Decimal("2500"))
    result = PricingService.estimate_selection(
        [{"item_type": "SERVICE", "item_id": item.id, "quantity": 3}],
        guest_count=20,
        currency="XAF",
    )
    assert result.known_total == Decimal("7500.00")


def test_pricing_on_request_is_partial(app):
    item = _service("Sur devis", "sur-devis", PricingUnit.ON_REQUEST.value)
    result = PricingService.estimate_selection(
        [{"item_type": "SERVICE", "item_id": item.id, "quantity": 1}],
        guest_count=20,
        currency="XAF",
    )
    assert result.known_total == Decimal("0.00")
    assert result.has_on_request_items is True
    assert result.items[0].subtotal is None


def test_minimum_people_becomes_warning_not_fake_total(app):
    menu = Menu(
        name="Menu 50",
        slug="menu-50",
        price=Decimal("10000"),
        pricing_unit=PricingUnit.PER_PERSON.value,
        minimum_people=50,
        is_active=True,
        is_public=True,
    )
    db.session.add(menu)
    db.session.commit()

    result = PricingService.estimate_selection(
        [{"item_type": "MENU", "item_id": menu.id, "quantity": 1}],
        guest_count=30,
        currency="XAF",
    )
    assert result.known_total == Decimal("0.00")
    assert result.has_on_request_items is True
    assert result.items[0].subtotal is None
    assert result.warnings


def test_invalid_quantity_rejected(app):
    item = _service("Unité", "unite", PricingUnit.PER_UNIT.value, Decimal("1000"))
    with pytest.raises(PricingError):
        PricingService.estimate_selection(
            [{"item_type": "SERVICE", "item_id": item.id, "quantity": 0}],
            guest_count=10,
            currency="XAF",
        )


def test_private_item_rejected(app):
    item = Service(
        name="Privé",
        slug="prive-pricing",
        pricing_unit=PricingUnit.FIXED.value,
        base_price=Decimal("1000"),
        is_active=True,
        is_public=False,
    )
    db.session.add(item)
    db.session.commit()
    with pytest.raises(PricingError):
        PricingService.estimate_selection(
            [{"item_type": "SERVICE", "item_id": item.id, "quantity": 1}],
            guest_count=10,
            currency="XAF",
        )
