from flask import Blueprint

catalog_admin_bp = Blueprint(
    "catalog_admin",
    __name__,
    url_prefix="/admin/catalogue",
)

from . import catalog  # noqa: E402,F401
