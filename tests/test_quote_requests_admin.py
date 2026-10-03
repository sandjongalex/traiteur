from datetime import date, timedelta

from app.extensions import db
from tests.helpers import create_user, login
from app.models.quote_request import (
    QuoteRequest,
    QuoteRequestSource,
    QuoteRequestStatus,
)


def _request():
    item = QuoteRequest(
        reference="DEM-2099-000001",
        public_token="public-token-admin",
        submission_token="submission-token-admin",
        status=QuoteRequestStatus.NEW.value,
        source=QuoteRequestSource.WEBSITE.value,
        customer_name="Admin Test",
        phone="+237600000000",
        event_type="Mariage",
        event_date=date.today() + timedelta(days=20),
        location="Yaoundé",
        guest_count=50,
        estimated_total=0,
        has_on_request_items=False,
        currency="XAF",
    )
    db.session.add(item)
    db.session.commit()
    return item


def test_quote_request_admin_requires_login(client):
    response = client.get("/admin/demandes-de-devis/", follow_redirects=False)
    assert response.status_code in {301, 302}
    assert "/admin/login" in response.headers["Location"]


def test_admin_can_list_and_view_requests(client, app):
    item = _request()
    create_user(); login(client)
    listing = client.get("/admin/demandes-de-devis/")
    detail = client.get(f"/admin/demandes-de-devis/{item.id}")
    assert listing.status_code == 200
    assert item.reference in listing.get_data(as_text=True)
    assert detail.status_code == 200
    assert "Admin Test" in detail.get_data(as_text=True)


def test_admin_can_update_valid_status(client, app):
    item = _request()
    create_user(); login(client)
    response = client.post(
        f"/admin/demandes-de-devis/{item.id}/status",
        data={"status": "REVIEWING"},
        follow_redirects=False,
    )
    assert response.status_code in {301, 302}
    db.session.refresh(item)
    assert item.status == "REVIEWING"


def test_admin_rejects_invalid_status(client, app):
    item = _request()
    create_user(); login(client)
    response = client.post(
        f"/admin/demandes-de-devis/{item.id}/status",
        data={"status": "WHATEVER"},
    )
    assert response.status_code == 400


def test_no_standard_hard_delete_route(client, app):
    item = _request()
    create_user(); login(client)
    response = client.post(f"/admin/demandes-de-devis/{item.id}/delete")
    assert response.status_code in {404, 405}
