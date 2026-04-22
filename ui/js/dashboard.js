// ui/js/dashboard.js
// ---- AUTH GUARD ----
const token = localStorage.getItem("token");

if (!token) {
  window.location.href = "/";
}

// If not using modules, these helpers are global (getOverview/getEC2/getOpenAlerts)
async function renderOverview() {
  try {
    const data = await fetch('/dashboard/overview').then(r=>r.json());
    // data may be {service:"EC2", ok:.., warning:.., critical:..} or an array per account
    const ok = data.ok ?? (Array.isArray(data) ? data.reduce((s,d)=>s+(d.ok||0),0):0);
    const warn = data.warning ?? (Array.isArray(data) ? data.reduce((s,d)=>s+(d.warning||0),0):0);
    const crit = data.critical ?? (Array.isArray(data) ? data.reduce((s,d)=>s+(d.critical||0),0):0);

    document.getElementById('okCount').textContent = ok;
    document.getElementById('warningCount').textContent = warn;
    document.getElementById('criticalCount').textContent = crit;
    document.getElementById('lastRefresh').textContent = 'Last: ' + new Date().toLocaleTimeString();

    // Tiles (if data is array)
    const tiles = document.getElementById('accountTiles');
    tiles.innerHTML = '';
    const arr = Array.isArray(data) ? data : [{ account_name: 'EC2', ok, warning:warn, critical:crit }];
    arr.forEach(a=>{
      const div = document.createElement('div');
      div.className = 'tile';
      if (a.critical > 0) div.classList.add('critical');
      else if (a.warning > 0) div.classList.add('warning');
      div.innerHTML = `<h3>${a.account_name || 'EC2'}</h3><div class="counts"><span>OK: ${a.ok}</span><span>W: ${a.warning}</span><span>C: ${a.critical}</span></div>`;
      div.onclick = ()=> {
        document.getElementById('ec2Section').classList.remove('hidden');
        loadEC2();
      };
      tiles.appendChild(div);
    });
  } catch (e) {
    console.error("overview error", e);
  }
}

async function loadEC2(){
  const rows = await fetch('/dashboard/ec2').then(r=>r.json());
  const tbody = document.getElementById('ec2Table');
  tbody.innerHTML = '';

  rows.forEach(i => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${i.instance_id}</td>
      <td>${i.name || '-'}</td>
      <td>${i.cpu?.toFixed(2) ?? '-'}</td>
      <td>${i.environment || '-'}</td>  
      <td class="${i.status.toLowerCase()}">${i.status}</td>
    `;
    tbody.appendChild(tr);
  });
}

async function renderAlertsList(alerts){
  const list = document.getElementById('alertList');
  list.innerHTML = '';
  alerts.forEach(a=>{
    const li = document.createElement('li');
    li.className = 'alert';
    li.innerHTML = `<div class="meta"><strong>${a.metric_name}</strong> <span>${a.instance||a.resource_id}</span></div><div><span class="severity ${a.severity.toLowerCase()}">${a.severity}</span></div>`;
    list.appendChild(li);
  });
}

async function refreshAll(){
  await renderOverview();
  await loadEC2();
  const alerts = await fetch('/alerts/open').then(r=>r.json());
  renderAlertsList(alerts || []);
}

document.getElementById && document.getElementById('refreshBtn') && document.getElementById('refreshBtn').addEventListener('click', refreshAll);

refreshAll();
setInterval(refreshAll, 5000);

// connect websocket to update alerts realtime
connectAlertWS(function(alerts){ renderAlertsList(alerts); });