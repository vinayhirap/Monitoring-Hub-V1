// src/pages/Alerts.jsx
import { useEffect, useState, useCallback } from "react";
import { useAuth } from "../auth/AuthContext";
import { useWebSocket } from "../hooks/useWebSocket";
import "./Alerts.css";

const BASE = "http://localhost:8000";

async function apiFetch(path, method = "GET", body) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body !== undefined) opts.body = JSON.stringify(body);
  const res = await fetch(`${BASE}${path}`, opts);
  if (!res.ok) {
    const d = await res.json().catch(() => ({}));
    throw new Error(d.detail || `${res.status}`);
  }
  return res.json();
}

const SEV_ORDER = { CRITICAL: 0, WARNING: 1, INFO: 2 };

export default function Alerts() {
  const { user } = useAuth();
  const role = (user?.role || "viewer").toLowerCase();
  // Only admin and editor can ack/resolve
  const canAct = role === "admin" || role === "editor";

  const [alerts,  setAlerts]  = useState([]);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState(null);
  const [tab,     setTab]     = useState("all");
  const [search,  setSearch]  = useState("");
  const [acting,  setActing]  = useState(null);

  const { lastMessage } = useWebSocket("alerts");

  const loadAlerts = useCallback(async () => {
    setError(null);
    try {
      const data = await apiFetch("/api/alerts");
      const arr  = Array.isArray(data) ? data : (data.alerts ?? []);
      setAlerts(arr.sort((a, b) =>
        (SEV_ORDER[a.severity?.toUpperCase()] ?? 9) -
        (SEV_ORDER[b.severity?.toUpperCase()] ?? 9)
      ));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAlerts();
    const t = setInterval(loadAlerts, 30000);
    return () => clearInterval(t);
  }, [loadAlerts]);

  useEffect(() => {
    if (!lastMessage || lastMessage.type !== "new_alert") return;
    setAlerts(prev => {
      const exists = prev.find(a => a.id === lastMessage.id);
      if (exists) return prev;
      return [lastMessage, ...prev].slice(0, 200);
    });
  }, [lastMessage]);

  async function handleAck(id) {
    if (!canAct) return;
    setActing(id);
    try {
      await apiFetch(`/api/alerts/${id}/ack`, "PATCH").catch(() =>
        apiFetch(`/api/alerts/${id}/ack`, "POST")
      );
      setAlerts(prev => prev.map(a =>
        a.id === id ? { ...a, status: "acknowledged" } : a
      ));
    } catch (e) {
      alert("Ack failed: " + e.message);
    } finally {
      setActing(null);
    }
  }

  async function handleResolve(id) {
    if (!canAct) return;
    setActing(id);
    try {
      await apiFetch(`/api/alerts/${id}/resolve`, "PATCH").catch(() =>
        apiFetch(`/api/alerts/${id}/resolve`, "POST")
      );
      setAlerts(prev => prev.map(a =>
        a.id === id ? { ...a, status: "resolved" } : a
      ));
    } catch (e) {
      alert("Resolve failed: " + e.message);
    } finally {
      setActing(null);
    }
  }

  const filtered = alerts.filter(a => {
    const s = (a.status || "").toLowerCase();
    if (tab === "active"       && s !== "active")       return false;
    if (tab === "critical"     && (a.severity || "").toUpperCase() !== "CRITICAL") return false;
    if (tab === "acknowledged" && s !== "acknowledged") return false;
    if (tab === "resolved"     && s !== "resolved")     return false;
    if (search) {
      const q = search.toLowerCase();
      return (
        (a.metric_name || "").toLowerCase().includes(q) ||
        (a.resource    || "").toLowerCase().includes(q) ||
        (a.severity    || "").toLowerCase().includes(q)
      );
    }
    return true;
  });

  const counts = {
    all:          alerts.length,
    active:       alerts.filter(a => (a.status || "").toLowerCase() === "active").length,
    critical:     alerts.filter(a => (a.severity || "").toUpperCase() === "CRITICAL").length,
    acknowledged: alerts.filter(a => (a.status || "").toLowerCase() === "acknowledged").length,
    resolved:     alerts.filter(a => (a.status || "").toLowerCase() === "resolved").length,
  };

  return (
    <div className="alerts-page">
      <div className="alerts-header">
        <div>
          <h1>Active <span className="accent">Alerts</span></h1>
          <p className="alerts-sub">Real-time CloudWatch alarm feed across all accounts</p>
        </div>
        <div className="alerts-header-right">
          <button className="btn-refresh" onClick={loadAlerts}>↻ Refresh</button>
          <div className="live-pill"><span className="live-dot" />LIVE</div>
        </div>
      </div>

      <div className="alerts-tabs">
        {[
          ["all",          "All"],
          ["active",       "Active"],
          ["critical",     "Critical"],
          ["acknowledged", "Acknowledged"],
          ["resolved",     "Resolved"],
        ].map(([key, label]) => (
          <button
            key={key}
            className={`atab ${tab === key ? "atab-active" : ""}`}
            onClick={() => setTab(key)}
          >
            {label}
            <span className={`atab-count ${tab === key ? "atab-count-active" : ""}`}>
              {counts[key]}
            </span>
          </button>
        ))}
        <input
          className="alerts-search"
          placeholder="Search metric, resource…"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </div>

      {loading ? (
        <div className="alerts-loading">Loading alerts…</div>
      ) : error ? (
        <div className="alerts-error">⚠ {error} <button onClick={loadAlerts}>Retry</button></div>
      ) : (
        <div className="alerts-table-wrap">
          <table className="alerts-table">
            <thead>
              <tr>
                <th>SEVERITY</th>
                <th>METRIC</th>
                <th>VALUE / THRESHOLD</th>
                <th>RESOURCE</th>
                <th>STATUS</th>
                <th>TRIGGERED</th>
                {canAct && <th>ACTION</th>}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan={canAct ? 7 : 6} className="atbl-empty">No alerts match filter.</td></tr>
              ) : filtered.map((a, idx) => {
                const sev      = (a.severity || "INFO").toUpperCase();
                const status   = (a.status   || "active").toLowerCase();
                const isActing = acting === a.id;
                return (
                  <tr key={a.id ?? idx} className={`alert-row sev-${sev.toLowerCase()}`}>
                    <td><SevBadge sev={sev} /></td>
                    <td className="alert-metric">{a.metric_name || a.alarm_name || "—"}</td>
                    <td className="mono small">
                      <span className="alert-val">{fmt(a.current_value)}</span>
                      <span className="alert-sep"> / </span>
                      <span className="alert-thr">{fmt(a.threshold)}</span>
                    </td>
                    <td className="alert-resource">{a.resource || a.resource_id || a.account_id || "—"}</td>
                    <td><StatusBadge status={status} /></td>
                    <td className="mono small">{a.triggered_at ? shortDateTime(a.triggered_at) : "—"}</td>
                    {canAct && (
                      <td>
                        <div className="alert-actions">
                          {status !== "acknowledged" && status !== "resolved" && (
                            <button className="btn-ack" disabled={isActing} onClick={() => handleAck(a.id)}>
                              {isActing ? "…" : "Ack"}
                            </button>
                          )}
                          {status !== "resolved" && (
                            <button className="btn-resolve" disabled={isActing} onClick={() => handleResolve(a.id)}>
                              {isActing ? "…" : "Resolve"}
                            </button>
                          )}
                        </div>
                      </td>
                    )}
                  </tr>
                );
              })}
            </tbody>
          </table>
          {!canAct && (
            <div style={{ padding: "8px 16px", color: "#666", fontSize: "12px" }}>
              👁 View-only — contact an Admin or Editor to acknowledge/resolve alerts.
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function SevBadge({ sev }) {
  const cls = { CRITICAL: "sev-badge sev-critical", WARNING: "sev-badge sev-warning", INFO: "sev-badge sev-info" }[sev] || "sev-badge sev-info";
  return <span className={cls}>● {sev}</span>;
}

function StatusBadge({ status }) {
  const cls = { active: "st-badge st-active", acknowledged: "st-badge st-ack", resolved: "st-badge st-resolved" }[status] || "st-badge st-active";
  return <span className={cls}>{status.toUpperCase()}</span>;
}

function fmt(v) {
  if (v == null) return "—";
  const n = parseFloat(v);
  if (isNaN(n)) return String(v);
  return n % 1 === 0 ? String(n) : n.toFixed(1);
}

function shortDateTime(iso) {
  try {
    return new Date(iso).toLocaleString("en-US", { month: "numeric", day: "numeric", year: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false });
  } catch { return iso; }
}
function shortDate(iso) {
  try {
    return new Date(iso).toLocaleDateString("en-US", { month: "numeric", day: "numeric", year: "numeric" });
  } catch { return iso; }
}
