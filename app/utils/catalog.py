import re
import unicodedata
from decimal import Decimal

from flask import current_app


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "item"


def unique_slug(model, value: str, current_id: int | None = None) -> str:
    base = slugify(value)
    candidate = base
    suffix = 2
    while True:
        query = model.query.filter_by(slug=candidate)
        if current_id is not None:
            query = query.filter(model.id != current_id)
        if query.first() is None:
            return candidate
        candidate = f"{base}-{suffix}"
        suffix += 1


def format_money(value: Decimal | None, pricing_unit: str | None = None) -> str:
    if pricing_unit == "ON_REQUEST" or value is None:
        return "Sur devis"

    amount = Decimal(value).quantize(Decimal("1"))
    formatted = f"{amount:,.0f}".replace(",", " ")
    currency = current_app.config.get("CURRENCY", "XAF")
    label = "FCFA" if currency == "XAF" else currency

    unit_suffix = {
        "PER_PERSON": " / personne",
        "PER_UNIT": " / unité",
        "PER_HOUR": " / heure",
    }.get(pricing_unit or "", "")

    return f"{formatted} {label}{unit_suffix}"
