from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..extensions import db
from ..models.equipment import Equipment, EquipmentMovement, EquipmentMovementType


ZERO = Decimal("0.00")


@dataclass(frozen=True)
class EquipmentBalance:
    total: Decimal
    available: Decimal
    out: Decimal
    maintenance: Decimal
    lost: Decimal
    broken: Decimal

    @property
    def unavailable(self) -> Decimal:
        return self.out + self.maintenance


class EquipmentService:
    @staticmethod
    def balance(item: Equipment) -> EquipmentBalance:
        total = Decimal(item.initial_quantity or ZERO)
        available = total
        out = ZERO
        maintenance = ZERO
        lost = ZERO
        broken = ZERO

        for movement in item.movements:
            q = Decimal(movement.quantity)
            kind = movement.movement_type

            if kind in {EquipmentMovementType.ENTRY.value, EquipmentMovementType.ADJUSTMENT_ADD.value}:
                total += q
                available += q
            elif kind == EquipmentMovementType.OUT.value:
                available -= q
                out += q
            elif kind == EquipmentMovementType.RETURN.value:
                out -= q
                available += q
            elif kind == EquipmentMovementType.MAINTENANCE_OUT.value:
                available -= q
                maintenance += q
            elif kind == EquipmentMovementType.MAINTENANCE_RETURN.value:
                maintenance -= q
                available += q
            elif kind in {
                EquipmentMovementType.LOSS_AVAILABLE.value,
                EquipmentMovementType.BREAKAGE_AVAILABLE.value,
                EquipmentMovementType.ADJUSTMENT_REMOVE.value,
            }:
                available -= q
                total -= q
                if kind == EquipmentMovementType.LOSS_AVAILABLE.value:
                    lost += q
                elif kind == EquipmentMovementType.BREAKAGE_AVAILABLE.value:
                    broken += q
            elif kind in {
                EquipmentMovementType.LOSS_EVENT.value,
                EquipmentMovementType.BREAKAGE_EVENT.value,
            }:
                out -= q
                total -= q
                if kind == EquipmentMovementType.LOSS_EVENT.value:
                    lost += q
                else:
                    broken += q
            elif kind in {
                EquipmentMovementType.LOSS_MAINTENANCE.value,
                EquipmentMovementType.BREAKAGE_MAINTENANCE.value,
            }:
                maintenance -= q
                total -= q
                if kind == EquipmentMovementType.LOSS_MAINTENANCE.value:
                    lost += q
                else:
                    broken += q

        return EquipmentBalance(
            total=total,
            available=available,
            out=out,
            maintenance=maintenance,
            lost=lost,
            broken=broken,
        )

    @classmethod
    def validate_movement(cls, item: Equipment, movement_type: str, quantity: Decimal) -> None:
        q = Decimal(quantity)
        if q <= 0:
            raise ValueError("La quantité doit être strictement positive.")

        b = cls.balance(item)

        needs_available = {
            EquipmentMovementType.OUT.value,
            EquipmentMovementType.MAINTENANCE_OUT.value,
            EquipmentMovementType.LOSS_AVAILABLE.value,
            EquipmentMovementType.BREAKAGE_AVAILABLE.value,
            EquipmentMovementType.ADJUSTMENT_REMOVE.value,
        }
        needs_out = {
            EquipmentMovementType.RETURN.value,
            EquipmentMovementType.LOSS_EVENT.value,
            EquipmentMovementType.BREAKAGE_EVENT.value,
        }
        needs_maintenance = {
            EquipmentMovementType.MAINTENANCE_RETURN.value,
            EquipmentMovementType.LOSS_MAINTENANCE.value,
            EquipmentMovementType.BREAKAGE_MAINTENANCE.value,
        }

        if movement_type in needs_available and q > b.available:
            raise ValueError(f"Quantité indisponible : {b.available} {item.unit} disponible(s).")
        if movement_type in needs_out and q > b.out:
            raise ValueError(f"Quantité invalide : {b.out} {item.unit} actuellement en sortie.")
        if movement_type in needs_maintenance and q > b.maintenance:
            raise ValueError(
                f"Quantité invalide : {b.maintenance} {item.unit} actuellement en maintenance."
            )

    @classmethod
    def add_movement(cls, item: Equipment, movement_type: str, quantity: Decimal, note: str | None, user_id: int | None):
        valid_types = {item.value for item in EquipmentMovementType}
        if movement_type not in valid_types:
            raise ValueError("Type de mouvement invalide.")
        cls.validate_movement(item, movement_type, quantity)
        movement = EquipmentMovement(
            equipment=item,
            movement_type=movement_type,
            quantity=Decimal(quantity),
            note=(note or "").strip() or None,
            created_by_user_id=user_id,
        )
        db.session.add(movement)
        return movement

    @staticmethod
    def list_items():
        return db.session.scalars(
            select(Equipment)
            .options(selectinload(Equipment.category), selectinload(Equipment.movements))
            .order_by(Equipment.name)
        ).all()
