from __future__ import annotations

from datetime import date, datetime, time, timezone
from decimal import Decimal
from enum import Enum
from secrets import token_urlsafe

from sqlalchemy import CheckConstraint, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class QuoteRequestStatus(str, Enum):
    NEW = "NEW"
    REVIEWING = "REVIEWING"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    CONVERTED = "CONVERTED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"


class QuoteRequestSource(str, Enum):
    WEBSITE = "WEBSITE"
    WHATSAPP = "WHATSAPP"
    PHONE = "PHONE"
    ADMIN = "ADMIN"
    OTHER = "OTHER"


class QuoteRequestItemType(str, Enum):
    SERVICE = "SERVICE"
    DISH = "DISH"
    MENU = "MENU"
    PACK = "PACK"


class EventType(str, Enum):
    WEDDING = "Mariage"
    BIRTHDAY = "Anniversaire"
    BAPTISM = "Baptême"
    PRIVATE_RECEPTION = "Réception privée"
    SEMINAR = "Séminaire"
    CONFERENCE = "Conférence"
    COCKTAIL = "Cocktail"
    BUFFET = "Buffet"
    CORPORATE = "Événement d’entreprise"
    FAMILY_CEREMONY = "Cérémonie familiale"
    OTHER = "Autre"


class QuoteRequestSequence(db.Model):
    __tablename__ = "quote_request_sequences"
    __table_args__ = (UniqueConstraint("year", name="uq_quote_request_sequences_year"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(nullable=False)
    last_value: Mapped[int] = mapped_column(default=0, nullable=False)


class QuoteRequest(db.Model):
    __tablename__ = "quote_requests"
    __table_args__ = (
        UniqueConstraint("reference", name="uq_quote_requests_reference"),
        UniqueConstraint("public_token", name="uq_quote_requests_public_token"),
        UniqueConstraint("submission_token", name="uq_quote_requests_submission_token"),
        CheckConstraint("guest_count > 0", name="quote_request_guest_count_positive"),
        CheckConstraint("budget_min IS NULL OR budget_min >= 0", name="quote_request_budget_min_nonnegative"),
        CheckConstraint("budget_max IS NULL OR budget_max >= 0", name="quote_request_budget_max_nonnegative"),
        CheckConstraint(
            "budget_min IS NULL OR budget_max IS NULL OR budget_max >= budget_min",
            name="quote_request_budget_range_valid",
        ),
        CheckConstraint(
            "estimated_total IS NULL OR estimated_total >= 0",
            name="quote_request_estimated_total_nonnegative",
        ),
        CheckConstraint(
            "status IN ('NEW','REVIEWING','CONTACTED','QUALIFIED','CONVERTED','REJECTED','ARCHIVED')",
            name="quote_request_status_valid",
        ),
        CheckConstraint(
            "source IN ('WEBSITE','WHATSAPP','PHONE','ADMIN','OTHER')",
            name="quote_request_source_valid",
        ),
        Index("ix_quote_requests_status_created", "status", "created_at"),
        Index("ix_quote_requests_event_date", "event_date"),
        Index("ix_quote_requests_phone", "phone"),
        Index("ix_quote_requests_email", "email"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(db.String(32), nullable=False)
    public_token: Mapped[str] = mapped_column(
        db.String(64), default=lambda: token_urlsafe(24), nullable=False
    )
    submission_token: Mapped[str] = mapped_column(db.String(64), nullable=False)
    status: Mapped[str] = mapped_column(
        db.String(20), default=QuoteRequestStatus.NEW.value, nullable=False
    )
    source: Mapped[str] = mapped_column(
        db.String(20), default=QuoteRequestSource.WEBSITE.value, nullable=False
    )

    customer_name: Mapped[str] = mapped_column(db.String(160), nullable=False)
    phone: Mapped[str | None] = mapped_column(db.String(40))
    whatsapp: Mapped[str | None] = mapped_column(db.String(40))
    email: Mapped[str | None] = mapped_column(db.String(254))

    event_type: Mapped[str] = mapped_column(db.String(80), nullable=False)
    event_date: Mapped[date] = mapped_column(nullable=False)
    event_time: Mapped[time | None] = mapped_column()
    location: Mapped[str] = mapped_column(db.String(255), nullable=False)
    guest_count: Mapped[int] = mapped_column(nullable=False)

    budget_min: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    budget_max: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    notes: Mapped[str | None] = mapped_column(db.Text)

    estimated_total: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    has_on_request_items: Mapped[bool] = mapped_column(default=False, nullable=False)
    currency: Mapped[str] = mapped_column(db.String(8), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    items: Mapped[list["QuoteRequestItem"]] = relationship(
        back_populates="quote_request",
        cascade="all, delete-orphan",
        order_by="QuoteRequestItem.id",
    )


class QuoteRequestItem(db.Model):
    __tablename__ = "quote_request_items"
    __table_args__ = (
        CheckConstraint(
            "item_type IN ('SERVICE','DISH','MENU','PACK')",
            name="quote_request_item_type_valid",
        ),
        CheckConstraint("quantity > 0", name="quote_request_item_quantity_positive"),
        CheckConstraint(
            "unit_price_snapshot IS NULL OR unit_price_snapshot >= 0",
            name="quote_request_item_unit_price_nonnegative",
        ),
        CheckConstraint(
            "estimated_subtotal IS NULL OR estimated_subtotal >= 0",
            name="quote_request_item_subtotal_nonnegative",
        ),
        Index("ix_quote_request_items_request", "quote_request_id"),
        Index("ix_quote_request_items_catalog_ref", "item_type", "item_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    quote_request_id: Mapped[int] = mapped_column(
        db.ForeignKey("quote_requests.id", ondelete="CASCADE"), nullable=False
    )
    item_type: Mapped[str] = mapped_column(db.String(20), nullable=False)
    item_id: Mapped[int] = mapped_column(nullable=False)
    label_snapshot: Mapped[str] = mapped_column(db.String(180), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(db.Numeric(12, 2), nullable=False)
    unit_price_snapshot: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    pricing_unit_snapshot: Mapped[str] = mapped_column(db.String(20), nullable=False)
    estimated_subtotal: Mapped[Decimal | None] = mapped_column(db.Numeric(14, 2))
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )

    quote_request: Mapped[QuoteRequest] = relationship(back_populates="items")
