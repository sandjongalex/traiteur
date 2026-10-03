from flask import Blueprint

public_bp = Blueprint("public", __name__)

from . import views  # noqa: E402,F401
