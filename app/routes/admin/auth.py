from datetime import datetime,timezone
from flask import flash,redirect,render_template,request,session,url_for
from flask_login import current_user,login_required,login_user,logout_user
from sqlalchemy import select
from ...extensions import db
from ...forms.auth import ChangePasswordForm,LoginForm
from ...models.auth import User
from ...services.audit import AuditService
from ...utils.security import is_safe_next_url
from . import admin_auth_bp

@admin_auth_bp.route("/login",methods=["GET","POST"])
def login():
 if current_user.is_authenticated: return redirect(url_for("admin_core.dashboard"))
 form=LoginForm()
 if form.validate_on_submit():
  user=db.session.scalar(select(User).where(User.email==User.normalize_email(form.email.data)))
  if user and user.is_active and user.check_password(form.password.data):
   session.clear(); login_user(user,remember=bool(form.remember.data),fresh=True); user.last_login_at=datetime.now(timezone.utc); AuditService.log("auth.login","User",user.id,user=user); db.session.commit()
   nxt=request.args.get("next"); return redirect(nxt if is_safe_next_url(nxt) else url_for("admin_core.dashboard"))
  AuditService.log("auth.login_failed","Auth",description="Échec de connexion"); db.session.commit(); flash("Identifiants incorrects.","error")
 return render_template("admin/login.html",form=form,title="Connexion")

@admin_auth_bp.post("/logout")
@login_required
def logout():
 AuditService.log("auth.logout","User",current_user.id); db.session.commit(); logout_user(); session.clear(); return redirect(url_for("admin_auth.login"))

@admin_auth_bp.route("/profile",methods=["GET","POST"])
@login_required
def profile():
 form=ChangePasswordForm()
 if form.validate_on_submit():
  if not current_user.check_password(form.current_password.data): flash("Mot de passe actuel incorrect.","error")
  else:
   current_user.set_password(form.new_password.data); current_user.must_change_password=False; AuditService.log("user.password_change","User",current_user.id); db.session.commit(); flash("Mot de passe modifié.","success"); return redirect(url_for("admin_auth.profile"))
 return render_template("admin/profile.html",form=form,title="Profil")
