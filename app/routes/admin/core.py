from flask import render_template
from flask_login import current_user
from sqlalchemy import select
from ...extensions import db
from ...models.catalog import Menu,Pack,Service
from ...models.quote_request import QuoteRequest,QuoteRequestStatus
from ...services.rbac import permission_required
from . import admin_core_bp

@admin_core_bp.get("/")
@permission_required("dashboard.view")
def dashboard():
 counts={
 "new_requests":db.session.scalar(select(db.func.count(QuoteRequest.id)).where(QuoteRequest.status==QuoteRequestStatus.NEW.value)) or 0,
 "services":db.session.scalar(select(db.func.count(Service.id))) or 0,
 "menus":db.session.scalar(select(db.func.count(Menu.id))) or 0,
 "packs":db.session.scalar(select(db.func.count(Pack.id))) or 0}
 return render_template("admin/dashboard.html",counts=counts,title="Dashboard")
