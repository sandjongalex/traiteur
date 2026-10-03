from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlalchemy import CheckConstraint, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class PricingUnit(str, Enum):
    FIXED = "FIXED"
    PER_PERSON = "PER_PERSON"
    PER_UNIT = "PER_UNIT"
    PER_HOUR = "PER_HOUR"
    ON_REQUEST = "ON_REQUEST"


class CategoryType(str, Enum):
    DISH = "DISH"
    SERVICE = "SERVICE"
    MENU = "MENU"
    PACK = "PACK"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class Category(TimestampMixin, db.Model):
    __tablename__ = "catalog_categories"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_catalog_categories_slug"),
        CheckConstraint("category_type IN ('DISH', 'SERVICE', 'MENU', 'PACK')", name="category_type_valid"),
        CheckConstraint("display_order >= 0", name="category_display_order_nonnegative"),
        Index("ix_catalog_categories_type_active", "category_type", "is_active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    slug: Mapped[str] = mapped_column(db.String(140), nullable=False)
    description: Mapped[str | None] = mapped_column(db.Text)
    category_type: Mapped[str] = mapped_column(db.String(20), nullable=False)
    display_order: Mapped[int] = mapped_column(default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    dishes: Mapped[list["Dish"]] = relationship(back_populates="category")


class Service(TimestampMixin, db.Model):
    __tablename__ = "catalog_services"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_catalog_services_slug"),
        CheckConstraint("pricing_unit IN ('FIXED', 'PER_PERSON', 'PER_UNIT', 'PER_HOUR', 'ON_REQUEST')", name="service_pricing_unit_valid"),
        CheckConstraint("display_order >= 0", name="service_display_order_nonnegative"),
        CheckConstraint("base_price IS NULL OR base_price >= 0", name="service_price_nonnegative"),
        Index("ix_catalog_services_public_order", "is_active", "is_public", "display_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(160), nullable=False)
    slug: Mapped[str] = mapped_column(db.String(180), nullable=False)
    short_description: Mapped[str | None] = mapped_column(db.String(320))
    description: Mapped[str | None] = mapped_column(db.Text)
    image_path: Mapped[str | None] = mapped_column(db.String(300))
    base_price: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    pricing_unit: Mapped[str] = mapped_column(
        db.String(20), default=PricingUnit.ON_REQUEST.value, nullable=False
    )
    is_featured: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(default=0, nullable=False)

    pack_links: Mapped[list["PackService"]] = relationship(back_populates="service")


class Dish(TimestampMixin, db.Model):
    __tablename__ = "catalog_dishes"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_catalog_dishes_slug"),
        CheckConstraint("pricing_unit IN ('FIXED', 'PER_PERSON', 'PER_UNIT', 'PER_HOUR', 'ON_REQUEST')", name="dish_pricing_unit_valid"),
        CheckConstraint("display_order >= 0", name="dish_display_order_nonnegative"),
        CheckConstraint("base_price IS NULL OR base_price >= 0", name="dish_price_nonnegative"),
        Index("ix_catalog_dishes_public_order", "is_active", "is_public", "display_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int | None] = mapped_column(
        db.ForeignKey("catalog_categories.id", ondelete="RESTRICT"), index=True
    )
    name: Mapped[str] = mapped_column(db.String(160), nullable=False)
    slug: Mapped[str] = mapped_column(db.String(180), nullable=False)
    short_description: Mapped[str | None] = mapped_column(db.String(320))
    description: Mapped[str | None] = mapped_column(db.Text)
    image_path: Mapped[str | None] = mapped_column(db.String(300))
    base_price: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    pricing_unit: Mapped[str] = mapped_column(
        db.String(20), default=PricingUnit.ON_REQUEST.value, nullable=False
    )
    is_featured: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(default=0, nullable=False)

    category: Mapped[Category | None] = relationship(back_populates="dishes")
    menu_links: Mapped[list["MenuItem"]] = relationship(back_populates="dish")
    pack_links: Mapped[list["PackDish"]] = relationship(back_populates="dish")


class Menu(TimestampMixin, db.Model):
    __tablename__ = "catalog_menus"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_catalog_menus_slug"),
        CheckConstraint("pricing_unit IN ('FIXED', 'PER_PERSON', 'PER_UNIT', 'PER_HOUR', 'ON_REQUEST')", name="menu_pricing_unit_valid"),
        CheckConstraint("display_order >= 0", name="menu_display_order_nonnegative"),
        CheckConstraint("price IS NULL OR price >= 0", name="menu_price_nonnegative"),
        CheckConstraint("minimum_people IS NULL OR minimum_people > 0", name="menu_minimum_people_positive"),
        Index("ix_catalog_menus_public_order", "is_active", "is_public", "display_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(160), nullable=False)
    slug: Mapped[str] = mapped_column(db.String(180), nullable=False)
    short_description: Mapped[str | None] = mapped_column(db.String(320))
    description: Mapped[str | None] = mapped_column(db.Text)
    image_path: Mapped[str | None] = mapped_column(db.String(300))
    price: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    pricing_unit: Mapped[str] = mapped_column(
        db.String(20), default=PricingUnit.PER_PERSON.value, nullable=False
    )
    minimum_people: Mapped[int | None] = mapped_column()
    is_featured: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(default=0, nullable=False)

    items: Mapped[list["MenuItem"]] = relationship(
        back_populates="menu",
        cascade="all, delete-orphan",
        order_by="MenuItem.display_order",
    )
    pack_links: Mapped[list["PackMenu"]] = relationship(back_populates="menu")


class MenuItem(TimestampMixin, db.Model):
    __tablename__ = "catalog_menu_items"
    __table_args__ = (
        UniqueConstraint("menu_id", "dish_id", name="uq_catalog_menu_item_dish"),
        CheckConstraint("quantity > 0", name="menu_item_quantity_positive"),
        CheckConstraint("display_order >= 0", name="menu_item_display_order_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    menu_id: Mapped[int] = mapped_column(
        db.ForeignKey("catalog_menus.id", ondelete="CASCADE"), nullable=False, index=True
    )
    dish_id: Mapped[int] = mapped_column(
        db.ForeignKey("catalog_dishes.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    quantity: Mapped[Decimal] = mapped_column(
        db.Numeric(10, 2), default=Decimal("1.00"), nullable=False
    )
    section: Mapped[str | None] = mapped_column(db.String(80))
    display_order: Mapped[int] = mapped_column(default=0, nullable=False)
    is_optional: Mapped[bool] = mapped_column(default=False, nullable=False)

    menu: Mapped[Menu] = relationship(back_populates="items")
    dish: Mapped[Dish] = relationship(back_populates="menu_links")


class Pack(TimestampMixin, db.Model):
    __tablename__ = "catalog_packs"
    __table_args__ = (
        UniqueConstraint("slug", name="uq_catalog_packs_slug"),
        CheckConstraint("pricing_unit IN ('FIXED', 'PER_PERSON', 'PER_UNIT', 'PER_HOUR', 'ON_REQUEST')", name="pack_pricing_unit_valid"),
        CheckConstraint("display_order >= 0", name="pack_display_order_nonnegative"),
        CheckConstraint("price IS NULL OR price >= 0", name="pack_price_nonnegative"),
        CheckConstraint("minimum_people IS NULL OR minimum_people > 0", name="pack_minimum_people_positive"),
        Index("ix_catalog_packs_public_order", "is_active", "is_public", "display_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(160), nullable=False)
    slug: Mapped[str] = mapped_column(db.String(180), nullable=False)
    short_description: Mapped[str | None] = mapped_column(db.String(320))
    description: Mapped[str | None] = mapped_column(db.Text)
    image_path: Mapped[str | None] = mapped_column(db.String(300))
    price: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    pricing_unit: Mapped[str] = mapped_column(
        db.String(20), default=PricingUnit.ON_REQUEST.value, nullable=False
    )
    minimum_people: Mapped[int | None] = mapped_column()
    is_featured: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(default=0, nullable=False)

    dish_items: Mapped[list["PackDish"]] = relationship(
        back_populates="pack", cascade="all, delete-orphan"
    )
    menu_items: Mapped[list["PackMenu"]] = relationship(
        back_populates="pack", cascade="all, delete-orphan"
    )
    service_items: Mapped[list["PackService"]] = relationship(
        back_populates="pack", cascade="all, delete-orphan"
    )


class PackDish(TimestampMixin, db.Model):
    __tablename__ = "catalog_pack_dishes"
    __table_args__ = (
        UniqueConstraint("pack_id", "dish_id", name="uq_catalog_pack_dish"),
        CheckConstraint("quantity > 0", name="pack_dish_quantity_positive"),
        CheckConstraint("display_order >= 0", name="pack_dish_display_order_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    pack_id: Mapped[int] = mapped_column(
        db.ForeignKey("catalog_packs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    dish_id: Mapped[int] = mapped_column(
        db.ForeignKey("catalog_dishes.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    quantity: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), default=Decimal("1.00"), nullable=False)
    display_order: Mapped[int] = mapped_column(default=0, nullable=False)

    pack: Mapped[Pack] = relationship(back_populates="dish_items")
    dish: Mapped[Dish] = relationship(back_populates="pack_links")


class PackMenu(TimestampMixin, db.Model):
    __tablename__ = "catalog_pack_menus"
    __table_args__ = (
        UniqueConstraint("pack_id", "menu_id", name="uq_catalog_pack_menu"),
        CheckConstraint("quantity > 0", name="pack_menu_quantity_positive"),
        CheckConstraint("display_order >= 0", name="pack_menu_display_order_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    pack_id: Mapped[int] = mapped_column(
        db.ForeignKey("catalog_packs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    menu_id: Mapped[int] = mapped_column(
        db.ForeignKey("catalog_menus.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    quantity: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), default=Decimal("1.00"), nullable=False)
    display_order: Mapped[int] = mapped_column(default=0, nullable=False)

    pack: Mapped[Pack] = relationship(back_populates="menu_items")
    menu: Mapped[Menu] = relationship(back_populates="pack_links")


class PackService(TimestampMixin, db.Model):
    __tablename__ = "catalog_pack_services"
    __table_args__ = (
        UniqueConstraint("pack_id", "service_id", name="uq_catalog_pack_service"),
        CheckConstraint("quantity > 0", name="pack_service_quantity_positive"),
        CheckConstraint("display_order >= 0", name="pack_service_display_order_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    pack_id: Mapped[int] = mapped_column(
        db.ForeignKey("catalog_packs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    service_id: Mapped[int] = mapped_column(
        db.ForeignKey("catalog_services.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    quantity: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), default=Decimal("1.00"), nullable=False)
    display_order: Mapped[int] = mapped_column(default=0, nullable=False)

    pack: Mapped[Pack] = relationship(back_populates="service_items")
    service: Mapped[Service] = relationship(back_populates="pack_links")
