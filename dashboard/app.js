const API_URL = "http://127.0.0.1:8000";


const API_KEY = "secret123";

async function loadLeads() {
    try {
        const res = await fetch(`${API_URL}/api/leads/scores`, {
            headers: {
                "X-API-KEY": API_KEY
            }
        });

        const result = await res.json();

        console.log("API response:", result); 

        let leads = [];

        
        if (Array.isArray(result)) {
            leads = result;
        } else if (result.data && Array.isArray(result.data.results)) {
            leads = result.data.results;
        } else {
            console.error("Unexpected API format:", result);
        }

        renderTable(leads);

    } catch (err) {
        console.error("Fetch error:", err);
    }
}

function renderTable(data) {
    const table = document.querySelector("#leadTable tbody");
    table.innerHTML = "";

    if (!Array.isArray(data)) {
        console.error("Invalid data format:", data);
        return;
    }

    data.forEach(lead => {
        
        let color = "lightgreen";
        if (lead.score < 40) color = "#ffcccc";
        else if (lead.score < 70) color = "#fff3cd";

       
        const name = lead.name || lead.client || lead.lead_id || lead.id || "N/A";
        const score = lead.score ?? "N/A";
        const stage = lead.stage || lead.status || lead.stage_name || "Scored";

        const row = `
            <tr style="background:${color}">
                <td>${name}</td>
                <td>${score}</td>
                <td>${stage}</td>
            </tr>
        `;
        table.innerHTML += row;
    });
}


loadLeads();