import os
import re
from datetime import datetime
from pathlib import Path

import click
from flask import Flask, current_app, render_template, request
from flask_login import current_user, logout_user
from sqlalchemy import select, text

from config import CONFIG_BY_NAME
from .extensions import csrf, db, login_manager, migrate


def create_app(config_name: str | None = None) -> Flask:
    env_name=(config_name or os.getenv("APP_ENV","development")).lower()
    config_class=CONFIG_BY_NAME.get(env_name)
    if config_class is None:
        raise RuntimeError(f"Unknown APP_ENV '{env_name}'. Expected one of: {', '.join(sorted(CONFIG_BY_NAME))}.")
    if env_name=="production": config_class.validate()

    app=Flask(__name__,instance_relative_config=True); app.config.from_object(config_class)
    Path(app.instance_path).mkdir(parents=True,exist_ok=True); Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True,exist_ok=True)
    db.init_app(app); migrate.init_app(app,db); csrf.init_app(app); login_manager.init_app(app)

    from . import models  # noqa:F401
    from .models.auth import User
    @login_manager.user_loader
    def load_user(user_id):
        try: return db.session.get(User,int(user_id))
        except (TypeError,ValueError): return None

    from .routes.admin import admin_auth_bp,admin_core_bp,audit_admin_bp,catalog_admin_bp,quote_request_admin_bp,roles_admin_bp,users_admin_bp
    from .routes.public import public_bp
    for bp in (public_bp,admin_auth_bp,admin_core_bp,catalog_admin_bp,quote_request_admin_bp,users_admin_bp,roles_admin_bp,audit_admin_bp): app.register_blueprint(bp)

    @app.before_request
    def enforce_admin_account_state():
        if not request.path.startswith("/admin") or not current_user.is_authenticated:
            return None
        if not current_user.is_active:
            logout_user()
            return None
        allowed_when_password_change_required = {
            "admin_auth.profile",
            "admin_auth.logout",
            "static",
        }
        if current_user.must_change_password and request.endpoint not in allowed_when_password_change_required:
            from flask import redirect, url_for
            return redirect(url_for("admin_auth.profile"))
        return None

    _register_cli(app); _register_template_context(app); _register_template_filters(app); _register_error_handlers(app)
    return app


def _register_template_context(app):
    @app.context_processor
    def inject_site_context():
        whatsapp=current_app.config.get("WATO_WHATSAPP"); digits=re.sub(r"\D","",whatsapp or "")
        site={"company_name":current_app.config["WATO_COMPANY_NAME"],"tagline":current_app.config["WATO_TAGLINE"],"city":current_app.config["WATO_CITY"],"country":current_app.config["WATO_COUNTRY"],"phone":current_app.config.get("WATO_PHONE"),"email":current_app.config.get("WATO_EMAIL"),"address":current_app.config.get("WATO_ADDRESS"),"whatsapp_url":f"https://wa.me/{digits}" if digits else None,"facebook_url":current_app.config.get("WATO_FACEBOOK_URL"),"instagram_url":current_app.config.get("WATO_INSTAGRAM_URL"),"tiktok_url":current_app.config.get("WATO_TIKTOK_URL"),"og_image":current_app.config.get("WATO_OG_IMAGE")}
        structured_data={"@context":"https://schema.org","@type":"FoodEstablishment","name":site["company_name"],"description":"Traiteur & Événementiel professionnel à Yaoundé, Cameroun.","address":{"@type":"PostalAddress","addressLocality":site["city"],"addressCountry":"CM"}}
        if site["phone"]: structured_data["telephone"]=site["phone"]
        if site["email"]: structured_data["email"]=site["email"]
        return {"site":site,"structured_data":structured_data,"current_year":datetime.now().year}

def _register_template_filters(app):
    from .utils.catalog import format_money
    app.add_template_filter(format_money,"money")

def _register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(error):
        template="admin/403.html" if current_user.is_authenticated and request.path.startswith("/admin") else "errors/403.html"
        return render_template(template,page_title="Accès refusé",meta_description="Accès refusé."),403
    @app.errorhandler(404)
    def not_found(error): return render_template("errors/404.html",page_title="Page introuvable",meta_description="La page demandée est introuvable."),404
    @app.errorhandler(500)
    def internal_error(error): return render_template("errors/500.html",page_title="Erreur interne",meta_description="Une erreur interne est survenue."),500

def _register_cli(app):
    from .models.auth import Role,User
    from .services.audit import AuditService
    from .services.rbac import RBACService

    @app.cli.command("db-check")
    def db_check():
        db.session.execute(text("SELECT 1")); click.echo("Database connection: OK")

    @app.cli.command("seed-rbac")
    def seed_rbac():
        roles,permissions=RBACService.seed(); click.echo(f"RBAC prêt : {roles} rôle(s) et {permissions} permission(s) créé(s).")

    @app.cli.command("create-superadmin")
    @click.option("--email",prompt=True)
    @click.option("--first-name",prompt="Prénom")
    @click.option("--last-name",prompt="Nom")
    @click.password_option(confirmation_prompt=True)
    def create_superadmin(email,first_name,last_name,password):
        RBACService.seed()
        normalized=User.normalize_email(email)
        if db.session.scalar(select(User).where(User.email==normalized)): raise click.ClickException("Cet email existe déjà.")
        role=db.session.scalar(select(Role).where(Role.code=="SUPER_ADMIN"))
        user=User(first_name=first_name.strip(),last_name=last_name.strip(),email=normalized,is_active=True,must_change_password=False)
        try: user.set_password(password)
        except ValueError as exc: raise click.ClickException(str(exc))
        user.roles=[role]; db.session.add(user); db.session.flush(); AuditService.log("user.superadmin_create","User",user.id,"Création initiale SUPER_ADMIN",user=user); db.session.commit()
        click.echo(f"SUPER_ADMIN créé : {user.email}")
