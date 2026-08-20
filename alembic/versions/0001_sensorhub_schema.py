"""Crea o actualiza el esquema inicial de SensorHub.

Revision ID: 0001_sensorhub_schema
Revises:
Create Date: 2026-08-19
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001_sensorhub_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Crea tablas faltantes y adapta bases creadas antes de usar Alembic."""
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())

    if "sensors" not in tables:
        op.create_table(
            "sensors",
            sa.Column("sensor_id", sa.String(), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("type", sa.String(), nullable=False),
            sa.Column("location", sa.String(), nullable=True),
            sa.Column("alert_threshold", sa.Float(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.PrimaryKeyConstraint("sensor_id"),
        )

    if "readings" not in tables:
        op.create_table(
            "readings",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("sensor_id", sa.String(), nullable=False),
            sa.Column("value", sa.Float(), nullable=False),
            sa.Column("unit", sa.String(), nullable=False),
            sa.Column("timestamp", sa.DateTime(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.ForeignKeyConstraint(["sensor_id"], ["sensors.sensor_id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_readings_sensor_id", "readings", ["sensor_id"])

    if "alert" not in tables:
        op.create_table(
            "alert",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("sensor_id", sa.String(), nullable=False),
            sa.Column("value", sa.Float(), nullable=False),
            sa.Column("threshold", sa.Float(), nullable=False),
            sa.Column("severity", sa.String(), nullable=False),
            sa.Column("status", sa.String(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["sensor_id"], ["sensors.sensor_id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_alert_id", "alert", ["id"])
    else:
        alert_columns = {column["name"] for column in inspector.get_columns("alert")}
        if "severity" not in alert_columns:
            op.add_column(
                "alert",
                sa.Column(
                    "severity",
                    sa.String(),
                    nullable=False,
                    server_default="WARNING",
                ),
            )


def downgrade() -> None:
    """Retira únicamente la ampliación segura para bases preexistentes."""
    inspector = sa.inspect(op.get_bind())
    if "alert" not in inspector.get_table_names():
        return

    alert_columns = {column["name"] for column in inspector.get_columns("alert")}
    if "severity" in alert_columns:
        op.drop_column("alert", "severity")
