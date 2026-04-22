from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
import logging

from app.api.alerts import router as alerts_router
from app.api.ec2 import router as ec2_router
from app.api.admin.accounts import router as admin_accounts_router
from app.api.admin.thresholds import router as admin_thresholds_router
from app.api.dashboard.overview import router as dashboard_overview_router
from app.api.dashboard.ec2 import router as dashboard_ec2_router
from app.api.ws.alerts import router as ws_alerts_router
from app.api.auth import router as auth_router
from app.api.admin.users import router as admin_users_router
from app.api.settings import router as settings_router

from app.ws.manager import ws_manager
from app.ws.pusher import redis_listener

from app.api.live_data import router as live_data_router
from app.api.audit_logs import router as audit_logs_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Monitoring Hub API",
    version="0.2.0",
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── STARTUP ───────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    async def safe_redis_listener():
        try:
            await redis_listener()
        except Exception as e:
            logger.warning(f"Redis listener crashed (server continues): {e}")

    asyncio.create_task(safe_redis_listener())
    logger.info("Application startup complete — Redis listener running in background")

# ── STATIC UI ─────────────────────────────────────────────────
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

# ── ROOT ──────────────────────────────────────────────────────
@app.get("/")
def login_page():
    return FileResponse("ui/login.html")

# ── WEBSOCKET ENDPOINTS ───────────────────────────────────────
@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    """
    Channels: overview | alerts | metrics
    """
    await ws_manager.connect(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text('{"type":"pong"}')
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel)

@app.get("/ws/status")
async def ws_status():
    return {"connections": ws_manager.connection_count()}

# ── API ROUTERS ───────────────────────────────────────────────
app.include_router(alerts_router, prefix="/api")
app.include_router(ec2_router)
app.include_router(admin_accounts_router)
app.include_router(admin_thresholds_router)
app.include_router(dashboard_overview_router)
app.include_router(dashboard_ec2_router)
app.include_router(ws_alerts_router)
app.include_router(auth_router)
app.include_router(admin_users_router)  # already has /api/users prefix internally
app.include_router(live_data_router)
app.include_router(audit_logs_router)
app.include_router(settings_router)