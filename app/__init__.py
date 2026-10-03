import os
import re
from datetime import datetime
from pathlib import Path

import click
from flask import Flask, current_app, render_template
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
    _register_template_context(app)
    _register_error_handlers(app)

    return app


def _register_template_context(app: Flask) -> None:
    @app.context_processor
    def inject_site_context():
        whatsapp = current_app.config.get("WATO_WHATSAPP")
        whatsapp_digits = re.sub(r"\D", "", whatsapp or "")
        site = {
            "company_name": current_app.config["WATO_COMPANY_NAME"],
            "tagline": current_app.config["WATO_TAGLINE"],
            "city": current_app.config["WATO_CITY"],
            "country": current_app.config["WATO_COUNTRY"],
            "phone": current_app.config.get("WATO_PHONE"),
            "email": current_app.config.get("WATO_EMAIL"),
            "address": current_app.config.get("WATO_ADDRESS"),
            "whatsapp_url": (
                f"https://wa.me/{whatsapp_digits}" if whatsapp_digits else None
            ),
            "facebook_url": current_app.config.get("WATO_FACEBOOK_URL"),
            "instagram_url": current_app.config.get("WATO_INSTAGRAM_URL"),
            "tiktok_url": current_app.config.get("WATO_TIKTOK_URL"),
            "og_image": current_app.config.get("WATO_OG_IMAGE"),
        }
        structured_data = {
            "@context": "https://schema.org",
            "@type": "FoodEstablishment",
            "name": site["company_name"],
            "description": "Traiteur & Événementiel professionnel à Yaoundé, Cameroun.",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": site["city"],
                "addressCountry": "CM",
            },
        }
        if site["phone"]:
            structured_data["telephone"] = site["phone"]
        if site["email"]:
            structured_data["email"] = site["email"]
        return {
            "site": site,
            "structured_data": structured_data,
            "current_year": datetime.now().year,
        }


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(403)
    def forbidden(error):
        return render_template(
            "errors/403.html",
            page_title="Accès refusé",
            meta_description="Accès refusé.",
        ), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template(
            "errors/404.html",
            page_title="Page introuvable",
            meta_description="La page demandée est introuvable.",
        ), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template(
            "errors/500.html",
            page_title="Erreur interne",
            meta_description="Une erreur interne est survenue.",
        ), 500


def _register_cli(app: Flask) -> None:
    @app.cli.command("db-check")
    def db_check() -> None:
        """Check that the configured database accepts a simple query."""
        db.session.execute(text("SELECT 1"))
        click.echo("Database connection: OK")
