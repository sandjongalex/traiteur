import pytest

from app import create_app


def test_create_app_uses_testing_config():
    app = create_app("testing")
    assert app.testing is True
    assert app.config["APP_NAME"] == "WATO EVENTS"
    assert app.config["CURRENCY"] == "XAF"


def test_unknown_environment_is_rejected():
    with pytest.raises(RuntimeError, match="Unknown APP_ENV"):
        create_app("does-not-exist")


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "application": "WATO EVENTS",
    }


def test_root_is_only_a_foundation_placeholder(client):
    response = client.get("/")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["project"] == "WATO EVENTS"
    assert payload["status"] == "foundation-ready"
