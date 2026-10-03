from tests.helpers import create_user,login

def test_login_success(client,app):
 create_user(); r=login(client); assert r.status_code in {301,302}; assert "/admin" in r.headers["Location"]
def test_login_bad_password(client,app):
 create_user(); r=login(client,password="wrong-password"); assert r.status_code==200; assert "Identifiants incorrects" in r.get_data(as_text=True)
def test_login_unknown_email(client):
 r=login(client,email="nobody@example.com"); assert r.status_code==200; assert "Identifiants incorrects" in r.get_data(as_text=True)
def test_inactive_user_cannot_login(client,app):
 create_user(active=False); r=login(client); assert r.status_code==200
def test_protected_route_requires_login(client):
 r=client.get("/admin/",follow_redirects=False); assert r.status_code in {301,302}; assert "/admin/login" in r.headers["Location"]
def test_logout(client,app):
 create_user(); login(client); r=client.post("/admin/logout",follow_redirects=False); assert r.status_code in {301,302}
def test_open_redirect_is_blocked(client,app):
 create_user(); r=client.post("/admin/login?next=https://evil.example",data={"email":"user@example.com","password":"very-secure-password"},follow_redirects=False); assert "evil.example" not in r.headers.get("Location","")
