import os
import sqlite3

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy import MetaData, event
from sqlalchemy.engine import Engine

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=NAMING_CONVENTION)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "admin_auth.login"
login_manager.login_message = "Connectez-vous pour accéder au back-office."
login_manager.session_protection = "strong"


@event.listens_for(Engine, "connect")
def configure_sqlite_connection(dbapi_connection, connection_record):
    """Apply SQLite-only safety/concurrency pragmas without affecting MySQL."""
    if not isinstance(dbapi_connection, sqlite3.Connection):
        return

    busy_timeout_ms = int(os.getenv("SQLITE_BUSY_TIMEOUT_MS", "5000"))
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute(f"PRAGMA busy_timeout={busy_timeout_ms}")
        if os.getenv("SQLITE_WAL_ENABLED", "1").strip().lower() not in {"0", "false", "no"}:
            cursor.execute("PRAGMA journal_mode=WAL")
    finally:
        cursor.close()
