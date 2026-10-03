from sqlalchemy import select
from ..extensions import db
from ..models.auth import Role,User
from .audit import AuditService
from .rbac import RBACService

class UserService:
 @staticmethod
 def create(*,first_name,last_name,email,phone,password,role_ids,actor=None):
  email=User.normalize_email(email)
  if db.session.scalar(select(User).where(User.email==email)): raise ValueError("Cet email est déjà utilisé.")
  user=User(first_name=first_name.strip(),last_name=last_name.strip(),email=email,phone=(phone or "").strip() or None,must_change_password=True)
  user.set_password(password); db.session.add(user); db.session.flush(); RBACService.sync_user_roles(user,role_ids)
  AuditService.log("user.create","User",user.id,"Création utilisateur",user=actor); db.session.commit(); return user
 @staticmethod
 def set_active(user,active,actor=None):
  if not active: RBACService.ensure_not_last_super_admin(user,disabling=True)
  user.is_active=active; AuditService.log("user.activate" if active else "user.deactivate","User",user.id,user=actor); db.session.commit()
 @staticmethod
 def reset_password(user,password,actor=None):
  user.set_password(password); user.must_change_password=True; AuditService.log("user.password_reset","User",user.id,user=actor); db.session.commit()
