# app/collector/metrics_writer.py

from datetime import datetime
from app.db import get_connection


def write_metric(
    resource_db_id: int,
    metric_name: str,
    metric_value: float,
    timestamp: datetime | None = None
):
    """
    Append-only metric writer.
    Safe for time-series.
    NO UPSERTS by design.
    """

    if timestamp is None:
        timestamp = datetime.utcnow()

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO metrics
                (resource_id, metric_name, metric_value, metric_timestamp)
            VALUES (%s, %s, %s, %s)
        """, (
            resource_db_id,     # FK → resources.id
            metric_name.lower(),
            metric_value,
            timestamp
        ))

        conn.commit()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()