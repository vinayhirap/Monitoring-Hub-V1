// src/pages/Dashboard.jsx
import { useEffect, useState } from "react";
import { useWebSocket } from "../hooks/useWebSocket";
import { getDashboardOverview, getAlerts } from "../api/api";
import HealthGrid from "../components/HealthGrid";
import StatCard from "../components/StatCard";

export default function Dashboard() {
  const [accounts, setAccounts] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastSync, setLastSync] = useState(null);

  // ── WebSocket connections ──────────────────────────────────
  const { isConnected: overviewConnected, lastMessage: overviewMsg } =
    useWebSocket("overview");
  const { isConnected: alertsConnected, lastMessage: alertMsg } =
    useWebSocket("alerts");

  // ── Initial data load ──────────────────────────────────────
  useEffect(() => {
    loadData();
    // Fallback polling every 30s if WS not delivering
    const poll = setInterval(loadData, 30000);
    return () => clearInterval(poll);
  }, []);

  async function loadData() {
    try {
      const [overview, alertsData] = await Promise.all([
        getDashboardOverview().catch(() => ({ accounts: [] })),
        getAlerts().catch(() => []),
      ]);
      setAccounts(overview.accounts ?? overview ?? []);
      setAlerts(Array.isArray(alertsData) ? alertsData : []);
      setLastSync(new Date());
    } catch (e) {
      console.error("Dashboard load error:", e);
    } finally {
      setLoading(false);
    }
  }

  // ── Handle real-time overview updates ─────────────────────
  useEffect(() => {
    if (!overviewMsg) return;
    if (overviewMsg.type === "metric_update") {
      setAccounts((prev) =>
        prev.map((acc) => {
          if (acc.id !== overviewMsg.account_id) return acc;
          return {
            ...acc,
            services: acc.services?.map((svc) =>
              svc.name === overviewMsg.service
                ? { ...svc, cpu: overviewMsg.cpu, memory: overviewMsg.memory }
                : svc
            ),
          };
        })
      );
      setLastSync(new Date());
    }
  }, [overviewMsg]);

  // ── Handle real-time alert updates ────────────────────────
  useEffect(() => {
    if (!alertMsg) return;
    if (alertMsg.type === "new_alert") {
      setAlerts((prev) => [alertMsg, ...prev].slice(0, 50));
    }
  }, [alertMsg]);

  const criticalCount = alerts.filter((a) => a.severity === "CRITICAL").length;
  const healthyAccounts = accounts.filter((a) => a.status === "healthy").length;

  return (
    <div className="dashboard">
      {/* ── Status Bar ───────────────────────────────────── */}
      <div className="status-bar">
        <span className={`ws-indicator ${overviewConnected ? "live" : "offline"}`}>
          {overviewConnected ? "● LIVE" : "○ RECONNECTING"}
        </span>
        {lastSync && (
          <span className="last-sync">
            Last sync: {lastSync.toLocaleTimeString()}
          </span>
        )}
      </div>

      {/* ── Stat Cards ───────────────────────────────────── */}
      <div className="stat-cards">
        <StatCard
          label="Total Accounts"
          value={accounts.length}
          icon="🏢"
        />
        <StatCard
          label="Healthy"
          value={healthyAccounts}
          icon="✅"
          variant="success"
        />
        <StatCard
          label="Critical Alerts"
          value={criticalCount}
          icon="🔴"
          variant={criticalCount > 0 ? "danger" : "success"}
        />
        <StatCard
          label="WS Channels"
          value={overviewConnected && alertsConnected ? "2/2" : "0/2"}
          icon="⚡"
          variant={overviewConnected ? "success" : "warning"}
        />
      </div>

      {/* ── Account Health Grid ──────────────────────────── */}
      {loading ? (
        <div className="loading-spinner">Loading accounts...</div>
      ) : (
        <HealthGrid accounts={accounts} />
      )}

      {/* ── Active Alerts ────────────────────────────────── */}
      {alerts.length > 0 && (
        <div className="alerts-panel">
          <h3>Active Alerts ({alerts.length})</h3>
          <div className="alerts-list">
            {alerts.slice(0, 10).map((alert, i) => (
              <div
                key={alert.alert_id ?? alert.id ?? i}
                className={`alert-row severity-${(alert.severity ?? "").toLowerCase()}`}
              >
                <span className="alert-severity">{alert.severity}</span>
                <span className="alert-metric">{alert.metric_name ?? alert.metric}</span>
                <span className="alert-value">
                  {alert.current_value ?? alert.value} / {alert.threshold}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}