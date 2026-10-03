"""Create catalogue domain tables.

Revision ID: 20261003_01_catalog
Revises:
Create Date: 2026-10-03
"""

from alembic import op
import sqlalchemy as sa


revision = "20261003_01_catalog"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "catalog_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("slug", sa.String(length=140), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category_type", sa.String(length=20), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "category_type IN ('DISH', 'SERVICE', 'MENU', 'PACK')",
            name="ck_catalog_categories_category_type_valid",
        ),
        sa.CheckConstraint(
            "display_order >= 0",
            name="ck_catalog_categories_category_display_order_nonnegative",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_catalog_categories"),
        sa.UniqueConstraint("slug", name="uq_catalog_categories_slug"),
    )
    op.create_index(
        "ix_catalog_categories_type_active",
        "catalog_categories",
        ["category_type", "is_active"],
        unique=False,
    )

    op.create_table(
        "catalog_services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("short_description", sa.String(length=320), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_path", sa.String(length=300), nullable=True),
        sa.Column("base_price", sa.Numeric(14, 2), nullable=True),
        sa.Column("pricing_unit", sa.String(length=20), nullable=False),
        sa.Column("is_featured", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "pricing_unit IN ('FIXED', 'PER_PERSON', 'PER_UNIT', 'PER_HOUR', 'ON_REQUEST')",
            name="ck_catalog_services_service_pricing_unit_valid",
        ),
        sa.CheckConstraint(
            "display_order >= 0",
            name="ck_catalog_services_service_display_order_nonnegative",
        ),
        sa.CheckConstraint(
            "base_price IS NULL OR base_price >= 0",
            name="ck_catalog_services_service_price_nonnegative",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_catalog_services"),
        sa.UniqueConstraint("slug", name="uq_catalog_services_slug"),
    )
    op.create_index(
        "ix_catalog_services_public_order",
        "catalog_services",
        ["is_active", "is_public", "display_order"],
        unique=False,
    )

    op.create_table(
        "catalog_menus",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("short_description", sa.String(length=320), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_path", sa.String(length=300), nullable=True),
        sa.Column("price", sa.Numeric(14, 2), nullable=True),
        sa.Column("pricing_unit", sa.String(length=20), nullable=False),
        sa.Column("minimum_people", sa.Integer(), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "pricing_unit IN ('FIXED', 'PER_PERSON', 'PER_UNIT', 'PER_HOUR', 'ON_REQUEST')",
            name="ck_catalog_menus_menu_pricing_unit_valid",
        ),
        sa.CheckConstraint(
            "display_order >= 0",
            name="ck_catalog_menus_menu_display_order_nonnegative",
        ),
        sa.CheckConstraint(
            "price IS NULL OR price >= 0",
            name="ck_catalog_menus_menu_price_nonnegative",
        ),
        sa.CheckConstraint(
            "minimum_people IS NULL OR minimum_people > 0",
            name="ck_catalog_menus_menu_minimum_people_positive",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_catalog_menus"),
        sa.UniqueConstraint("slug", name="uq_catalog_menus_slug"),
    )
    op.create_index(
        "ix_catalog_menus_public_order",
        "catalog_menus",
        ["is_active", "is_public", "display_order"],
        unique=False,
    )

    op.create_table(
        "catalog_packs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("short_description", sa.String(length=320), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_path", sa.String(length=300), nullable=True),
        sa.Column("price", sa.Numeric(14, 2), nullable=True),
        sa.Column("pricing_unit", sa.String(length=20), nullable=False),
        sa.Column("minimum_people", sa.Integer(), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "pricing_unit IN ('FIXED', 'PER_PERSON', 'PER_UNIT', 'PER_HOUR', 'ON_REQUEST')",
            name="ck_catalog_packs_pack_pricing_unit_valid",
        ),
        sa.CheckConstraint(
            "display_order >= 0",
            name="ck_catalog_packs_pack_display_order_nonnegative",
        ),
        sa.CheckConstraint(
            "price IS NULL OR price >= 0",
            name="ck_catalog_packs_pack_price_nonnegative",
        ),
        sa.CheckConstraint(
            "minimum_people IS NULL OR minimum_people > 0",
            name="ck_catalog_packs_pack_minimum_people_positive",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_catalog_packs"),
        sa.UniqueConstraint("slug", name="uq_catalog_packs_slug"),
    )
    op.create_index(
        "ix_catalog_packs_public_order",
        "catalog_packs",
        ["is_active", "is_public", "display_order"],
        unique=False,
    )

    op.create_table(
        "catalog_dishes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("short_description", sa.String(length=320), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_path", sa.String(length=300), nullable=True),
        sa.Column("base_price", sa.Numeric(14, 2), nullable=True),
        sa.Column("pricing_unit", sa.String(length=20), nullable=False),
        sa.Column("is_featured", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "pricing_unit IN ('FIXED', 'PER_PERSON', 'PER_UNIT', 'PER_HOUR', 'ON_REQUEST')",
            name="ck_catalog_dishes_dish_pricing_unit_valid",
        ),
        sa.CheckConstraint(
            "display_order >= 0",
            name="ck_catalog_dishes_dish_display_order_nonnegative",
        ),
        sa.CheckConstraint(
            "base_price IS NULL OR base_price >= 0",
            name="ck_catalog_dishes_dish_price_nonnegative",
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["catalog_categories.id"],
            name="fk_catalog_dishes_category_id_catalog_categories",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_catalog_dishes"),
        sa.UniqueConstraint("slug", name="uq_catalog_dishes_slug"),
    )
    op.create_index(
        "ix_catalog_dishes_category_id",
        "catalog_dishes",
        ["category_id"],
        unique=False,
    )
    op.create_index(
        "ix_catalog_dishes_public_order",
        "catalog_dishes",
        ["is_active", "is_public", "display_order"],
        unique=False,
    )

    op.create_table(
        "catalog_menu_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("menu_id", sa.Integer(), nullable=False),
        sa.Column("dish_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(10, 2), nullable=False),
        sa.Column("section", sa.String(length=80), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_optional", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "quantity > 0",
            name="ck_catalog_menu_items_menu_item_quantity_positive",
        ),
        sa.CheckConstraint(
            "display_order >= 0",
            name="ck_catalog_menu_items_menu_item_display_order_nonnegative",
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["catalog_dishes.id"],
            name="fk_catalog_menu_items_dish_id_catalog_dishes",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["menu_id"],
            ["catalog_menus.id"],
            name="fk_catalog_menu_items_menu_id_catalog_menus",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_catalog_menu_items"),
        sa.UniqueConstraint(
            "menu_id",
            "dish_id",
            name="uq_catalog_menu_item_dish",
        ),
    )
    op.create_index(
        "ix_catalog_menu_items_dish_id",
        "catalog_menu_items",
        ["dish_id"],
        unique=False,
    )
    op.create_index(
        "ix_catalog_menu_items_menu_id",
        "catalog_menu_items",
        ["menu_id"],
        unique=False,
    )

    op.create_table(
        "catalog_pack_dishes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pack_id", sa.Integer(), nullable=False),
        sa.Column("dish_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(10, 2), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "quantity > 0",
            name="ck_catalog_pack_dishes_pack_dish_quantity_positive",
        ),
        sa.CheckConstraint(
            "display_order >= 0",
            name="ck_catalog_pack_dishes_pack_dish_display_order_nonnegative",
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["catalog_dishes.id"],
            name="fk_catalog_pack_dishes_dish_id_catalog_dishes",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["pack_id"],
            ["catalog_packs.id"],
            name="fk_catalog_pack_dishes_pack_id_catalog_packs",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_catalog_pack_dishes"),
        sa.UniqueConstraint("pack_id", "dish_id", name="uq_catalog_pack_dish"),
    )
    op.create_index("ix_catalog_pack_dishes_dish_id", "catalog_pack_dishes", ["dish_id"], unique=False)
    op.create_index("ix_catalog_pack_dishes_pack_id", "catalog_pack_dishes", ["pack_id"], unique=False)

    op.create_table(
        "catalog_pack_menus",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pack_id", sa.Integer(), nullable=False),
        sa.Column("menu_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(10, 2), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "quantity > 0",
            name="ck_catalog_pack_menus_pack_menu_quantity_positive",
        ),
        sa.CheckConstraint(
            "display_order >= 0",
            name="ck_catalog_pack_menus_pack_menu_display_order_nonnegative",
        ),
        sa.ForeignKeyConstraint(
            ["menu_id"],
            ["catalog_menus.id"],
            name="fk_catalog_pack_menus_menu_id_catalog_menus",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["pack_id"],
            ["catalog_packs.id"],
            name="fk_catalog_pack_menus_pack_id_catalog_packs",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_catalog_pack_menus"),
        sa.UniqueConstraint("pack_id", "menu_id", name="uq_catalog_pack_menu"),
    )
    op.create_index("ix_catalog_pack_menus_menu_id", "catalog_pack_menus", ["menu_id"], unique=False)
    op.create_index("ix_catalog_pack_menus_pack_id", "catalog_pack_menus", ["pack_id"], unique=False)

    op.create_table(
        "catalog_pack_services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pack_id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(10, 2), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "quantity > 0",
            name="ck_catalog_pack_services_pack_service_quantity_positive",
        ),
        sa.CheckConstraint(
            "display_order >= 0",
            name="ck_catalog_pack_services_pack_service_display_order_nonnegative",
        ),
        sa.ForeignKeyConstraint(
            ["pack_id"],
            ["catalog_packs.id"],
            name="fk_catalog_pack_services_pack_id_catalog_packs",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["catalog_services.id"],
            name="fk_catalog_pack_services_service_id_catalog_services",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_catalog_pack_services"),
        sa.UniqueConstraint(
            "pack_id",
            "service_id",
            name="uq_catalog_pack_service",
        ),
    )
    op.create_index("ix_catalog_pack_services_pack_id", "catalog_pack_services", ["pack_id"], unique=False)
    op.create_index("ix_catalog_pack_services_service_id", "catalog_pack_services", ["service_id"], unique=False)


def downgrade():
    op.drop_index("ix_catalog_pack_services_service_id", table_name="catalog_pack_services")
    op.drop_index("ix_catalog_pack_services_pack_id", table_name="catalog_pack_services")
    op.drop_table("catalog_pack_services")

    op.drop_index("ix_catalog_pack_menus_pack_id", table_name="catalog_pack_menus")
    op.drop_index("ix_catalog_pack_menus_menu_id", table_name="catalog_pack_menus")
    op.drop_table("catalog_pack_menus")

    op.drop_index("ix_catalog_pack_dishes_pack_id", table_name="catalog_pack_dishes")
    op.drop_index("ix_catalog_pack_dishes_dish_id", table_name="catalog_pack_dishes")
    op.drop_table("catalog_pack_dishes")

    op.drop_index("ix_catalog_menu_items_menu_id", table_name="catalog_menu_items")
    op.drop_index("ix_catalog_menu_items_dish_id", table_name="catalog_menu_items")
    op.drop_table("catalog_menu_items")

    op.drop_index("ix_catalog_dishes_public_order", table_name="catalog_dishes")
    op.drop_index("ix_catalog_dishes_category_id", table_name="catalog_dishes")
    op.drop_table("catalog_dishes")

    op.drop_index("ix_catalog_packs_public_order", table_name="catalog_packs")
    op.drop_table("catalog_packs")

    op.drop_index("ix_catalog_menus_public_order", table_name="catalog_menus")
    op.drop_table("catalog_menus")

    op.drop_index("ix_catalog_services_public_order", table_name="catalog_services")
    op.drop_table("catalog_services")

    op.drop_index("ix_catalog_categories_type_active", table_name="catalog_categories")
    op.drop_table("catalog_categories")
