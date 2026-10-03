from decimal import Decimal

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.extensions import db
from app.models.catalog import PricingUnit, Service
from app.models.auth import Role, User


EXPECTED_TABLES = {
    "alembic_version",
    "catalog_categories",
    "catalog_services",
    "catalog_dishes",
    "catalog_menus",
    "catalog_menu_items",
    "catalog_packs",
    "catalog_pack_dishes",
    "catalog_pack_menus",
    "catalog_pack_services",
    "quote_request_sequences",
    "quote_requests",
    "quote_request_items",
    "users",
    "roles",
    "permissions",
    "user_roles",
    "role_permissions",
    "audit_logs",
}


def _file_app(monkeypatch, tmp_path, name="wato-test.db"):
    db_path = tmp_path / name
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path.as_posix()}")
    monkeypatch.setenv("SQLITE_BUSY_TIMEOUT_MS", "5000")
    monkeypatch.setenv("SQLITE_WAL_ENABLED", "1")
    return create_app("development"), db_path


def test_sqlite_pragmas_are_enabled(monkeypatch, tmp_path):
    app, _ = _file_app(monkeypatch, tmp_path)

    with app.app_context():
        connection = db.session.connection()
        assert connection.execute(text("PRAGMA foreign_keys")).scalar_one() == 1
        assert connection.execute(text("PRAGMA busy_timeout")).scalar_one() >= 5000
        assert connection.execute(text("PRAGMA journal_mode")).scalar_one().lower() == "wal"


def test_empty_sqlite_database_migrates_to_single_head(monkeypatch, tmp_path):
    app, db_path = _file_app(monkeypatch, tmp_path, "fresh.db")
    assert not db_path.exists()

    runner = app.test_cli_runner()
    upgrade = runner.invoke(args=["db", "upgrade"])
    assert upgrade.exit_code == 0, upgrade.output
    assert db_path.exists()

    with app.app_context():
        tables = set(inspect(db.engine).get_table_names())
        assert EXPECTED_TABLES <= tables
        revision = db.session.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one()
        assert revision == "20261003_03_auth_rbac"


def test_sqlite_seed_rbac_is_idempotent_after_migration(monkeypatch, tmp_path):
    app, _ = _file_app(monkeypatch, tmp_path, "seed.db")
    runner = app.test_cli_runner()

    assert runner.invoke(args=["db", "upgrade"]).exit_code == 0
    first = runner.invoke(args=["seed-rbac"])
    second = runner.invoke(args=["seed-rbac"])

    assert first.exit_code == 0, first.output
    assert second.exit_code == 0, second.output

    with app.app_context():
        role_count = db.session.query(Role).count()
        assert role_count == 7


def test_create_superadmin_cli_works_on_sqlite(monkeypatch, tmp_path):
    app, _ = _file_app(monkeypatch, tmp_path, "admin.db")
    runner = app.test_cli_runner()

    assert runner.invoke(args=["db", "upgrade"]).exit_code == 0

    result = runner.invoke(
        args=["create-superadmin"],
        input=(
            "admin@example.com\n"
            "Test\n"
            "Admin\n"
            "very-secure-password\n"
            "very-secure-password\n"
        ),
    )

    assert result.exit_code == 0, result.output

    with app.app_context():
        user = db.session.scalar(
            db.select(User).where(User.email == "admin@example.com")
        )
        assert user is not None
        assert user.is_super_admin is True
        assert user.password_hash != "very-secure-password"


def test_sqlite_foreign_keys_reject_invalid_association(monkeypatch, tmp_path):
    app, _ = _file_app(monkeypatch, tmp_path, "fk.db")
    runner = app.test_cli_runner()
    assert runner.invoke(args=["db", "upgrade"]).exit_code == 0

    with app.app_context():
        with pytest.raises(IntegrityError):
            db.session.execute(
                text("INSERT INTO user_roles (user_id, role_id) VALUES (999999, 999999)")
            )
            db.session.commit()
        db.session.rollback()


def test_sqlite_numeric_preserves_decimal(monkeypatch, tmp_path):
    app, _ = _file_app(monkeypatch, tmp_path, "decimal.db")
    runner = app.test_cli_runner()
    assert runner.invoke(args=["db", "upgrade"]).exit_code == 0

    with app.app_context():
        item = Service(
            name="Decimal SQLite",
            slug="decimal-sqlite",
            base_price=Decimal("5000.00"),
            pricing_unit=PricingUnit.FIXED.value,
            is_active=True,
            is_public=True,
        )
        db.session.add(item)
        db.session.commit()
        db.session.expire_all()

        loaded = db.session.scalar(
            db.select(Service).where(Service.slug == "decimal-sqlite")
        )
        assert loaded.base_price == Decimal("5000.00")


def test_sqlite_downgrade_then_upgrade_on_temporary_database(monkeypatch, tmp_path):
    app, _ = _file_app(monkeypatch, tmp_path, "downgrade.db")
    runner = app.test_cli_runner()

    assert runner.invoke(args=["db", "upgrade"]).exit_code == 0
    down = runner.invoke(args=["db", "downgrade", "-1"])
    assert down.exit_code == 0, down.output
    up = runner.invoke(args=["db", "upgrade"])
    assert up.exit_code == 0, up.output
