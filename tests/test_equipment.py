from decimal import Decimal

import pytest

from app.extensions import db
from app.models.equipment import Equipment, EquipmentCategory, EquipmentMovementType
from app.services.equipment import EquipmentService


@pytest.fixture
def equipment_item(app):
    with app.app_context():
        category = EquipmentCategory(name="Tentes", code="TENTES", is_active=True)
        item = Equipment(
            category=category,
            name="Tente 5 x 10 m",
            reference="TENTE-001",
            unit="pièce",
            initial_quantity=Decimal("4.00"),
            condition="GOOD",
            is_active=True,
        )
        db.session.add_all([category, item])
        db.session.commit()
        yield item.id


def test_equipment_ledger_balances(app, equipment_item):
    with app.app_context():
        item = db.session.get(Equipment, equipment_item)

        EquipmentService.add_movement(item, EquipmentMovementType.OUT.value, Decimal("2"), "Événement", None)
        db.session.flush()
        assert EquipmentService.balance(item).available == Decimal("2.00")
        assert EquipmentService.balance(item).out == Decimal("2.00")

        EquipmentService.add_movement(item, EquipmentMovementType.RETURN.value, Decimal("1"), "Retour", None)
        db.session.flush()
        balance = EquipmentService.balance(item)
        assert balance.available == Decimal("3.00")
        assert balance.out == Decimal("1.00")

        EquipmentService.add_movement(item, EquipmentMovementType.LOSS_EVENT.value, Decimal("1"), "Perdue", None)
        db.session.flush()
        balance = EquipmentService.balance(item)
        assert balance.total == Decimal("3.00")
        assert balance.available == Decimal("3.00")
        assert balance.out == Decimal("0.00")
        assert balance.lost == Decimal("1.00")


def test_equipment_prevents_negative_available(app, equipment_item):
    with app.app_context():
        item = db.session.get(Equipment, equipment_item)
        with pytest.raises(ValueError, match="Quantité indisponible"):
            EquipmentService.add_movement(
                item, EquipmentMovementType.OUT.value, Decimal("5"), None, None
            )
