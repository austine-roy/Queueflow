"""Create QueueFlow core tables.

Revision ID: 20260824_0001
Revises:
Create Date: 2026-08-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260824_0001"
down_revision = None
branch_labels = None
depends_on = None

# The types are explicitly created below. Prevent table creation from issuing a
# second CREATE TYPE statement when this migration runs on PostgreSQL.
queue_status = postgresql.ENUM("NORMAL", "BUSY", "CROWDED", "CRITICAL", "CLOSED", name="queue_status", create_type=False)
camera_source_type = postgresql.ENUM("VIDEO_FILE", "RTSP", "WEBCAM", "SIMULATED", name="camera_source_type", create_type=False)
alert_severity = postgresql.ENUM("INFO", "WARNING", "CRITICAL", name="alert_severity", create_type=False)


def upgrade() -> None:
    bind = op.get_bind()
    queue_status.create(bind, checkfirst=True)
    camera_source_type.create(bind, checkfirst=True)
    alert_severity.create(bind, checkfirst=True)
    op.create_table("locations", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=200), nullable=False), sa.Column("description", sa.Text(), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False))
    op.create_table("queues", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=200), nullable=False), sa.Column("location_id", sa.Integer(), sa.ForeignKey("locations.id", ondelete="CASCADE"), nullable=False), sa.Column("capacity", sa.Integer(), nullable=False), sa.Column("status", queue_status, nullable=False, server_default="NORMAL"), sa.Column("current_count", sa.Integer(), nullable=False, server_default="0"), sa.Column("estimated_wait_time", sa.Float(), nullable=False, server_default="0"), sa.Column("density", sa.Float(), nullable=False, server_default="0"), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False))
    op.create_index("ix_queues_location_id", "queues", ["location_id"])
    op.create_table("cameras", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=200), nullable=False), sa.Column("location_id", sa.Integer(), sa.ForeignKey("locations.id", ondelete="CASCADE"), nullable=False), sa.Column("queue_id", sa.Integer(), sa.ForeignKey("queues.id", ondelete="SET NULL"), nullable=True), sa.Column("source_type", camera_source_type, nullable=False), sa.Column("source_url", sa.String(length=2048), nullable=True), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False))
    op.create_index("ix_cameras_location_id", "cameras", ["location_id"])
    op.create_index("ix_cameras_queue_id", "cameras", ["queue_id"])
    op.create_table("queue_measurements", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("queue_id", sa.Integer(), sa.ForeignKey("queues.id", ondelete="CASCADE"), nullable=False), sa.Column("person_count", sa.Integer(), nullable=False), sa.Column("density", sa.Float(), nullable=False), sa.Column("estimated_wait_time", sa.Float(), nullable=False), sa.Column("status", queue_status, nullable=False), sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False))
    op.create_index("ix_queue_measurements_queue_id", "queue_measurements", ["queue_id"])
    op.create_index("ix_queue_measurements_recorded_at", "queue_measurements", ["recorded_at"])
    op.create_table("alerts", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("queue_id", sa.Integer(), sa.ForeignKey("queues.id", ondelete="CASCADE"), nullable=False), sa.Column("type", sa.String(length=100), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("severity", alert_severity, nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_alerts_queue_id", "alerts", ["queue_id"])


def downgrade() -> None:
    op.drop_table("alerts")
    op.drop_table("queue_measurements")
    op.drop_table("cameras")
    op.drop_table("queues")
    op.drop_table("locations")
    bind = op.get_bind()
    alert_severity.drop(bind, checkfirst=True)
    camera_source_type.drop(bind, checkfirst=True)
    queue_status.drop(bind, checkfirst=True)
