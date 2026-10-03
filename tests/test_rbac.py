import pytest
from app.extensions import db
from app.models.auth import Role
from app.services.rbac import RBACService
from tests.helpers import create_user,login

def test_commercial_can_view_quote_requests(client,app):
 create_user(roles=("COMMERCIAL",)); login(client); assert client.get("/admin/demandes-de-devis/").status_code==200
def test_commercial_cannot_manage_users(client,app):
 create_user(roles=("COMMERCIAL",)); login(client); assert client.get("/admin/users/").status_code==403
def test_cuisine_cannot_manage_roles(client,app):
 create_user(roles=("CUISINE",)); login(client); assert client.get("/admin/roles/").status_code==403
def test_forged_direct_request_is_denied(client,app):
 create_user(roles=("PERSONNEL",)); login(client); assert client.get("/admin/catalogue/services/new").status_code==403
def test_last_super_admin_cannot_be_disabled(client,app):
 u=create_user(); login(client)
 r=client.post(f"/admin/users/{u.id}/toggle",follow_redirects=False); db.session.refresh(u); assert u.is_active is True
def test_last_super_admin_cannot_lose_role(app):
 u=create_user(); RBACService.seed()
 with pytest.raises(ValueError): RBACService.sync_user_roles(u,[])
def test_old_catalog_session_bypass_does_not_work(client):
 with client.session_transaction() as s: s["catalog_admin"]=True
 r=client.get("/admin/catalogue/",follow_redirects=False); assert r.status_code in {301,302}; assert "/admin/login" in r.headers["Location"]
