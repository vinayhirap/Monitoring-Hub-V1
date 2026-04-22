function api(url) {
  return fetch(url, {
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  }).then(r => r.json());
}

const API_BASE = ""; // same origin by default

async function fetchJSON(path) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) throw new Error(`${path} ${res.status}`);
  return res.json();
}

async function getOverview() { return fetchJSON("/dashboard/overview"); }
async function getAccountsOverview() { return fetchJSON("/dashboard/overview"); /* you can add per-account endpoint */ }
async function getEC2() { return fetchJSON("/ec2/instances"); }
async function getOpenAlerts() { return fetchJSON("/alerts/open"); }

export { getOverview, getEC2, getOpenAlerts, fetchJSON };
