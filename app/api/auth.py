# app/api/auth.py
from fastapi import APIRouter, HTTPException, Body
from app.db import get_connection
import hashlib
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["Auth"])


def _verify_password(plain: str, stored: str) -> bool:
    """Verify password — supports bcrypt and sha256 fallback."""
    try:
        from passlib.context import CryptContext
        ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return ctx.verify(plain, stored)
    except Exception:
        # fallback: sha256
        return hashlib.sha256(plain.encode()).hexdigest() == stored


@router.post("/login")
def login(payload: dict = Body(...)):
    username = (payload.get("username") or "").strip()
    password = (payload.get("password") or "").strip()

    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")

    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Detect password column name dynamically
    cursor.execute("SHOW COLUMNS FROM users LIKE 'password%'")
    col    = cursor.fetchone()
    pw_col = col["Field"] if col else "password_hash"

    cursor.execute(
        f"SELECT id, username, role, {pw_col} AS pw FROM users WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not _verify_password(password, user["pw"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "id":       user["id"],
        "username": user["username"],
        "role":     user["role"],
    }