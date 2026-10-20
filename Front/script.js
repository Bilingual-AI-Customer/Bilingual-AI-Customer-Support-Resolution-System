const API_BASE = "http://localhost:8000";
const PAGE_SIZE = 6;

let complaints = [
  {
    id: 1,
    text: "My order has not arrived even though I paid two weeks ago.",
    category: "Shipping & Delivery",
    priority: "High",
    status: "New",
    aiConfidence: 0.93,
    reply: "We apologize for the delay. We will investigate the shipment and update you within 24 hours.",
    sources: ["Shipping Policy", "Order Tracking Guide"]
  },
  {
    id: 2,
    text: "I was charged twice for the same order.",
    category: "Payments & Billing",
    priority: "High",
    status: "Needs Follow-up",
    aiConfidence: 0.97,
    reply: "We apologize for the duplicate charge. Our team will review the transaction.",
    sources: ["Refund Policy", "Payment Troubleshooting Guide"]
  },
  {
    id: 3,
    text: "المنتج وصل بحالة سيئة وعايز أستبدله.",
    category: "Products",
    priority: "Medium",
    status: "In Progress",
    aiConfidence: 0.88,
    reply: "We are sorry about that. Please share your order details so we can help with the replacement.",
    sources: ["Replacement & Return Policy"]
  },
  {
    id: 4,
    text: "How can I change my account email address?",
    category: "Account",
    priority: "Low",
    status: "Resolved",
    aiConfidence: 0.91,
    reply: "You can change your email from Settings > Account > Email.",
    sources: ["Account Settings Guide"]
  },
  {
    id: 5,
    text: "الدعم الفني مش بيرد عليا من 3 أيام.",
    category: "Customer Service",
    priority: "High",
    status: "New",
    aiConfidence: 0.85,
    reply: "We apologize for the delay. Your request needs further review by our support team.",
    sources: ["Service Level Agreement (SLA)"]
  }
];

let loadError = false;
let loading = false;
let page = 1;
let sort = { key: "id", dir: "asc" };

const PRIORITY_ORDER = { High: 3, Medium: 2, Low: 1 };
const STATUS_ORDER = { New: 1, "In Progress": 2, "Needs Follow-up": 3, Resolved: 4 };

const $ = id => document.getElementById(id);

const escapeHTML = value => String(value ?? "").replace(/[&<>"']/g, char => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#39;"
}[char]));

function badge(type, value) {
  const classValue = String(value ?? "").replace(/\s+/g, "-");
  return `<span class="badge ${type}-${escapeHTML(classValue)}">${escapeHTML(value)}</span>`;
}

function short(text) {
  text = String(text ?? "");
  return text.length > 60 ? text.slice(0, 60) + "…" : text;
}

function highlight(text, query) {
  if (!query) return escapeHTML(text);
  const lower = text.toLowerCase();
  let out = "";
  let i = 0;
  let at;
  while ((at = lower.indexOf(query, i)) !== -1) {
    out += escapeHTML(text.slice(i, at)) +
      `<mark>${escapeHTML(text.slice(at, at + query.length))}</mark>`;
    i = at + query.length;
  }
  return out + escapeHTML(text.slice(i));
}

/* ---------- Toast ---------- */
let toastTimer;
function toast(message) {
  const el = $("toast");
  el.textContent = message;
  el.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.hidden = true; }, 2600);
}

/* ---------- Theme ---------- */
function applyTheme(theme, save) {
  document.documentElement.dataset.theme = theme;
  const btn = $("theme-toggle");
  btn.textContent = theme === "dark" ? "☀️" : "🌙";
  btn.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
  if (save) {
    try { localStorage.setItem("theme", theme); } catch (e) {}
  }
}

/* ---------- Mobile menu ---------- */
function setMenu(open) {
  $("sidebar").classList.toggle("open", open);
  $("scrim").hidden = !open;
  $("menu-btn").setAttribute("aria-expanded", String(open));
}

/* ---------- Dashboard ---------- */
function renderDashboard() {
  $("stat-total").textContent = complaints.length;
  $("stat-new").textContent = complaints.filter(c => c.status === "New").length;
  $("stat-followup").textContent = complaints.filter(c => c.status === "Needs Follow-up").length;
  $("stat-resolved").textContent = complaints.filter(c => c.status === "Resolved").length;

  const recent = [...complaints].sort((a, b) => b.id - a.id).slice(0, 5);

  $("recent-body").innerHTML = recent.map(c => `
    <tr data-id="${Number(c.id)}" tabindex="0">
      <td>${Number(c.id)}</td>
      <td dir="auto">${escapeHTML(short(c.text))}</td>
      <td>${badge("p", c.priority)}</td>
      <td>${badge("s", c.status)}</td>
    </tr>
  `).join("");

  $("dashboard-empty").hidden = complaints.length > 0;
}

/* ---------- Complaints list ---------- */
function getFiltered() {
  const query = $("search").value.trim().toLowerCase();
  const status = $("filter-status").value;
  const priority = $("filter-priority").value;

  const list = complaints.filter(c =>
    String(c.text ?? "").toLowerCase().includes(query) &&
    (!status || c.status === status) &&
    (!priority || c.priority === priority)
  );

  const dir = sort.dir === "asc" ? 1 : -1;
  const value = c => {
    if (sort.key === "priority") return PRIORITY_ORDER[c.priority] || 0;
    if (sort.key === "status") return STATUS_ORDER[c.status] || 0;
    if (sort.key === "category") return String(c.category ?? "").toLowerCase();
    return Number(c.id);
  };

  return list.sort((a, b) => {
    const x = value(a), y = value(b);
    return (x > y ? 1 : x < y ? -1 : 0) * dir;
  });
}

function renderComplaints() {
  const query = $("search").value.trim().toLowerCase();
  const filtered = getFiltered();
  const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  page = Math.min(page, pages);
  const slice = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  $("complaint-count").textContent =
    `${filtered.length} ${filtered.length === 1 ? "complaint" : "complaints"}`;

  $("complaints-body").innerHTML = slice.map(c => `
    <tr data-id="${Number(c.id)}" tabindex="0">
      <td>${Number(c.id)}</td>
      <td dir="auto">${highlight(short(c.text), query)}</td>
      <td>${escapeHTML(c.category)}</td>
      <td>${badge("p", c.priority)}</td>
      <td>${badge("s", c.status)}</td>
    </tr>
  `).join("");

  document.querySelectorAll(".sort-btn").forEach(btn => {
    const active = btn.dataset.sort === sort.key;
    if (active) {
      btn.setAttribute("aria-sort", sort.dir === "asc" ? "ascending" : "descending");
    } else {
      btn.removeAttribute("aria-sort");
    }
    btn.querySelector("i").textContent = active ? (sort.dir === "asc" ? "▲" : "▼") : "↕";
  });

  $("complaints-loading").hidden = !loading;
  $("empty").hidden = filtered.length > 0 || loadError || loading;
  $("complaints-error").hidden = !loadError;
  $("complaints-table-wrap").hidden = loadError || loading || filtered.length === 0;
  $("pager").hidden = loadError || loading || filtered.length <= PAGE_SIZE;
  $("page-info").textContent = `Page ${page} of ${pages}`;
  $("prev-page").disabled = page <= 1;
  $("next-page").disabled = page >= pages;
}

/* ---------- Details ---------- */
function currentId() {
  const parts = location.hash.split("/");
  return parts[1] === "complaint" ? Number(parts[2]) : null;
}

function renderDetails(id) {
  const index = complaints.findIndex(c => c.id === Number(id));
  const complaint = complaints[index];

  if (!complaint) {
    location.hash = "#/complaints";
    return;
  }

  $("d-title").textContent = `Complaint #${complaint.id}`;
  $("d-text").textContent = complaint.text;
  $("d-category").textContent = complaint.category;

  $("d-priority").textContent = complaint.priority;
  $("d-priority").className = `badge p-${String(complaint.priority).replace(/\s+/g, "-")}`;

  $("d-status-select").value = complaint.status;
  $("d-ai-category").textContent = complaint.category;

  const confidence = Math.max(0, Math.min(100, Math.round(Number(complaint.aiConfidence || 0) * 100)));
  $("d-ai-conf").textContent = `${confidence}%`;
  $("confidence-bar").style.width = `${confidence}%`;

  $("d-reply").value = complaint.reply || "";
  $("char-count").textContent = $("d-reply").value.length;

  $("d-sources").innerHTML = (complaint.sources || [])
    .map(source => `<li>${escapeHTML(source)}</li>`)
    .join("") || "<li>No sources yet</li>";

  $("prev-complaint").disabled = index <= 0;
  $("next-complaint").disabled = index >= complaints.length - 1;
  $("reply-feedback").hidden = true;
}

function saveReply() {
  const complaint = complaints.find(c => c.id === currentId());
  if (!complaint) return;

  const reply = $("d-reply").value.trim();
  const feedback = $("reply-feedback");

  if (!reply) {
    feedback.textContent = "Please enter a reply first.";
    feedback.style.color = "#c94e55";
    feedback.hidden = false;
    return;
  }

  complaint.reply = reply;
  feedback.textContent = "Reply saved in this demo. It has not been sent to the customer.";
  feedback.style.color = "";
  feedback.hidden = false;
  toast("Reply saved");
}

async function copyReply() {
  const text = $("d-reply").value;
  if (!text) return toast("Nothing to copy");
  try {
    await navigator.clipboard.writeText(text);
  } catch (e) {
    $("d-reply").select();
    document.execCommand("copy");
  }
  toast("Reply copied");
}

function goRelative(step) {
  const index = complaints.findIndex(c => c.id === currentId());
  const target = complaints[index + step];
  if (target) location.hash = `#/complaint/${target.id}`;
}

/* ---------- Export ---------- */
function exportCSV() {
  const rows = getFiltered();
  if (!rows.length) return toast("No complaints to export");

  const cell = v => `"${String(v ?? "").replace(/"/g, '""')}"`;
  const lines = [["ID", "Complaint", "Category", "Priority", "Status", "Confidence"].join(",")]
    .concat(rows.map(c =>
      [c.id, c.text, c.category, c.priority, c.status, c.aiConfidence].map(cell).join(",")
    ));

  const blob = new Blob(["\uFEFF" + lines.join("\n")], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "complaints.csv";
  a.click();
  URL.revokeObjectURL(url);
  toast(`Exported ${rows.length} complaints`);
}

/* ---------- Routing ---------- */
function showView(name) {
  document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
  const view = $("view-" + name);
  if (view) view.classList.add("active");

  document.querySelectorAll("[data-nav]").forEach(link => {
    const active = link.dataset.nav === name || (name === "details" && link.dataset.nav === "complaints");
    link.classList.toggle("active", active);
    if (active) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });

  const headings = { dashboard: "Dashboard", complaints: "Complaints", details: "Complaint Details" };
  $("page-heading").textContent = headings[name] || "Dashboard";
  document.title = `${headings[name] || "Dashboard"} · SupportAI`;
}

function route() {
  const parts = (location.hash || "#/dashboard").split("/");
  const pageName = parts[1];
  const id = parts[2];

  setMenu(false);

  if (pageName === "complaints") {
    renderComplaints();
    showView("complaints");
  } else if (pageName === "complaint" && id) {
    renderDetails(id);
    showView("details");
  } else {
    renderDashboard();
    showView("dashboard");
  }
  window.scrollTo(0, 0);
}

/* ---------- API ---------- */
async function loadComplaintsFromApi() {
  loading = true;
  loadError = false;
  renderComplaints();

  try {
    const response = await fetch(`${API_BASE}/complaints`);
    if (!response.ok) throw new Error("Failed to load complaints");

    const data = await response.json();
    if (!Array.isArray(data)) throw new Error("Invalid complaints data");

    complaints = data;
    $("conn-status").textContent = "Connected";
  } catch (error) {
    console.warn("Backend unavailable. Using sample data.", error);
    document.querySelector(".status-dot").classList.add("offline");
    $("conn-status").textContent = "Demo data (offline)";
  } finally {
    loading = false;
    route();
  }
}

/* ---------- Events ---------- */
document.addEventListener("click", event => {
  const row = event.target.closest("tr[data-id]");
  if (row) location.hash = `#/complaint/${row.dataset.id}`;
});

document.addEventListener("keydown", event => {
  const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(event.target.tagName);

  if (event.key === "Enter" && event.target.matches("tr[data-id]")) {
    location.hash = `#/complaint/${event.target.dataset.id}`;
  } else if (event.key === "Escape") {
    setMenu(false);
  } else if (event.key === "/" && !typing) {
    event.preventDefault();
    location.hash = "#/complaints";
    setTimeout(() => $("search").focus(), 0);
  } else if (event.key === "Enter" && event.ctrlKey && event.target.id === "d-reply") {
    saveReply();
  }
});

["search", "filter-status", "filter-priority"].forEach(id => {
  $(id).addEventListener("input", () => { page = 1; renderComplaints(); });
  $(id).addEventListener("change", () => { page = 1; renderComplaints(); });
});

document.querySelectorAll(".sort-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const key = btn.dataset.sort;
    sort = { key, dir: sort.key === key && sort.dir === "asc" ? "desc" : "asc" };
    renderComplaints();
  });
});

$("clear-filters").addEventListener("click", () => {
  $("search").value = "";
  $("filter-status").value = "";
  $("filter-priority").value = "";
  page = 1;
  renderComplaints();
});

$("prev-page").addEventListener("click", () => { page--; renderComplaints(); });
$("next-page").addEventListener("click", () => { page++; renderComplaints(); });
$("retry-load").addEventListener("click", loadComplaintsFromApi);
$("export-csv").addEventListener("click", exportCSV);

$("theme-toggle").addEventListener("click", () => {
  applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark", true);
});

$("menu-btn").addEventListener("click", () => setMenu(true));
$("scrim").addEventListener("click", () => setMenu(false));

$("send-reply").addEventListener("click", saveReply);
$("copy-reply").addEventListener("click", copyReply);
$("prev-complaint").addEventListener("click", () => goRelative(-1));
$("next-complaint").addEventListener("click", () => goRelative(1));

$("d-reply").addEventListener("input", () => {
  $("char-count").textContent = $("d-reply").value.length;
});

$("d-status-select").addEventListener("change", event => {
  const complaint = complaints.find(c => c.id === currentId());
  if (!complaint) return;
  complaint.status = event.target.value;
  toast(`Status changed to ${complaint.status}`);
});

/* New complaint dialog */
const dialog = $("new-dialog");
$("add-complaint").addEventListener("click", () => {
  $("new-form").reset();
  dialog.showModal();
  $("n-text").focus();
});
$("n-cancel").addEventListener("click", () => dialog.close());

$("new-form").addEventListener("submit", event => {
  const text = $("n-text").value.trim();
  if (!text) {
    event.preventDefault();
    $("n-text").focus();
    return;
  }

  const id = complaints.reduce((max, c) => Math.max(max, Number(c.id) || 0), 0) + 1;
  complaints.push({
    id,
    text,
    category: $("n-category").value,
    priority: $("n-priority").value,
    status: "New",
    aiConfidence: 0,
    reply: "",
    sources: []
  });

  toast(`Complaint #${id} added (demo only)`);
  renderComplaints();
});

window.addEventListener("hashchange", route);

applyTheme(document.documentElement.dataset.theme || "light", false);
loadComplaintsFromApi();