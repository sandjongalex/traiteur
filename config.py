import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _database_url(default: str | None = None) -> str | None:
    value = os.getenv("DATABASE_URL", default)
    if value and value.startswith("mysql://"):
        return value.replace("mysql://", "mysql+pymysql://", 1)
    return value


class BaseConfig:
    APP_NAME = "WATO EVENTS"
    APP_TIMEZONE = os.getenv("APP_TIMEZONE", "Africa/Douala")
    CURRENCY = os.getenv("WATO_CURRENCY", "XAF")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = _database_url(
        f"sqlite:///{BASE_DIR / 'instance' / 'wato_events.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", "8")) * 1024 * 1024
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        str(BASE_DIR / "app" / "static" / "uploads"),
    )
    WTF_CSRF_ENABLED = True
    JSON_SORT_KEYS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    SECRET_KEY = "testing-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False

    @classmethod
    def validate(cls) -> None:
        if not os.getenv("SECRET_KEY"):
            raise RuntimeError("SECRET_KEY must be defined in production.")
        if not os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL must be defined in production.")


CONFIG_BY_NAME = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
