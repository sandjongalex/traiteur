"""Create quote request domain.

Revision ID: 20261003_02_quote_requests
Revises: 20261003_01_catalog
Create Date: 2026-10-03
"""

from alembic import op
import sqlalchemy as sa


revision = "20261003_02_quote_requests"
down_revision = "20261003_01_catalog"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "quote_request_sequences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("last_value", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_quote_request_sequences"),
        sa.UniqueConstraint("year", name="uq_quote_request_sequences_year"),
    )

    op.create_table(
        "quote_requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("reference", sa.String(length=32), nullable=False),
        sa.Column("public_token", sa.String(length=64), nullable=False),
        sa.Column("submission_token", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("source", sa.String(length=20), nullable=False),
        sa.Column("customer_name", sa.String(length=160), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=True),
        sa.Column("whatsapp", sa.String(length=40), nullable=True),
        sa.Column("email", sa.String(length=254), nullable=True),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("event_date", sa.Date(), nullable=False),
        sa.Column("event_time", sa.Time(), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("guest_count", sa.Integer(), nullable=False),
        sa.Column("budget_min", sa.Numeric(14, 2), nullable=True),
        sa.Column("budget_max", sa.Numeric(14, 2), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("estimated_total", sa.Numeric(14, 2), nullable=True),
        sa.Column("has_on_request_items", sa.Boolean(), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "guest_count > 0",
            name="ck_quote_requests_quote_request_guest_count_positive",
        ),
        sa.CheckConstraint(
            "budget_min IS NULL OR budget_min >= 0",
            name="ck_quote_requests_quote_request_budget_min_nonnegative",
        ),
        sa.CheckConstraint(
            "budget_max IS NULL OR budget_max >= 0",
            name="ck_quote_requests_quote_request_budget_max_nonnegative",
        ),
        sa.CheckConstraint(
            "budget_min IS NULL OR budget_max IS NULL OR budget_max >= budget_min",
            name="ck_quote_requests_quote_request_budget_range_valid",
        ),
        sa.CheckConstraint(
            "estimated_total IS NULL OR estimated_total >= 0",
            name="ck_quote_requests_quote_request_estimated_total_nonnegative",
        ),
        sa.CheckConstraint(
            "status IN ('NEW','REVIEWING','CONTACTED','QUALIFIED','CONVERTED','REJECTED','ARCHIVED')",
            name="ck_quote_requests_quote_request_status_valid",
        ),
        sa.CheckConstraint(
            "source IN ('WEBSITE','WHATSAPP','PHONE','ADMIN','OTHER')",
            name="ck_quote_requests_quote_request_source_valid",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_quote_requests"),
        sa.UniqueConstraint("reference", name="uq_quote_requests_reference"),
        sa.UniqueConstraint("public_token", name="uq_quote_requests_public_token"),
        sa.UniqueConstraint("submission_token", name="uq_quote_requests_submission_token"),
    )
    op.create_index(
        "ix_quote_requests_status_created",
        "quote_requests",
        ["status", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_quote_requests_event_date", "quote_requests", ["event_date"], unique=False
    )
    op.create_index("ix_quote_requests_phone", "quote_requests", ["phone"], unique=False)
    op.create_index("ix_quote_requests_email", "quote_requests", ["email"], unique=False)

    op.create_table(
        "quote_request_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quote_request_id", sa.Integer(), nullable=False),
        sa.Column("item_type", sa.String(length=20), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("label_snapshot", sa.String(length=180), nullable=False),
        sa.Column("quantity", sa.Numeric(12, 2), nullable=False),
        sa.Column("unit_price_snapshot", sa.Numeric(14, 2), nullable=True),
        sa.Column("pricing_unit_snapshot", sa.String(length=20), nullable=False),
        sa.Column("estimated_subtotal", sa.Numeric(14, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "item_type IN ('SERVICE','DISH','MENU','PACK')",
            name="ck_quote_request_items_quote_request_item_type_valid",
        ),
        sa.CheckConstraint(
            "quantity > 0",
            name="ck_quote_request_items_quote_request_item_quantity_positive",
        ),
        sa.CheckConstraint(
            "unit_price_snapshot IS NULL OR unit_price_snapshot >= 0",
            name="ck_quote_request_items_quote_request_item_unit_price_nonnegative",
        ),
        sa.CheckConstraint(
            "estimated_subtotal IS NULL OR estimated_subtotal >= 0",
            name="ck_quote_request_items_quote_request_item_subtotal_nonnegative",
        ),
        sa.ForeignKeyConstraint(
            ["quote_request_id"],
            ["quote_requests.id"],
            name="fk_quote_request_items_quote_request_id_quote_requests",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_quote_request_items"),
    )
    op.create_index(
        "ix_quote_request_items_request",
        "quote_request_items",
        ["quote_request_id"],
        unique=False,
    )
    op.create_index(
        "ix_quote_request_items_catalog_ref",
        "quote_request_items",
        ["item_type", "item_id"],
        unique=False,
    )


def downgrade():
    op.drop_index("ix_quote_request_items_catalog_ref", table_name="quote_request_items")
    op.drop_index("ix_quote_request_items_request", table_name="quote_request_items")
    op.drop_table("quote_request_items")

    op.drop_index("ix_quote_requests_email", table_name="quote_requests")
    op.drop_index("ix_quote_requests_phone", table_name="quote_requests")
    op.drop_index("ix_quote_requests_event_date", table_name="quote_requests")
    op.drop_index("ix_quote_requests_status_created", table_name="quote_requests")
    op.drop_table("quote_requests")

    op.drop_table("quote_request_sequences")
