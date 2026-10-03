import pytest

from app import create_app


def test_production_requires_secret_key(monkeypatch, tmp_path):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv(
        "DATABASE_URL",
        f"sqlite:///{(tmp_path / 'prod.db').as_posix()}",
    )
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app("production")


def test_production_requires_database_url(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "safe-test-value")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        create_app("production")


def test_production_accepts_sqlite_database_url(monkeypatch, tmp_path):
    db_path = tmp_path / "pythonanywhere.db"
    monkeypatch.setenv("SECRET_KEY", "safe-test-value")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path.as_posix()}")

    app = create_app("production")

    assert app.config["SQLALCHEMY_DATABASE_URI"] == f"sqlite:///{db_path.as_posix()}"
    assert app.config["SESSION_COOKIE_SECURE"] is True


def test_mysql_short_scheme_is_normalized(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "mysql://user:password@host/database")

    app = create_app("development")

    assert app.config["SQLALCHEMY_DATABASE_URI"].startswith("mysql+pymysql://")
