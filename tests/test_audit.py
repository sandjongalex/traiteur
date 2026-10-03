from app.extensions import db
from app.models.auth import AuditLog
from tests.helpers import create_user,login

def test_login_creates_audit(client,app):
 create_user(); login(client); assert db.session.query(AuditLog).filter_by(action="auth.login").count()==1
def test_user_deactivation_creates_audit(client,app):
 admin=create_user(); other=create_user(email="other@example.com",roles=("COMMERCIAL",)); login(client); client.post(f"/admin/users/{other.id}/toggle"); assert db.session.query(AuditLog).filter_by(action="user.deactivate").count()==1
