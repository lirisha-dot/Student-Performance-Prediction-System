const form = document.getElementById("predictForm");
const errorBox = document.getElementById("error");

const advice = {
  "Excellent": "Keep up the current routine. This student is on track for top marks.",
  "Good": "Solid performance. A little more study time could lift this to excellent.",
  "Average": "Improve attendance and assignment scores to move up a level.",
  "Needs Improvement": "At risk. Increase daily study hours and attendance, and arrange extra support."
};

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorBox.hidden = true;
  const body = Object.fromEntries(new FormData(form));
  const res = await fetch("/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  const data = await res.json();
  if (!res.ok) { errorBox.textContent = data.error; errorBox.hidden = false; return; }
  document.getElementById("marks").textContent = data.marks;
  document.getElementById("level").textContent = data.level;
  document.getElementById("advice").textContent = advice[data.level] || "";
  document.getElementById("result").hidden = false;
  loadHistory();
});

async function loadHistory() {
  const rows = await (await fetch("/api/history")).json();
  const tbody = document.getElementById("history");
  tbody.innerHTML = "";
  rows.forEach(r => {
    const tr = document.createElement("tr");
    [r.name, r.study_hours, r.attendance + "%", r.previous_marks + "%", r.assignment_score + "%",
     r.predicted_marks, r.predicted_level, r.created_at].forEach(v => {
      const td = document.createElement("td");
      td.textContent = v;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
}

async function loadMetrics(m) {
  m = m || await (await fetch("/api/metrics")).json();
  const imp = Object.entries(m.importance).map(([k, v]) => `${k.replace("_", " ")}: ${v}`).join(", ");
  document.getElementById("metrics").innerHTML =
    `<dt>Training records</dt><dd>${m.records}</dd>
     <dt>Linear Regression R²</dt><dd>${m.lr_r2}</dd>
     <dt>Linear Regression MAE</dt><dd>${m.lr_mae} marks</dd>
     <dt>Decision Tree accuracy</dt><dd>${(m.dt_accuracy * 100).toFixed(1)}%</dd>
     <dt>Tree feature importance</dt><dd>${imp}</dd>`;
}

document.getElementById("retrain").addEventListener("click", async (e) => {
  e.target.textContent = "Training…";
  const m = await (await fetch("/api/train", { method: "POST" })).json();
  loadMetrics(m);
  e.target.textContent = "Retrain from database";
});

loadHistory();
loadMetrics();
