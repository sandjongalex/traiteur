"""Create authentication, RBAC and audit tables.

Revision ID: 20261003_03_auth_rbac
Revises: 20261003_02_quote_requests
Create Date: 2026-10-03
"""
from alembic import op
import sqlalchemy as sa
revision="20261003_03_auth_rbac"
down_revision="20261003_02_quote_requests"
branch_labels=None
depends_on=None

def upgrade():
 op.create_table("permissions",
  sa.Column("id",sa.Integer(),nullable=False),
  sa.Column("code",sa.String(120),nullable=False),
  sa.Column("description",sa.String(255),nullable=True),
  sa.Column("created_at",sa.DateTime(),nullable=False),
  sa.PrimaryKeyConstraint("id",name="pk_permissions"),
  sa.UniqueConstraint("code",name="uq_permissions_code"))
 op.create_index("ix_permissions_code","permissions",["code"],unique=False)
 op.create_table("roles",
  sa.Column("id",sa.Integer(),nullable=False),
  sa.Column("code",sa.String(50),nullable=False),
  sa.Column("name",sa.String(100),nullable=False),
  sa.Column("description",sa.String(255),nullable=True),
  sa.Column("is_system",sa.Boolean(),nullable=False),
  sa.Column("is_active",sa.Boolean(),nullable=False),
  sa.Column("created_at",sa.DateTime(),nullable=False),
  sa.Column("updated_at",sa.DateTime(),nullable=False),
  sa.PrimaryKeyConstraint("id",name="pk_roles"),
  sa.UniqueConstraint("code",name="uq_roles_code"))
 op.create_index("ix_roles_code","roles",["code"],unique=False)
 op.create_table("users",
  sa.Column("id",sa.Integer(),nullable=False),
  sa.Column("first_name",sa.String(100),nullable=False),
  sa.Column("last_name",sa.String(100),nullable=False),
  sa.Column("email",sa.String(254),nullable=False),
  sa.Column("phone",sa.String(40),nullable=True),
  sa.Column("password_hash",sa.String(255),nullable=False),
  sa.Column("is_active",sa.Boolean(),nullable=False),
  sa.Column("must_change_password",sa.Boolean(),nullable=False),
  sa.Column("last_login_at",sa.DateTime(),nullable=True),
  sa.Column("created_at",sa.DateTime(),nullable=False),
  sa.Column("updated_at",sa.DateTime(),nullable=False),
  sa.PrimaryKeyConstraint("id",name="pk_users"),
  sa.UniqueConstraint("email",name="uq_users_email"))
 op.create_index("ix_users_email","users",["email"],unique=False)
 op.create_index("ix_users_active","users",["is_active"],unique=False)
 op.create_table("user_roles",
  sa.Column("user_id",sa.Integer(),nullable=False),
  sa.Column("role_id",sa.Integer(),nullable=False),
  sa.ForeignKeyConstraint(["user_id"],["users.id"],name="fk_user_roles_user_id_users",ondelete="CASCADE"),
  sa.ForeignKeyConstraint(["role_id"],["roles.id"],name="fk_user_roles_role_id_roles",ondelete="CASCADE"),
  sa.PrimaryKeyConstraint("user_id","role_id",name="pk_user_roles"),
  sa.UniqueConstraint("user_id","role_id",name="uq_user_roles_user_role"))
 op.create_table("role_permissions",
  sa.Column("role_id",sa.Integer(),nullable=False),
  sa.Column("permission_id",sa.Integer(),nullable=False),
  sa.ForeignKeyConstraint(["role_id"],["roles.id"],name="fk_role_permissions_role_id_roles",ondelete="CASCADE"),
  sa.ForeignKeyConstraint(["permission_id"],["permissions.id"],name="fk_role_permissions_permission_id_permissions",ondelete="CASCADE"),
  sa.PrimaryKeyConstraint("role_id","permission_id",name="pk_role_permissions"),
  sa.UniqueConstraint("role_id","permission_id",name="uq_role_permissions_role_permission"))
 op.create_table("audit_logs",
  sa.Column("id",sa.Integer(),nullable=False),
  sa.Column("user_id",sa.Integer(),nullable=True),
  sa.Column("action",sa.String(100),nullable=False),
  sa.Column("resource_type",sa.String(80),nullable=False),
  sa.Column("resource_id",sa.String(80),nullable=True),
  sa.Column("description",sa.String(500),nullable=True),
  sa.Column("metadata_json",sa.Text(),nullable=True),
  sa.Column("ip_address",sa.String(64),nullable=True),
  sa.Column("created_at",sa.DateTime(),nullable=False),
  sa.ForeignKeyConstraint(["user_id"],["users.id"],name="fk_audit_logs_user_id_users",ondelete="SET NULL"),
  sa.PrimaryKeyConstraint("id",name="pk_audit_logs"))
 op.create_index("ix_audit_logs_created_at","audit_logs",["created_at"],unique=False)
 op.create_index("ix_audit_logs_resource","audit_logs",["resource_type","resource_id"],unique=False)
 op.create_index("ix_audit_logs_action","audit_logs",["action"],unique=False)

def downgrade():
 op.drop_index("ix_audit_logs_action",table_name="audit_logs"); op.drop_index("ix_audit_logs_resource",table_name="audit_logs"); op.drop_index("ix_audit_logs_created_at",table_name="audit_logs"); op.drop_table("audit_logs")
 op.drop_table("role_permissions"); op.drop_table("user_roles")
 op.drop_index("ix_users_active",table_name="users"); op.drop_index("ix_users_email",table_name="users"); op.drop_table("users")
 op.drop_index("ix_roles_code",table_name="roles"); op.drop_table("roles")
 op.drop_index("ix_permissions_code",table_name="permissions"); op.drop_table("permissions")
