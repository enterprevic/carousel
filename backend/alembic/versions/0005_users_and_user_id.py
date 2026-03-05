"""add users table and user_id to carousels

Revision ID: 0005
Revises: 0004
Create Date: 2024-01-05 00:00:00.000000
"""
from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            username VARCHAR(64) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
        )
    """)
    op.execute(
        "ALTER TABLE carousels ADD COLUMN user_id UUID REFERENCES users(id) ON DELETE CASCADE"
    )
    op.execute("CREATE INDEX ix_carousels_user_id ON carousels(user_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_carousels_user_id")
    op.execute("ALTER TABLE carousels DROP COLUMN IF EXISTS user_id")
    op.execute("DROP TABLE IF EXISTS users")
