from fastapi import APIRouter
from app.db import get_connection

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/overview")
def dashboard_overview():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
          a.account_name,
          COUNT(DISTINCT r.id) AS total_resources,
          SUM(CASE WHEN al.severity = 'critical' THEN 1 ELSE 0 END) AS critical,
          SUM(CASE WHEN al.severity = 'warning' THEN 1 ELSE 0 END) AS warning,
          SUM(CASE WHEN al.severity = 'ok' THEN 1 ELSE 0 END) AS ok
        FROM aws_accounts a
        LEFT JOIN resources r ON r.aws_account_id = a.id
        LEFT JOIN alerts al ON al.resource_id = r.id AND al.resolved_at IS NULL
        WHERE a.status = 'active'
        GROUP BY a.id
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
