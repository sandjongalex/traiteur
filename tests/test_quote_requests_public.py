from datetime import date, timedelta
from decimal import Decimal

from app.extensions import db
from app.models.catalog import Menu, PricingUnit, Service
from app.models.quote_request import QuoteRequest, QuoteRequestItem


def _base_payload(token="submission-test-1"):
    return {
        "event_type": "Mariage",
        "event_date": (date.today() + timedelta(days=30)).isoformat(),
        "event_time": "18:00",
        "location": "Yaoundé — Bastos",
        "guest_count": "100",
        "budget_min": "300000",
        "budget_max": "900000",
        "notes": "Réception familiale.",
        "customer_name": "Client Test",
        "phone": "+237 600 000 000",
        "whatsapp": "",
        "email": "",
        "submission_token": token,
        "website": "",
    }


def test_configurator_get(client):
    response = client.get("/demande-de-devis")
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "ESTIMATION INDICATIVE" in text
    assert "Récapitulatif" in text


def test_valid_submission_creates_request_and_snapshots(client, app):
    menu = Menu(
        name="Menu Snapshot",
        slug="menu-snapshot",
        price=Decimal("5000"),
        pricing_unit=PricingUnit.PER_PERSON.value,
        is_active=True,
        is_public=True,
    )
    db.session.add(menu)
    db.session.commit()

    payload = _base_payload()
    payload["menu_ids"] = str(menu.id)
    payload["price"] = "1"

    response = client.post("/demande-de-devis", data=payload, follow_redirects=False)
    assert response.status_code in {301, 302}
    assert "/demande-de-devis/confirmation/" in response.headers["Location"]

    saved = db.session.scalar(db.select(QuoteRequest))
    line = db.session.scalar(db.select(QuoteRequestItem))
    assert saved.reference.startswith("DEM-")
    assert saved.estimated_total == Decimal("500000.00")
    assert line.unit_price_snapshot == Decimal("5000.00")
    assert line.estimated_subtotal == Decimal("500000.00")

    menu.price = Decimal("7500")
    db.session.commit()
    db.session.refresh(line)
    assert line.unit_price_snapshot == Decimal("5000.00")


def test_browser_price_is_ignored(client, app):
    service = Service(
        name="Prix serveur",
        slug="prix-serveur",
        base_price=Decimal("25000"),
        pricing_unit=PricingUnit.FIXED.value,
        is_active=True,
        is_public=True,
    )
    db.session.add(service)
    db.session.commit()

    payload = _base_payload("submission-price-tamper")
    payload["service_ids"] = str(service.id)
    payload["price"] = "1"
    client.post("/demande-de-devis", data=payload)

    line = db.session.scalar(db.select(QuoteRequestItem))
    assert line.unit_price_snapshot == Decimal("25000.00")
    assert line.estimated_subtotal == Decimal("25000.00")


def test_missing_contact_is_rejected(client):
    payload = _base_payload("submission-no-contact")
    payload.update({"phone": "", "whatsapp": "", "email": ""})
    response = client.post("/demande-de-devis", data=payload)
    assert response.status_code == 200
    assert db.session.scalar(db.select(QuoteRequest)) is None


def test_past_date_is_rejected(client):
    payload = _base_payload("submission-past")
    payload["event_date"] = (date.today() - timedelta(days=1)).isoformat()
    response = client.post("/demande-de-devis", data=payload)
    assert response.status_code == 200
    assert db.session.scalar(db.select(QuoteRequest)) is None


def test_inactive_selection_is_rejected(client, app):
    service = Service(
        name="Inactif",
        slug="inactif-request",
        base_price=Decimal("1000"),
        pricing_unit=PricingUnit.FIXED.value,
        is_active=False,
        is_public=True,
    )
    db.session.add(service)
    db.session.commit()
    payload = _base_payload("submission-inactive")
    payload["service_ids"] = str(service.id)
    response = client.post("/demande-de-devis", data=payload)
    assert response.status_code == 200
    assert db.session.scalar(db.select(QuoteRequest)) is None


def test_duplicate_submission_token_creates_one_request(client, app):
    payload = _base_payload("same-submission-token")
    first = client.post("/demande-de-devis", data=payload, follow_redirects=False)
    second = client.post("/demande-de-devis", data=payload, follow_redirects=False)
    assert first.status_code in {301, 302}
    assert second.status_code in {301, 302}
    assert len(db.session.scalars(db.select(QuoteRequest)).all()) == 1


def test_confirmation_requires_random_public_token(client, app):
    payload = _base_payload("confirmation-token")
    client.post("/demande-de-devis", data=payload)
    saved = db.session.scalar(db.select(QuoteRequest))

    bad = client.get(f"/demande-de-devis/confirmation/{saved.reference}/wrong-token")
    assert bad.status_code == 404

    good = client.get(
        f"/demande-de-devis/confirmation/{saved.reference}/{saved.public_token}"
    )
    text = good.get_data(as_text=True)
    assert good.status_code == 200
    assert saved.reference in text
    assert saved.phone not in text
    assert saved.customer_name not in text
