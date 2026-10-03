from flask import abort,flash,redirect,render_template,request,url_for
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ...extensions import db
from ...forms.auth import CreateUserForm,ResetPasswordForm,UserForm
from ...forms.rbac import UserRolesForm
from ...models.auth import Role,User
from ...services.audit import AuditService
from ...services.rbac import RBACService,permission_required
from ...services.users import UserService
from . import users_admin_bp

def _roles(): return [(r.id,r.name) for r in db.session.scalars(select(Role).where(Role.is_active.is_(True)).order_by(Role.name)).all()]

@users_admin_bp.get("/")
@permission_required("user.view")
def index():
 items=db.session.scalars(select(User).options(selectinload(User.roles)).order_by(User.last_name,User.first_name)).unique().all()
 return render_template("admin/users/list.html",items=items,title="Utilisateurs")

@users_admin_bp.route("/new",methods=["GET","POST"])
@permission_required("user.create")
def create():
 form=CreateUserForm(); roles=UserRolesForm(); roles.role_ids.choices=_roles()
 if form.validate_on_submit() and roles.validate_on_submit():
  try: UserService.create(first_name=form.first_name.data,last_name=form.last_name.data,email=form.email.data,phone=form.phone.data,password=form.password.data,role_ids=roles.role_ids.data,actor=current_user); flash("Utilisateur créé.","success"); return redirect(url_for("users_admin.index"))
  except ValueError as e: flash(str(e),"error")
 return render_template("admin/users/form.html",form=form,roles_form=roles,title="Nouvel utilisateur")

@users_admin_bp.route("/<int:user_id>/edit",methods=["GET","POST"])
@permission_required("user.edit")
def edit(user_id):
 user=db.get_or_404(User,user_id); form=UserForm(obj=user); roles=UserRolesForm(); roles.role_ids.choices=_roles()
 if request.method=="GET": roles.role_ids.data=[r.id for r in user.roles]
 if form.validate_on_submit() and roles.validate_on_submit():
  user.first_name=form.first_name.data.strip(); user.last_name=form.last_name.data.strip(); user.phone=(form.phone.data or "").strip() or None; user.email=User.normalize_email(form.email.data)
  try: RBACService.sync_user_roles(user,roles.role_ids.data); AuditService.log("user.roles_change","User",user.id,user=current_user); db.session.commit(); flash("Utilisateur mis à jour.","success"); return redirect(url_for("users_admin.index"))
  except ValueError as e: db.session.rollback(); flash(str(e),"error")
 return render_template("admin/users/form.html",form=form,roles_form=roles,title="Modifier utilisateur",user=user)

@users_admin_bp.post("/<int:user_id>/toggle")
@permission_required("user.edit")
def toggle(user_id):
 user=db.get_or_404(User,user_id)
 try: UserService.set_active(user,not user.is_active,actor=current_user); flash("État utilisateur mis à jour.","success")
 except ValueError as e: flash(str(e),"error")
 return redirect(url_for("users_admin.index"))

@users_admin_bp.route("/<int:user_id>/reset-password",methods=["GET","POST"])
@permission_required("user.edit")
def reset_password(user_id):
 user=db.get_or_404(User,user_id); form=ResetPasswordForm()
 if form.validate_on_submit(): UserService.reset_password(user,form.new_password.data,actor=current_user); flash("Mot de passe réinitialisé.","success"); return redirect(url_for("users_admin.index"))
 return render_template("admin/users/reset_password.html",form=form,user=user,title="Réinitialiser mot de passe")
