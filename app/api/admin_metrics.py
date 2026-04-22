from fastapi import APIRouter
from app.db import get_connection

router = APIRouter(prefix="/admin/metrics", tags=["Admin"])

@router.get("/")
def list_metrics():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM metric_catalog")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


@router.put("/{metric_id}/toggle")
def toggle_metric(metric_id: int, enabled: bool):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE metric_catalog SET enabled=%s WHERE id=%s",
        (enabled, metric_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "updated"}