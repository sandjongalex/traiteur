from __future__ import annotations

import json

from flask import request
from flask_login import current_user

from ..extensions import db
from ..models.auth import AuditLog


class AuditService:
    @staticmethod
    def log(
        action: str,
        resource_type: str,
        resource_id=None,
        description: str | None = None,
        metadata: dict | None = None,
        user=None,
    ) -> AuditLog:
        actor = user
        if actor is None and getattr(current_user, "is_authenticated", False):
            actor = current_user

        forwarded = request.headers.get("X-Forwarded-For", "")
        ip_address = forwarded.split(",")[0].strip() if forwarded else request.remote_addr

        entry = AuditLog(
            user_id=getattr(actor, "id", None),
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id is not None else None,
            description=description,
            metadata_json=json.dumps(metadata, ensure_ascii=False) if metadata else None,
            ip_address=ip_address,
        )
        db.session.add(entry)
        return entry
