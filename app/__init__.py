import os
from pathlib import Path

import click
from flask import Flask
from sqlalchemy import text

from config import CONFIG_BY_NAME
from .extensions import csrf, db, migrate


def create_app(config_name: str | None = None) -> Flask:
    env_name = (config_name or os.getenv("APP_ENV", "development")).lower()
    config_class = CONFIG_BY_NAME.get(env_name)

    if config_class is None:
        valid = ", ".join(sorted(CONFIG_BY_NAME))
        raise RuntimeError(f"Unknown APP_ENV '{env_name}'. Expected one of: {valid}.")

    if env_name == "production":
        config_class.validate()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from .routes.public import public_bp
    app.register_blueprint(public_bp)

    _register_cli(app)
    return app


def _register_cli(app: Flask) -> None:
    @app.cli.command("db-check")
    def db_check() -> None:
        """Check that the configured database accepts a simple query."""
        db.session.execute(text("SELECT 1"))
        click.echo("Database connection: OK")
