
function toast(msg, type='success') {
  let wrap = document.querySelector('.toast-wrap');
  if (!wrap) { wrap = document.createElement('div'); wrap.className = 'toast-wrap'; document.body.appendChild(wrap); }
  const el = document.createElement('div');
  el.className = `toast-app ${type}`; el.textContent = msg;
  wrap.appendChild(el);
  setTimeout(()=> el.remove(), 3500);
}

function initTheme() {
  const saved = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
}
function toggleTheme() {
  const cur = document.documentElement.getAttribute('data-theme') || 'dark';
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}

function renderNav(active) {
  const user = getUser();
  return `
  <div class="navbar-app">
    <div class="brand">
      <div class="brand-logo">M</div>
      <div>MockForge <span style="color:var(--muted);font-weight:400;font-size:0.85rem;">AI</span></div>
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
      <button class="theme-toggle" onclick="toggleTheme()">Theme</button>
      <span style="color:var(--muted);font-size:0.9rem;">${user.name || ''}</span>
      <button class="btn btn-grad btn-sm" onclick="logout()">Logout</button>
    </div>
  </div>
  <div class="layout">
    <aside class="sidebar">
      <a href="dashboard.html" class="${active==='dashboard'?'active':''}">Dashboard</a>
      <a href="create-api.html" class="${active==='create'?'active':''}">Create API</a>
      <a href="api-management.html" class="${active==='manage'?'active':''}">My APIs</a>
      <a href="api-testing.html" class="${active==='test'?'active':''}">API Tester</a>
      <a href="ml-dashboard.html" class="${active==='ml'?'active':''}">ML Predictions</a>
      <a href="ai-docs.html" class="${active==='ai'?'active':''}">AI Docs</a>
      <a href="profile.html" class="${active==='profile'?'active':''}">Profile</a>
    </aside>
    <main class="main" id="page-main"></main>
  </div>`;
}

function mountShell(active, html) {
  initTheme();
  document.body.innerHTML = renderNav(active);
  document.getElementById('page-main').innerHTML = html;
}
