"""add indexes and export error column

Revision ID: 0003
Revises: 0002
Create Date: 2024-01-03 00:00:00.000000
"""
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Indexes for the most-queried foreign keys and filter columns
    op.execute("CREATE INDEX IF NOT EXISTS idx_slides_carousel_id ON slides(carousel_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_generations_carousel_id ON generations(carousel_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_exports_carousel_id ON exports(carousel_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_carousels_status ON carousels(status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_carousels_created_at ON carousels(created_at DESC)")

    # Store error reason on failed exports
    op.execute("ALTER TABLE exports ADD COLUMN IF NOT EXISTS error TEXT")


def downgrade() -> None:
    op.execute("ALTER TABLE exports DROP COLUMN IF EXISTS error")
    op.execute("DROP INDEX IF EXISTS idx_carousels_created_at")
    op.execute("DROP INDEX IF EXISTS idx_carousels_status")
    op.execute("DROP INDEX IF EXISTS idx_exports_carousel_id")
    op.execute("DROP INDEX IF EXISTS idx_generations_carousel_id")
    op.execute("DROP INDEX IF EXISTS idx_slides_carousel_id")
