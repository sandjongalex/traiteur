import pytest
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.auth import AuditLog,Permission,Role,User
from tests.helpers import create_user,seed_rbac

def test_password_is_hashed_and_checked(app):
 u=create_user(); assert u.password_hash!="very-secure-password"; assert u.check_password("very-secure-password"); assert not u.check_password("wrong")
def test_password_minimum_length(app):
 u=User(first_name="A",last_name="B",email="a@b.cm")
 with pytest.raises(ValueError): u.set_password("short")
def test_email_unique(app):
 u=create_user(); v=User(first_name="X",last_name="Y",email=u.email); v.set_password("another-secure-password"); db.session.add(v)
 with pytest.raises(IntegrityError): db.session.commit()
 db.session.rollback()
def test_seed_is_idempotent(app):
 seed_rbac(); counts=(db.session.query(Role).count(),db.session.query(Permission).count()); seed_rbac(); assert counts==(db.session.query(Role).count(),db.session.query(Permission).count())
def test_super_admin_bypasses_permissions(app):
 u=create_user(); assert u.has_permission("anything.future") is True
def test_audit_model(app):
 u=create_user(); a=AuditLog(user_id=u.id,action="test",resource_type="User"); db.session.add(a); db.session.commit(); assert a.id
