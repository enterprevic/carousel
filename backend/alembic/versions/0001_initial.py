"""initial

Revision ID: 0001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def _create_enum_if_not_exists(name: str, values: list[str]) -> None:
    vals = ", ".join(f"'{v}'" for v in values)
    op.execute(f"""
        DO $$ BEGIN
            CREATE TYPE {name} AS ENUM ({vals});
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
    """)


def upgrade() -> None:
    _create_enum_if_not_exists("source_type_enum", ["text", "video", "links"])
    _create_enum_if_not_exists("carousel_status_enum", ["draft", "generating", "ready", "failed"])
    _create_enum_if_not_exists("generation_status_enum", ["queued", "running", "done", "failed"])
    _create_enum_if_not_exists("export_status_enum", ["queued", "running", "done", "failed"])

    op.execute("""
        CREATE TABLE IF NOT EXISTS carousels (
            id UUID PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            source_type source_type_enum NOT NULL,
            source_payload JSONB NOT NULL DEFAULT '{}',
            format JSONB NOT NULL DEFAULT '{}',
            design JSONB NOT NULL DEFAULT '{}',
            status carousel_status_enum NOT NULL DEFAULT 'draft',
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS slides (
            id UUID PRIMARY KEY,
            carousel_id UUID NOT NULL REFERENCES carousels(id) ON DELETE CASCADE,
            "order" INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL DEFAULT '',
            body TEXT NOT NULL DEFAULT '',
            footer_cta VARCHAR(255),
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            id UUID PRIMARY KEY,
            carousel_id UUID NOT NULL REFERENCES carousels(id) ON DELETE CASCADE,
            status generation_status_enum NOT NULL DEFAULT 'queued',
            tokens_used INTEGER,
            error TEXT,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS exports (
            id UUID PRIMARY KEY,
            carousel_id UUID NOT NULL REFERENCES carousels(id) ON DELETE CASCADE,
            status export_status_enum NOT NULL DEFAULT 'queued',
            file_url VARCHAR(1024),
            created_at TIMESTAMP NOT NULL
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS exports")
    op.execute("DROP TABLE IF EXISTS generations")
    op.execute("DROP TABLE IF EXISTS slides")
    op.execute("DROP TABLE IF EXISTS carousels")
    op.execute("DROP TYPE IF EXISTS export_status_enum")
    op.execute("DROP TYPE IF EXISTS generation_status_enum")
    op.execute("DROP TYPE IF EXISTS carousel_status_enum")
    op.execute("DROP TYPE IF EXISTS source_type_enum")
