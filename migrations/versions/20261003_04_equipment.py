"""Create equipment management domain.

Revision ID: 20261003_04_equipment
Revises: 20261003_03_auth_rbac
Create Date: 2026-10-03
"""
from alembic import op
import sqlalchemy as sa

revision = "20261003_04_equipment"
down_revision = "20261003_03_auth_rbac"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "equipment_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_equipment_categories"),
        sa.UniqueConstraint("code", name="uq_equipment_categories_code"),
        sa.UniqueConstraint("name", name="uq_equipment_categories_name"),
    )
    op.create_index(
        "ix_equipment_categories_active",
        "equipment_categories",
        ["is_active"],
        unique=False,
    )

    op.create_table(
        "equipment_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("reference", sa.String(length=80), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("unit", sa.String(length=40), nullable=False),
        sa.Column("initial_quantity", sa.Numeric(12, 2), nullable=False),
        sa.Column("purchase_price", sa.Numeric(14, 2), nullable=True),
        sa.Column("replacement_value", sa.Numeric(14, 2), nullable=True),
        sa.Column("condition", sa.String(length=20), nullable=False),
        sa.Column("image_path", sa.String(length=300), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "initial_quantity >= 0",
            name="ck_equipment_items_equipment_initial_quantity_nonnegative",
        ),
        sa.CheckConstraint(
            "purchase_price IS NULL OR purchase_price >= 0",
            name="ck_equipment_items_equipment_purchase_price_nonnegative",
        ),
        sa.CheckConstraint(
            "replacement_value IS NULL OR replacement_value >= 0",
            name="ck_equipment_items_equipment_replacement_value_nonnegative",
        ),
        sa.CheckConstraint(
            "condition IN ('NEW','GOOD','FAIR','DAMAGED')",
            name="ck_equipment_items_equipment_condition_valid",
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["equipment_categories.id"],
            name="fk_equipment_items_category_id_equipment_categories",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_equipment_items"),
        sa.UniqueConstraint("reference", name="uq_equipment_items_reference"),
    )
    op.create_index(
        "ix_equipment_items_category_id",
        "equipment_items",
        ["category_id"],
        unique=False,
    )
    op.create_index(
        "ix_equipment_items_category_active",
        "equipment_items",
        ["category_id", "is_active"],
        unique=False,
    )

    op.create_table(
        "equipment_movements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("equipment_id", sa.Integer(), nullable=False),
        sa.Column("movement_type", sa.String(length=40), nullable=False),
        sa.Column("quantity", sa.Numeric(12, 2), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "quantity > 0",
            name="ck_equipment_movements_equipment_movement_quantity_positive",
        ),
        sa.CheckConstraint(
            "movement_type IN ("
            "'ENTRY','OUT','RETURN','MAINTENANCE_OUT','MAINTENANCE_RETURN',"
            "'LOSS_AVAILABLE','LOSS_EVENT','LOSS_MAINTENANCE',"
            "'BREAKAGE_AVAILABLE','BREAKAGE_EVENT','BREAKAGE_MAINTENANCE',"
            "'ADJUSTMENT_ADD','ADJUSTMENT_REMOVE'"
            ")",
            name="ck_equipment_movements_equipment_movement_type_valid",
        ),
        sa.ForeignKeyConstraint(
            ["equipment_id"],
            ["equipment_items.id"],
            name="fk_equipment_movements_equipment_id_equipment_items",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["users.id"],
            name="fk_equipment_movements_created_by_user_id_users",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_equipment_movements"),
    )
    op.create_index(
        "ix_equipment_movements_equipment_id",
        "equipment_movements",
        ["equipment_id"],
        unique=False,
    )
    op.create_index(
        "ix_equipment_movements_item_date",
        "equipment_movements",
        ["equipment_id", "occurred_at"],
        unique=False,
    )
    op.create_index(
        "ix_equipment_movements_type_date",
        "equipment_movements",
        ["movement_type", "occurred_at"],
        unique=False,
    )


def downgrade():
    op.drop_index("ix_equipment_movements_type_date", table_name="equipment_movements")
    op.drop_index("ix_equipment_movements_item_date", table_name="equipment_movements")
    op.drop_index("ix_equipment_movements_equipment_id", table_name="equipment_movements")
    op.drop_table("equipment_movements")

    op.drop_index("ix_equipment_items_category_active", table_name="equipment_items")
    op.drop_index("ix_equipment_items_category_id", table_name="equipment_items")
    op.drop_table("equipment_items")

    op.drop_index("ix_equipment_categories_active", table_name="equipment_categories")
    op.drop_table("equipment_categories")
