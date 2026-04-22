// ui/js/ws.js
// Simple resilient websocket with critical beep loop until resolved
const alertSound = new Audio("https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg");
alertSound.preload = "auto";

let ws;
let reconnectTimer = null;
const activeBeep = new Map(); // alertId -> intervalId

function connectAlertWS(onAlert) {
  const url = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + "/ws/alerts";
  ws = new WebSocket(url);

  ws.onopen = () => {
    console.log("WS CONNECTED");
    if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
  };

  ws.onmessage = (e) => {
    let alerts;
    try { alerts = JSON.parse(e.data); } catch { return; }
    onAlert(alerts || []);

    // beep logic: for any CRITICAL and ACTIVE alert -> start beep; stop when it's no longer present
    const critActive = alerts.filter(a => a.severity === "CRITICAL" && a.status === "ACTIVE");
    const presentIds = new Set(critActive.map(a => a.id));
    // start beep for new
    critActive.forEach(a => {
      if (!activeBeep.has(a.id)) {
        // play immediately and then repeat every 4s until resolved
        try { alertSound.currentTime = 0; alertSound.play(); } catch(e) { console.warn("autoplay blocked", e); }
        const interval = setInterval(() => {
          try { alertSound.currentTime = 0; alertSound.play(); } catch(e){}
        }, 4000);
        activeBeep.set(a.id, interval);
      }
    });

    // stop beep for resolved/absent ones
    for (const [id, iv] of activeBeep) {
      if (!presentIds.has(id)) {
        clearInterval(iv);
        activeBeep.delete(id);
      }
    }
  };

  ws.onclose = (e) => {
    console.log("WS CLOSED, reconnecting in 3s", e.reason || '');
    // stop any active beep (client closed)
    for (const iv of activeBeep.values()) clearInterval(iv);
    activeBeep.clear();
    reconnectTimer = setTimeout(()=> connectAlertWS(onAlert), 3000);
  };

  ws.onerror = (err) => {
    console.warn("WS ERROR", err);
    ws && ws.close();
  };
}

// helper to call from other scripts
window.connectAlertWS = connectAlertWS;