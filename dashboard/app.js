let API_URL = "http://127.0.0.1:8000";
let API_KEY = sessionStorage.getItem("metroblue_api_key") || "";
let leadRows = [];
let sortAscending = false;

async function loadConfig() {
  try {
    const res = await fetch(`${API_URL}/api/config`);
    const result = await res.json();
    if (result?.data?.api_url) API_URL = result.data.api_url;
  } catch (err) {
    console.warn("Config endpoint unavailable, using defaults.", err);
  }
}

function ensureApiKey() {
  if (!API_KEY) {
    API_KEY = window.prompt("Enter API key for MetroBlue dashboard:", "") || "";
    sessionStorage.setItem("metroblue_api_key", API_KEY);
  }
}

async function loadLeads() {
  try {
    const res = await fetch(`${API_URL}/api/leads/scores`, {
      headers: { "X-API-KEY": API_KEY },
    });

    const result = await res.json();
    leadRows = result?.data?.results || [];
    applyFiltersAndRender();
  } catch (err) {
    console.error("Fetch error:", err);
  }
}

function applyFiltersAndRender() {
  const stageFilter = (document.getElementById("stageFilter")?.value || "").toLowerCase();
  let filtered = [...leadRows];

  if (stageFilter) {
    filtered = filtered.filter((lead) => (lead.stage || "").toLowerCase() === stageFilter);
  }

  filtered.sort((a, b) => {
    const s1 = Number(a.score ?? 0);
    const s2 = Number(b.score ?? 0);
    return sortAscending ? s1 - s2 : s2 - s1;
  });

  renderTable(filtered);
}

function renderTable(data) {
  const table = document.querySelector("#leadTable tbody");
  table.innerHTML = "";

  data.forEach((lead) => {
    const score = Number(lead.score ?? 0);
    let color = "#d4edda";
    if (score < 0.4) color = "#f8d7da";
    else if (score < 0.7) color = "#fff3cd";

    const row = `
      <tr style="background:${color}">
          <td>${lead.name || lead.lead_id || "N/A"}</td>
          <td>${score.toFixed(2)}</td>
          <td>${lead.stage || "N/A"}</td>
      </tr>
    `;
    table.innerHTML += row;
  });
}

function wireEvents() {
  document.getElementById("stageFilter")?.addEventListener("change", applyFiltersAndRender);
  document.getElementById("scoreHeader")?.addEventListener("click", () => {
    sortAscending = !sortAscending;
    applyFiltersAndRender();
  });
}

(async function init() {
  await loadConfig();
  ensureApiKey();
  wireEvents();
  await loadLeads();
})();
