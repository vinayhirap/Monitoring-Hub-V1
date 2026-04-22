# app/collector/alert_generator.py

import datetime
from app.db import get_connection

def evaluate_alerts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ Get latest metric per resource + metric
    cursor.execute("""
        SELECT m.resource_id, m.metric_name, m.metric_value
        FROM metrics m
        JOIN (
            SELECT resource_id, metric_name, MAX(metric_timestamp) AS ts
            FROM metrics
            GROUP BY resource_id, metric_name
        ) latest
        ON m.resource_id = latest.resource_id
        AND m.metric_name = latest.metric_name
        AND m.metric_timestamp = latest.ts
    """)
    metric_rows = cursor.fetchall()

    for m in metric_rows:
        cursor.execute("""
            SELECT *
            FROM thresholds
            WHERE metric_id = (
                SELECT id FROM metric_catalog
                WHERE metric_name = %s
                LIMIT 1
            )
            AND enabled = true
        """, (m["metric_name"],))

        threshold = cursor.fetchone()
        if not threshold:
            continue

        value = m["metric_value"]
        status = None

        if threshold["comparison"] == '>':
            if value >= threshold["critical_value"]:
                status = "critical"
            elif value >= threshold["warning_value"]:
                status = "warning"
        else:
            if value <= threshold["critical_value"]:
                status = "critical"
            elif value <= threshold["warning_value"]:
                status = "warning"

        if not status:
            continue

        # 2️⃣ Insert alert if not already open
        cursor.execute("""
            SELECT id FROM alerts
            WHERE resource_id = %s
            AND metric_name = %s
            AND status != 'resolved'
        """, (m["resource_id"], m["metric_name"]))

        exists = cursor.fetchone()
        if exists:
            continue

        cursor.execute("""
            INSERT INTO alerts
            (resource_id, metric_name, severity, triggered_at)
            VALUES (%s, %s, %s, %s)
        """, (
            m["resource_id"],
            m["metric_name"],
            status,
            datetime.datetime.utcnow()
        ))

    conn.commit()
    cursor.close()
    conn.close()