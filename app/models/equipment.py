from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlalchemy import CheckConstraint, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class EquipmentCondition(str, Enum):
    NEW = "NEW"
    GOOD = "GOOD"
    FAIR = "FAIR"
    DAMAGED = "DAMAGED"


class EquipmentMovementType(str, Enum):
    ENTRY = "ENTRY"
    OUT = "OUT"
    RETURN = "RETURN"
    MAINTENANCE_OUT = "MAINTENANCE_OUT"
    MAINTENANCE_RETURN = "MAINTENANCE_RETURN"
    LOSS_AVAILABLE = "LOSS_AVAILABLE"
    LOSS_EVENT = "LOSS_EVENT"
    LOSS_MAINTENANCE = "LOSS_MAINTENANCE"
    BREAKAGE_AVAILABLE = "BREAKAGE_AVAILABLE"
    BREAKAGE_EVENT = "BREAKAGE_EVENT"
    BREAKAGE_MAINTENANCE = "BREAKAGE_MAINTENANCE"
    ADJUSTMENT_ADD = "ADJUSTMENT_ADD"
    ADJUSTMENT_REMOVE = "ADJUSTMENT_REMOVE"


class EquipmentCategory(db.Model):
    __tablename__ = "equipment_categories"
    __table_args__ = (
        UniqueConstraint("code", name="uq_equipment_categories_code"),
        UniqueConstraint("name", name="uq_equipment_categories_name"),
        Index("ix_equipment_categories_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    code: Mapped[str] = mapped_column(db.String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(db.String(500))
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    equipment: Mapped[list["Equipment"]] = relationship(back_populates="category")


class Equipment(db.Model):
    __tablename__ = "equipment_items"
    __table_args__ = (
        UniqueConstraint("reference", name="uq_equipment_items_reference"),
        CheckConstraint("initial_quantity >= 0", name="equipment_initial_quantity_nonnegative"),
        CheckConstraint(
            "purchase_price IS NULL OR purchase_price >= 0",
            name="equipment_purchase_price_nonnegative",
        ),
        CheckConstraint(
            "replacement_value IS NULL OR replacement_value >= 0",
            name="equipment_replacement_value_nonnegative",
        ),
        CheckConstraint(
            "condition IN ('NEW','GOOD','FAIR','DAMAGED')",
            name="equipment_condition_valid",
        ),
        Index("ix_equipment_items_category_active", "category_id", "is_active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(
        db.ForeignKey("equipment_categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(db.String(160), nullable=False)
    reference: Mapped[str | None] = mapped_column(db.String(80))
    description: Mapped[str | None] = mapped_column(db.Text)
    unit: Mapped[str] = mapped_column(db.String(40), default="pièce", nullable=False)
    initial_quantity: Mapped[Decimal] = mapped_column(
        db.Numeric(12, 2), default=Decimal("0.00"), nullable=False
    )
    purchase_price: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    replacement_value: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    condition: Mapped[str] = mapped_column(
        db.String(20), default=EquipmentCondition.GOOD.value, nullable=False
    )
    image_path: Mapped[str | None] = mapped_column(db.String(300))
    notes: Mapped[str | None] = mapped_column(db.Text)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    category: Mapped[EquipmentCategory] = relationship(back_populates="equipment")
    movements: Mapped[list["EquipmentMovement"]] = relationship(
        back_populates="equipment", order_by="EquipmentMovement.occurred_at"
    )


class EquipmentMovement(db.Model):
    __tablename__ = "equipment_movements"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="equipment_movement_quantity_positive"),
        CheckConstraint(
            "movement_type IN ("
            "'ENTRY','OUT','RETURN','MAINTENANCE_OUT','MAINTENANCE_RETURN',"
            "'LOSS_AVAILABLE','LOSS_EVENT','LOSS_MAINTENANCE',"
            "'BREAKAGE_AVAILABLE','BREAKAGE_EVENT','BREAKAGE_MAINTENANCE',"
            "'ADJUSTMENT_ADD','ADJUSTMENT_REMOVE'"
            ")",
            name="equipment_movement_type_valid",
        ),
        Index("ix_equipment_movements_item_date", "equipment_id", "occurred_at"),
        Index("ix_equipment_movements_type_date", "movement_type", "occurred_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        db.ForeignKey("equipment_items.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    movement_type: Mapped[str] = mapped_column(db.String(40), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(db.Numeric(12, 2), nullable=False)
    note: Mapped[str | None] = mapped_column(db.String(500))
    created_by_user_id: Mapped[int | None] = mapped_column(
        db.ForeignKey("users.id", ondelete="SET NULL")
    )
    occurred_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )

    equipment: Mapped[Equipment] = relationship(back_populates="movements")
