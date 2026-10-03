from __future__ import annotations

from functools import wraps

from flask import abort
from flask_login import current_user, login_required
from sqlalchemy import select

from ..extensions import db
from ..models.auth import Permission, Role, User


ROLE_MATRIX = {
    "SUPER_ADMIN": set(),
    "ADMIN": {
        "dashboard.view",
        "catalog.view", "catalog.create", "catalog.edit", "catalog.validate",
        "quote_request.view", "quote_request.edit", "quote_request.validate",
        "user.view", "user.create", "user.edit",
        "role.view",
        "audit.view",
        "settings.view",
    },
    "COMMERCIAL": {
        "dashboard.view",
        "catalog.view",
        "quote_request.view", "quote_request.edit", "quote_request.validate",
    },
    "CUISINE": {"dashboard.view", "catalog.view"},
    "LOGISTIQUE": {"dashboard.view", "catalog.view", "quote_request.view"},
    "COMPTABILITE": {"dashboard.view", "catalog.view", "quote_request.view", "audit.view"},
    "PERSONNEL": {"dashboard.view"},
}

PERMISSIONS = {
    "dashboard.view": "Consulter le tableau de bord",
    "catalog.view": "Consulter le catalogue",
    "catalog.create": "Créer des éléments du catalogue",
    "catalog.edit": "Modifier des éléments du catalogue",
    "catalog.validate": "Publier/valider des éléments du catalogue",
    "quote_request.view": "Consulter les demandes de devis",
    "quote_request.edit": "Traiter les demandes de devis",
    "quote_request.validate": "Valider les transitions des demandes",
    "user.view": "Consulter les utilisateurs",
    "user.create": "Créer des utilisateurs",
    "user.edit": "Modifier les utilisateurs",
    "role.view": "Consulter les rôles",
    "role.manage": "Gérer les permissions des rôles",
    "audit.view": "Consulter l'audit",
    "settings.view": "Consulter les paramètres",
}

ROLE_LABELS = {
    "SUPER_ADMIN": "Super administrateur",
    "ADMIN": "Administrateur",
    "COMMERCIAL": "Commercial",
    "CUISINE": "Cuisine",
    "LOGISTIQUE": "Logistique",
    "COMPTABILITE": "Comptabilité",
    "PERSONNEL": "Personnel",
}


def permission_required(code: str):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped(*args, **kwargs):
            if not current_user.is_active:
                abort(403)
            if not current_user.has_permission(code):
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


class RBACService:
    @staticmethod
    def seed() -> tuple[int, int]:
        created_permissions = 0
        created_roles = 0

        permissions_by_code = {}
        for code, description in PERMISSIONS.items():
            permission = db.session.scalar(select(Permission).where(Permission.code == code))
            if permission is None:
                permission = Permission(code=code, description=description)
                db.session.add(permission)
                created_permissions += 1
            else:
                permission.description = description
            permissions_by_code[code] = permission

        db.session.flush()

        for code, label in ROLE_LABELS.items():
            role = db.session.scalar(select(Role).where(Role.code == code))
            if role is None:
                role = Role(code=code, name=label, is_system=True, is_active=True)
                db.session.add(role)
                created_roles += 1
            else:
                role.name = label
                role.is_system = True
                role.is_active = True

            if code == "SUPER_ADMIN":
                role.permissions = []
            else:
                role.permissions = [
                    permissions_by_code[p]
                    for p in sorted(ROLE_MATRIX.get(code, set()))
                ]

        db.session.commit()
        return created_roles, created_permissions

    @staticmethod
    def active_super_admin_count() -> int:
        users = db.session.scalars(select(User)).all()
        return sum(1 for user in users if user.is_active and user.is_super_admin)

    @classmethod
    def ensure_not_last_super_admin(cls, user: User, *, removing_super_admin=False, disabling=False):
        if not user.is_super_admin:
            return
        if not (removing_super_admin or disabling):
            return
        if cls.active_super_admin_count() <= 1:
            raise ValueError("Le dernier SUPER_ADMIN actif ne peut pas être désactivé ni perdre son rôle.")

    @staticmethod
    def sync_user_roles(user: User, role_ids: list[int]) -> None:
        roles = db.session.scalars(
            select(Role).where(Role.id.in_(role_ids), Role.is_active.is_(True))
        ).all() if role_ids else []
        if {role.id for role in roles} != set(role_ids):
            raise ValueError("Un rôle sélectionné est invalide.")
        removing_super = user.is_super_admin and not any(role.code == "SUPER_ADMIN" for role in roles)
        RBACService.ensure_not_last_super_admin(user, removing_super_admin=removing_super)
        user.roles = roles
