from flask import abort,flash,redirect,render_template,request,url_for
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ...extensions import db
from ...forms.rbac import RolePermissionsForm
from ...models.auth import Permission,Role
from ...services.audit import AuditService
from ...services.rbac import permission_required
from . import roles_admin_bp

@roles_admin_bp.get("/")
@permission_required("role.view")
def index():
 items=db.session.scalars(select(Role).options(selectinload(Role.permissions)).order_by(Role.name)).unique().all()
 return render_template("admin/roles/list.html",items=items,title="Rôles")

@roles_admin_bp.route("/<int:role_id>",methods=["GET","POST"])
@permission_required("role.manage")
def edit(role_id):
 role=db.get_or_404(Role,role_id)
 if role.code=="SUPER_ADMIN": abort(403)
 form=RolePermissionsForm(obj=role); perms=db.session.scalars(select(Permission).order_by(Permission.code)).all(); form.permission_ids.choices=[(p.id,p.code) for p in perms]
 if request.method=="GET": form.permission_ids.data=[p.id for p in role.permissions]
 if form.validate_on_submit():
  role.name=form.name.data.strip(); role.description=form.description.data or None; role.permissions=[p for p in perms if p.id in set(form.permission_ids.data)]; AuditService.log("role.permissions_change","Role",role.id,user=current_user); db.session.commit(); flash("Rôle mis à jour.","success"); return redirect(url_for("roles_admin.index"))
 return render_template("admin/roles/form.html",form=form,role=role,title="Modifier rôle")
