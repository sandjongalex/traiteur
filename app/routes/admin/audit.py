from flask import render_template,request
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ...extensions import db
from ...models.auth import AuditLog
from ...services.rbac import permission_required
from . import audit_admin_bp

@audit_admin_bp.get("/")
@permission_required("audit.view")
def index():
 action=request.args.get("action","").strip(); resource=request.args.get("resource_type","").strip()
 stmt=select(AuditLog).options(selectinload(AuditLog.user)).order_by(AuditLog.created_at.desc())
 if action: stmt=stmt.where(AuditLog.action.contains(action))
 if resource: stmt=stmt.where(AuditLog.resource_type==resource)
 items=db.session.scalars(stmt.limit(300)).all()
 return render_template("admin/audit/list.html",items=items,action=action,resource_type=resource,title="Audit")
