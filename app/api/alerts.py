# app/api/alerts.py
from typing import Optional
import datetime
import time
import logging
from fastapi import APIRouter, HTTPException
from app.db import get_connection

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alerts", tags=["Alerts"])

# Simple in-process cache — alerts list doesn't change sub-second
_alerts_cache: dict = {"data": None, "ts": 0}
_CACHE_TTL = 15  # seconds — short enough for near-realtime, avoids hammering DB


def _invalidate_cache():
    _alerts_cache["data"] = None
    _alerts_cache["ts"]   = 0


def _fetch_alerts_from_db():
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    # FORCE index on triggered_at for speed — ensure index exists:
    # ALTER TABLE alerts ADD INDEX idx_triggered (triggered_at DESC);
    cursor.execute("""
        SELECT
            id,
            resource_id                             AS resource,
            metric_name,
            severity,
            status,
            current_value,
            threshold,
            value,
            -- Ensure UTC timezone in output so frontend can convert correctly
            CONVERT_TZ(triggered_at, @@session.time_zone, '+00:00') AS triggered_at,
            CONVERT_TZ(resolved_at,  @@session.time_zone, '+00:00') AS resolved_at,
            acked,
            muted_until,
            environment
        FROM alerts
        ORDER BY triggered_at DESC
        LIMIT 200
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Append 'Z' suffix so JS Date() parses as UTC — no local-time shift
    for r in rows:
        for field in ("triggered_at", "resolved_at"):
            if r.get(field) and isinstance(r[field], datetime.datetime):
                # MySQL returns naive datetime — treat as UTC, add Z
                r[field] = r[field].strftime("%Y-%m-%dT%H:%M:%SZ")
            elif r.get(field) and isinstance(r[field], str) and not r[field].endswith("Z"):
                r[field] = r[field].rstrip("+00:00").rstrip(" UTC") + "Z"

    return rows


# ── GET all alerts (cached) ───────────────────────────────────
@router.get("")
def get_alerts():
    now = time.time()
    if _alerts_cache["data"] is not None and now - _alerts_cache["ts"] < _CACHE_TTL:
        return _alerts_cache["data"]
    rows = _fetch_alerts_from_db()
    _alerts_cache["data"] = rows
    _alerts_cache["ts"]   = now
    return rows


# ── GET open/active only ──────────────────────────────────────
@router.get("/open")
def open_alerts():
    """
    Returns only unresolved alerts — used by Overview alert strip + api.js getAlerts().
    Also cached. Invalidated on ack/resolve.
    """
    now = time.time()
    # Reuse full cache if available, filter client-side to avoid second DB call
    if _alerts_cache["data"] is not None and now - _alerts_cache["ts"] < _CACHE_TTL:
        return [a for a in _alerts_cache["data"] if a.get("status") != "resolved"]

    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            id,
            resource_id AS resource,
            metric_name,
            severity,
            status,
            current_value,
            threshold,
            value,
            CONVERT_TZ(triggered_at, @@session.time_zone, '+00:00') AS triggered_at,
            CONVERT_TZ(resolved_at,  @@session.time_zone, '+00:00') AS resolved_at,
            acked,
            environment
        FROM alerts
        WHERE resolved_at IS NULL
        ORDER BY
            FIELD(severity, 'CRITICAL', 'WARNING', 'INFO'),
            triggered_at DESC
        LIMIT 100
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    for r in rows:
        for field in ("triggered_at", "resolved_at"):
            if r.get(field) and isinstance(r[field], datetime.datetime):
                r[field] = r[field].strftime("%Y-%m-%dT%H:%M:%SZ")
            elif r.get(field) and isinstance(r[field], str) and not r[field].endswith("Z"):
                r[field] = r[field].rstrip("+00:00").rstrip(" UTC") + "Z"

    return rows


# ── ACK ───────────────────────────────────────────────────────
@router.post("/{alert_id}/ack")
@router.patch("/{alert_id}/ack")
def ack_alert(alert_id: int):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE alerts SET acked = 1, status = 'acknowledged' WHERE id = %s",
        (alert_id,)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    conn.commit()
    cursor.close()
    conn.close()
    _invalidate_cache()
    return {"status": "acknowledged"}


# ── RESOLVE ───────────────────────────────────────────────────
@router.post("/{alert_id}/resolve")
@router.patch("/{alert_id}/resolve")
def resolve_alert(alert_id: int):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE alerts SET resolved_at = UTC_TIMESTAMP(), status = 'resolved' WHERE id = %s",
        (alert_id,)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    conn.commit()
    cursor.close()
    conn.close()
    _invalidate_cache()
    return {"status": "resolved", "alert_id": alert_id}


# ── MUTE ──────────────────────────────────────────────────────
@router.post("/{alert_id}/mute")
def mute_alert(alert_id: int, minutes: int = 30):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE alerts SET muted_until = DATE_ADD(UTC_TIMESTAMP(), INTERVAL %s MINUTE) WHERE id = %s",
        (minutes, alert_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    _invalidate_cache()
    return {"status": "muted", "minutes": minutes}


# ── CLEAR ─────────────────────────────────────────────────────
@router.delete("/clear")
def clear_alerts():
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("DELETE FROM alerts WHERE resolved_at IS NULL AND acked = 0")
    conn.commit()
    affected = cur.rowcount
    cur.close()
    conn.close()
    _invalidate_cache()
    return {"status": "cleared", "count": affected}