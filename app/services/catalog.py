from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..extensions import db
from ..models.catalog import (
    Dish,
    Menu,
    MenuItem,
    Pack,
    PackDish,
    PackMenu,
    PackService,
    Service,
)


class CatalogService:
    @staticmethod
    def public_services(*, featured: bool | None = None):
        stmt = select(Service).where(Service.is_active.is_(True), Service.is_public.is_(True))
        if featured is not None:
            stmt = stmt.where(Service.is_featured.is_(featured))
        stmt = stmt.order_by(Service.display_order, Service.name)
        return db.session.scalars(stmt).all()

    @staticmethod
    def public_dishes(*, featured: bool | None = None):
        stmt = select(Dish).where(Dish.is_active.is_(True), Dish.is_public.is_(True))
        if featured is not None:
            stmt = stmt.where(Dish.is_featured.is_(featured))
        stmt = stmt.order_by(Dish.display_order, Dish.name)
        return db.session.scalars(stmt).all()

    @staticmethod
    def public_menus(*, featured: bool | None = None):
        stmt = (
            select(Menu)
            .options(selectinload(Menu.items).selectinload(MenuItem.dish))
            .where(Menu.is_active.is_(True), Menu.is_public.is_(True))
        )
        if featured is not None:
            stmt = stmt.where(Menu.is_featured.is_(featured))
        stmt = stmt.order_by(Menu.display_order, Menu.name)
        return db.session.scalars(stmt).unique().all()

    @staticmethod
    def public_packs(*, featured: bool | None = None):
        stmt = (
            select(Pack)
            .options(
                selectinload(Pack.dish_items).selectinload(PackDish.dish),
                selectinload(Pack.menu_items).selectinload(PackMenu.menu),
                selectinload(Pack.service_items).selectinload(PackService.service),
            )
            .where(Pack.is_active.is_(True), Pack.is_public.is_(True))
        )
        if featured is not None:
            stmt = stmt.where(Pack.is_featured.is_(featured))
        stmt = stmt.order_by(Pack.display_order, Pack.name)
        return db.session.scalars(stmt).unique().all()
