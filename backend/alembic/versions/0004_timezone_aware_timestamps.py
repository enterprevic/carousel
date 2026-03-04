"""convert timestamps to timezone-aware

Revision ID: 0004
Revises: 0003
Create Date: 2024-01-04 00:00:00.000000
"""
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None

# All timestamp columns that need converting
_columns = [
    ("carousels", "created_at"),
    ("carousels", "updated_at"),
    ("slides", "created_at"),
    ("slides", "updated_at"),
    ("generations", "created_at"),
    ("generations", "updated_at"),
    ("exports", "created_at"),
]


def upgrade() -> None:
    for table, col in _columns:
        op.execute(
            f"ALTER TABLE {table} "
            f"ALTER COLUMN {col} TYPE TIMESTAMP WITH TIME ZONE "
            f"USING {col} AT TIME ZONE 'UTC'"
        )


def downgrade() -> None:
    for table, col in _columns:
        op.execute(
            f"ALTER TABLE {table} "
            f"ALTER COLUMN {col} TYPE TIMESTAMP WITHOUT TIME ZONE "
            f"USING {col} AT TIME ZONE 'UTC'"
        )
