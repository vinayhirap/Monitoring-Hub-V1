# app/api/audit_logs.py
from fastapi import APIRouter, Depends
from app.db import get_connection
from app.auth.deps import get_current_user
import datetime

router = APIRouter(prefix="/api", tags=["audit"])


def serialize(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        if isinstance(v, (datetime.datetime, datetime.date)):
            out[k] = v.isoformat()
        else:
            out[k] = v
    return out


@router.get("/audit-logs")
def get_audit_logs(
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            id,
            actor,
            action,
            payload,
            created_at
        FROM audit_logs
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [serialize(r) for r in rows]