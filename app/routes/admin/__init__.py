from flask import Blueprint

catalog_admin_bp = Blueprint(
    "catalog_admin",
    __name__,
    url_prefix="/admin/catalogue",
)

quote_request_admin_bp = Blueprint(
    "quote_request_admin",
    __name__,
    url_prefix="/admin/demandes-de-devis",
)

from . import catalog, quote_requests  # noqa: E402,F401
