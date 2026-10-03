from flask import Blueprint

admin_auth_bp=Blueprint("admin_auth",__name__,url_prefix="/admin")
admin_core_bp=Blueprint("admin_core",__name__,url_prefix="/admin")
catalog_admin_bp=Blueprint("catalog_admin",__name__,url_prefix="/admin/catalogue")
quote_request_admin_bp=Blueprint("quote_request_admin",__name__,url_prefix="/admin/demandes-de-devis")
users_admin_bp=Blueprint("users_admin",__name__,url_prefix="/admin/users")
roles_admin_bp=Blueprint("roles_admin",__name__,url_prefix="/admin/roles")
audit_admin_bp=Blueprint("audit_admin",__name__,url_prefix="/admin/audit")
equipment_admin_bp=Blueprint("equipment_admin",__name__,url_prefix="/admin/materiel")

from . import auth,core,catalog,quote_requests,users,roles,audit,equipment  # noqa: E402,F401
