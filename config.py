import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _database_url(default: str | None = None) -> str | None:
    value = os.getenv("DATABASE_URL", default)
    if value and value.startswith("mysql://"):
        return value.replace("mysql://", "mysql+pymysql://", 1)
    return value


def _optional_env(name: str) -> str | None:
    value = os.getenv(name, "").strip()
    return value or None


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

    WATO_COMPANY_NAME = os.getenv("WATO_COMPANY_NAME", "WATO EVENTS")
    WATO_TAGLINE = os.getenv("WATO_TAGLINE", "Vos moments, notre savoir-faire.")
    WATO_CITY = os.getenv("WATO_CITY", "Yaoundé")
    WATO_COUNTRY = os.getenv("WATO_COUNTRY", "Cameroun")
    WATO_PHONE = _optional_env("WATO_PHONE")
    WATO_WHATSAPP = _optional_env("WATO_WHATSAPP")
    WATO_EMAIL = _optional_env("WATO_EMAIL")
    WATO_ADDRESS = _optional_env("WATO_ADDRESS")
    WATO_FACEBOOK_URL = _optional_env("WATO_FACEBOOK_URL")
    WATO_INSTAGRAM_URL = _optional_env("WATO_INSTAGRAM_URL")
    WATO_TIKTOK_URL = _optional_env("WATO_TIKTOK_URL")
    WATO_OG_IMAGE = _optional_env("WATO_OG_IMAGE")


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
