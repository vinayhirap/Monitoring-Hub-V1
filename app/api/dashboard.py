from fastapi import APIRouter
from app.db import get_connection

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/overview")
def overview():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
          SUM(CASE WHEN m.metric_value < 60 THEN 1 ELSE 0 END) AS ok,
          SUM(CASE WHEN m.metric_value BETWEEN 60 AND 79 THEN 1 ELSE 0 END) AS warning,
          SUM(CASE WHEN m.metric_value >= 80 THEN 1 ELSE 0 END) AS critical
        FROM metrics m
        JOIN (
            SELECT resource_id, MAX(metric_timestamp) AS ts
            FROM metrics
            WHERE metric_name = 'cpu'
            GROUP BY resource_id
        ) latest
        ON m.resource_id = latest.resource_id
        AND m.metric_timestamp = latest.ts
    """)

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return {
        "service": "EC2",
        "ok": row["ok"] or 0,
        "warning": row["warning"] or 0,
        "critical": row["critical"] or 0
    }

