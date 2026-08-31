"""Add a queue-history index for recent measurement lookups."""

from alembic import op

revision = "20260902_0003"
down_revision = "20260901_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_queue_measurements_queue_recorded", "queue_measurements", ["queue_id", "recorded_at", "id"])


def downgrade() -> None:
    op.drop_index("ix_queue_measurements_queue_recorded", table_name="queue_measurements")
