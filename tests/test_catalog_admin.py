from decimal import Decimal
from io import BytesIO

from app.extensions import db
from app.models.catalog import PricingUnit, Service
from app.utils.files import save_catalog_image


def _login_catalog(client):
    return client.post(
        "/admin/catalogue/access",
        data={"access_key": "testing-catalog-key"},
        follow_redirects=False,
    )


def test_admin_catalog_requires_access(client):
    response = client.get("/admin/catalogue/", follow_redirects=False)
    assert response.status_code in {301, 302}
    assert "/admin/catalogue/access" in response.headers["Location"]


def test_admin_access_accepts_configured_key(client):
    response = _login_catalog(client)
    assert response.status_code in {301, 302}
    assert "/admin/catalogue/" in response.headers["Location"]


def test_admin_can_create_service(client, app):
    _login_catalog(client)

    response = client.post(
        "/admin/catalogue/services/new",
        data={
            "name": "Service test",
            "slug": "",
            "short_description": "Description",
            "description": "",
            "pricing_unit": PricingUnit.PER_PERSON.value,
            "base_price": "5000",
            "display_order": "1",
            "is_active": "y",
            "is_public": "y",
        },
        follow_redirects=False,
    )

    assert response.status_code in {301, 302}
    service = db.session.scalar(db.select(Service).where(Service.slug == "service-test"))
    assert service is not None
    assert service.base_price == Decimal("5000.00")
    assert service.is_public is True


def test_admin_can_toggle_publication(client, app):
    service = Service(name="Toggle", slug="toggle", is_public=False)
    db.session.add(service)
    db.session.commit()

    _login_catalog(client)
    response = client.post(
        f"/admin/catalogue/services/{service.id}/toggle/is_public",
        follow_redirects=False,
    )

    assert response.status_code in {301, 302}
    db.session.refresh(service)
    assert service.is_public is True


def test_catalog_upload_renames_allowed_file(app, tmp_path):
    app.config["UPLOAD_FOLDER"] = str(tmp_path)
    file = type("Upload", (), {})()

    from werkzeug.datastructures import FileStorage

    storage = FileStorage(
        stream=BytesIO(b"fake-image"),
        filename="../../dangerous name.jpg",
        content_type="image/jpeg",
    )
    saved = save_catalog_image(storage)

    assert saved.startswith("uploads/catalog/")
    assert saved.endswith(".jpg")
    assert ".." not in saved


def test_catalog_upload_rejects_forbidden_extension(app, tmp_path):
    app.config["UPLOAD_FOLDER"] = str(tmp_path)

    from werkzeug.datastructures import FileStorage

    storage = FileStorage(
        stream=BytesIO(b"bad"),
        filename="payload.exe",
        content_type="application/octet-stream",
    )

    try:
        save_catalog_image(storage)
        raised = False
    except ValueError:
        raised = True

    assert raised is True


def test_catalog_upload_rejects_mime_mismatch(app, tmp_path):
    app.config["UPLOAD_FOLDER"] = str(tmp_path)

    from werkzeug.datastructures import FileStorage

    storage = FileStorage(
        stream=BytesIO(b"not-really-a-jpeg"),
        filename="photo.jpg",
        content_type="application/octet-stream",
    )

    try:
        save_catalog_image(storage)
        raised = False
    except ValueError:
        raised = True

    assert raised is True
