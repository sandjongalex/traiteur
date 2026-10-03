from sqlalchemy import select
from app.extensions import db
from app.models.auth import Role,User
from app.services.rbac import RBACService

def seed_rbac(): RBACService.seed()
def create_user(email="user@example.com",password="very-secure-password",roles=("SUPER_ADMIN",),active=True):
 seed_rbac(); user=User(first_name="Test",last_name="User",email=email,is_active=active,must_change_password=False); user.set_password(password)
 user.roles=db.session.scalars(select(Role).where(Role.code.in_(roles))).all(); db.session.add(user); db.session.commit(); return user
def login(client,email="user@example.com",password="very-secure-password"):
 return client.post("/admin/login",data={"email":email,"password":password},follow_redirects=False)
