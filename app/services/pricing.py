from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Iterable

from sqlalchemy import select

from ..extensions import db
from ..models.catalog import Dish, Menu, Pack, PricingUnit, Service
from ..models.quote_request import QuoteRequestItemType


MAX_QUANTITY = Decimal("10000")


class PricingError(ValueError):
    pass


@dataclass(frozen=True)
class EstimatedItem:
    item_type: str
    item_id: int
    label: str
    quantity: Decimal
    pricing_unit: str
    unit_price: Decimal | None
    subtotal: Decimal | None


@dataclass(frozen=True)
class EstimateResult:
    items: list[EstimatedItem]
    known_total: Decimal
    has_on_request_items: bool
    currency: str
    warnings: list[str]


class PricingService:
    MODEL_MAP = {
        QuoteRequestItemType.SERVICE.value: (Service, "base_price"),
        QuoteRequestItemType.DISH.value: (Dish, "base_price"),
        QuoteRequestItemType.MENU.value: (Menu, "price"),
        QuoteRequestItemType.PACK.value: (Pack, "price"),
    }

    @staticmethod
    def _quantity(value) -> Decimal:
        try:
            quantity = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise PricingError("Quantité invalide.") from exc
        if quantity <= 0 or quantity > MAX_QUANTITY:
            raise PricingError("La quantité doit être comprise entre 0 et 10 000.")
        return quantity

    @classmethod
    def estimate_selection(
        cls,
        selections: Iterable[dict],
        *,
        guest_count: int,
        currency: str,
    ) -> EstimateResult:
        if guest_count <= 0 or guest_count > 100000:
            raise PricingError("Le nombre de personnes est invalide.")

        result_items: list[EstimatedItem] = []
        warnings: list[str] = []
        known_total = Decimal("0.00")
        has_on_request = False

        for raw in selections:
            item_type = str(raw.get("item_type", "")).upper()
            if item_type not in cls.MODEL_MAP:
                raise PricingError("Type d’élément catalogue invalide.")

            model, price_attribute = cls.MODEL_MAP[item_type]
            try:
                item_id = int(raw.get("item_id"))
            except (TypeError, ValueError) as exc:
                raise PricingError("Identifiant catalogue invalide.") from exc

            item = db.session.scalar(
                select(model).where(
                    model.id == item_id,
                    model.is_active.is_(True),
                    model.is_public.is_(True),
                )
            )
            if item is None:
                raise PricingError("Un élément sélectionné n’est plus disponible.")

            pricing_unit = item.pricing_unit
            requested_quantity = cls._quantity(raw.get("quantity", 1))
            minimum_people = getattr(item, "minimum_people", None)

            if minimum_people and guest_count < minimum_people:
                warnings.append(
                    f"{item.name} requiert au minimum {minimum_people} personnes. "
                    "La demande reste enregistrable mais le montant devra être confirmé."
                )

            if pricing_unit == PricingUnit.PER_PERSON.value:
                quantity = Decimal(guest_count)
            else:
                quantity = requested_quantity

            unit_price = getattr(item, price_attribute)
            subtotal: Decimal | None

            if pricing_unit == PricingUnit.ON_REQUEST.value or unit_price is None:
                unit_price = None
                subtotal = None
                has_on_request = True
            elif minimum_people and guest_count < minimum_people:
                subtotal = None
                has_on_request = True
            elif pricing_unit == PricingUnit.FIXED.value:
                quantity = Decimal("1")
                subtotal = Decimal(unit_price)
            elif pricing_unit in {
                PricingUnit.PER_PERSON.value,
                PricingUnit.PER_UNIT.value,
                PricingUnit.PER_HOUR.value,
            }:
                subtotal = Decimal(unit_price) * quantity
            else:
                raise PricingError("Unité de tarification non prise en charge.")

            if subtotal is not None:
                subtotal = subtotal.quantize(Decimal("0.01"))
                known_total += subtotal

            result_items.append(
                EstimatedItem(
                    item_type=item_type,
                    item_id=item.id,
                    label=item.name,
                    quantity=quantity,
                    pricing_unit=pricing_unit,
                    unit_price=Decimal(unit_price) if unit_price is not None else None,
                    subtotal=subtotal,
                )
            )

        return EstimateResult(
            items=result_items,
            known_total=known_total.quantize(Decimal("0.01")),
            has_on_request_items=has_on_request,
            currency=currency,
            warnings=warnings,
        )
