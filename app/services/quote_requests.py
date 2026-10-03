from __future__ import annotations

from datetime import datetime
from secrets import token_urlsafe

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models.quote_request import (
    QuoteRequest,
    QuoteRequestItem,
    QuoteRequestSequence,
    QuoteRequestSource,
    QuoteRequestStatus,
)
from .pricing import EstimateResult


class DuplicateSubmissionError(ValueError):
    pass


class QuoteRequestService:
    @staticmethod
    def next_reference() -> str:
        year = datetime.now().year
        sequence = db.session.scalar(
            select(QuoteRequestSequence)
            .where(QuoteRequestSequence.year == year)
            .with_for_update()
        )
        if sequence is None:
            sequence = QuoteRequestSequence(year=year, last_value=0)
            db.session.add(sequence)
            db.session.flush()
        sequence.last_value += 1
        return f"DEM-{year}-{sequence.last_value:06d}"

    @classmethod
    def create_from_public(
        cls,
        *,
        form,
        estimate: EstimateResult,
        submission_token: str,
    ) -> QuoteRequest:
        if db.session.scalar(
            select(QuoteRequest.id).where(
                QuoteRequest.submission_token == submission_token
            )
        ):
            raise DuplicateSubmissionError("Cette demande a déjà été envoyée.")

        request_record = QuoteRequest(
            reference=cls.next_reference(),
            public_token=token_urlsafe(24),
            submission_token=submission_token,
            status=QuoteRequestStatus.NEW.value,
            source=QuoteRequestSource.WEBSITE.value,
            customer_name=form.customer_name.data.strip(),
            phone=form.normalized_phone(),
            whatsapp=form.normalized_whatsapp(),
            email=form.normalized_email(),
            event_type=form.event_type.data,
            event_date=form.event_date.data,
            event_time=form.event_time.data,
            location=form.location.data.strip(),
            guest_count=form.guest_count.data,
            budget_min=form.budget_min.data,
            budget_max=form.budget_max.data,
            notes=(form.notes.data or "").strip() or None,
            estimated_total=estimate.known_total,
            has_on_request_items=estimate.has_on_request_items,
            currency=estimate.currency,
        )
        db.session.add(request_record)

        for item in estimate.items:
            request_record.items.append(
                QuoteRequestItem(
                    item_type=item.item_type,
                    item_id=item.item_id,
                    label_snapshot=item.label,
                    quantity=item.quantity,
                    unit_price_snapshot=item.unit_price,
                    pricing_unit_snapshot=item.pricing_unit,
                    estimated_subtotal=item.subtotal,
                )
            )

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            existing = db.session.scalar(
                select(QuoteRequest).where(
                    QuoteRequest.submission_token == submission_token
                )
            )
            if existing is not None:
                raise DuplicateSubmissionError("Cette demande a déjà été envoyée.")
            raise

        return request_record
