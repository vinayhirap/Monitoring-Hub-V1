from app.db import get_connection

def get_enabled_metrics(service):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM metric_catalog
        WHERE service = %s AND enabled = true
    """, (service,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_threshold(metric_id, aws_account_id, resource_type):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM thresholds
        WHERE metric_id = %s
          AND aws_account_id = %s
          AND resource_type = %s
          AND enabled = true
        LIMIT 1
    """, (metric_id, aws_account_id, resource_type))

    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row