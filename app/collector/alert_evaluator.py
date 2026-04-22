from app.db import get_connection
from datetime import datetime
import json
from app.ws.publisher import publish_alert


def compare(value, threshold, op):
    if threshold is None:
        return False
    if op == ">":
        return value > threshold
    if op == ">=":
        return value >= threshold
    if op == "<":
        return value < threshold
    if op == "<=":
        return value <= threshold
    return False


def evaluate_alerts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.resource_id,
            m.metric_name,
            m.metric_value,
            m.metric_timestamp,
            r.resource_type,
            r.tags,
            t.warning_value,
            t.critical_value,
            t.comparison
        FROM metrics m
        JOIN resources r ON r.id = m.resource_id
        JOIN metric_catalog mc ON mc.metric_name = m.metric_name
        JOIN thresholds t
            ON t.metric_id = mc.id
           AND t.resource_type = r.resource_type
           AND t.enabled = 1
        JOIN (
            SELECT resource_id, metric_name, MAX(metric_timestamp) AS ts
            FROM metrics
            GROUP BY resource_id, metric_name
        ) latest
          ON latest.resource_id = m.resource_id
         AND latest.metric_name = m.metric_name
         AND latest.ts = m.metric_timestamp
    """)

    rows = cursor.fetchall()

    for row in rows:
        resource_id = row["resource_id"]
        metric_name = row["metric_name"]
        metric_value = row["metric_value"]

        tags = json.loads(row["tags"] or "{}")
        environment = tags.get("environment", "uat")

        # STEP 1: threshold check
        if compare(metric_value, row["critical_value"], row["comparison"]):
            threshold_value = row["critical_value"]
        elif compare(metric_value, row["warning_value"], row["comparison"]):
            threshold_value = row["warning_value"]
        else:
            # resolve alert
            cursor.execute("""
                UPDATE alerts
                SET status = 'RESOLVED',
                    resolved_at = NOW()
                WHERE resource_id = %s
                  AND metric_name = %s
                  AND status = 'ACTIVE'
            """, (resource_id, metric_name))
            continue

        # STEP 2: severity from environment
        if environment == "prod":
            severity = "CRITICAL"
        elif environment == "uat":
            severity = "WARNING"
        else:
            severity = "INFO"

        # STEP 3: avoid duplicate alerts
        cursor.execute("""
            SELECT id
            FROM alerts
            WHERE resource_id = %s
              AND metric_name = %s
              AND severity = %s
              AND status = 'ACTIVE'
        """, (resource_id, metric_name, severity))

        if cursor.fetchone():
            continue

        # STEP 4: insert alert
        cursor.execute("""
            INSERT INTO alerts
                (resource_id, metric_name, severity,
                 environment, status, triggered_at)
            VALUES (%s, %s, %s, %s, 'ACTIVE', %s)
        """, (
            resource_id,
            metric_name,
            severity,
            environment,
            datetime.utcnow()
        ))

        new_alert_id = cursor.lastrowid

        # STEP 5: publish alert
        publish_alert(
            alert_id=new_alert_id,
            severity=severity,
            metric=metric_name,
            value=metric_value,
            threshold=threshold_value,
            account_id=tags.get("account_id", "unknown")
        )

    conn.commit()
    cursor.close()
    conn.close()