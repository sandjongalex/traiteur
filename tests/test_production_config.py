import pytest

from app import create_app


def test_production_requires_secret_key(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv(
        "DATABASE_URL",
        "mysql+pymysql://user:password@localhost/wato_events",
    )
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app("production")


def test_production_requires_database_url(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "safe-test-value")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        create_app("production")
