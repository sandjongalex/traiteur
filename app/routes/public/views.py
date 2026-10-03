from flask import current_app, jsonify

from . import public_bp


@public_bp.get("/")
def index():
    return jsonify(
        {
            "project": current_app.config["APP_NAME"],
            "status": "foundation-ready",
            "next": "PROMPT 2 — Identité visuelle + site public",
        }
    )


@public_bp.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "application": current_app.config["APP_NAME"],
        }
    )
