/*const categories = [
  { name: "Mess / Food", emoji: "🍽️", desc: "Food, Hygiene, Menu" },
  { name: "Electricity", emoji: "💡", desc: "Light, Fan, Power Cut" },
  { name: "Hostel / Room", emoji: "🛏️", desc: "Bed, Washroom, Cleaning" },
  { name: "Wi-Fi / IT", emoji: "📶", desc: "Internet, Login Issue" },
  { name: "Water", emoji: "💧", desc: "RO, Geyser, Leakage" },
  { name: "Academics", emoji: "📚", desc: "Faculty, Timetable, Exam" },
  { name: "Transport / Bus", emoji: "🚌", desc: "Bus Timing, Route" },
  { name: "Others", emoji: "📝", desc: "Anything ..." },
];

let currentFilter = "All";
let complaints = JSON.parse(localStorage.getItem("quico_complaints") || "[]");

if (complaints.length === 0) {
  complaints = [
    { id: "QUICO-1021", name: "Aarav Sharma", enroll: "E22CSE045", category: "Mess / Food", urgency: "High", block: "A2", room: "304", title: "cold food in mess", desc: "Bad taste", status: "InProgress", date: "11 Nov 2026" },
    { id: "QUICO-1022", name: "Priya Verma", enroll: "E23BBA012", category: "Electricity", urgency: "Medium", block: "B1", room: "112", title: "Fan is not working Properly", desc: "from tommorow fan is not working.", status: "Pending", date: "11 Nov 2026" },
    { id: "QUICO-1023", name: "Rohan Gupta", enroll: "E22CSE089", category: "Wi-Fi / IT", urgency: "Low", block: "C3", room: "210", title: "just 1mbps speed", desc: "Wi fi speed is so slow .", status: "Resolved", date: "10 Nov 2026" },
  ];
  saveData();
}

function saveData() {
  localStorage.setItem("quico_complaints", JSON.stringify(complaints));
}

function doLogin() {
  const email = document.getElementById("loginEmail").value.trim();
  const pass = document.getElementById("loginPass").value.trim();
  const err = document.getElementById("loginError");
  if (!email.endsWith("@bennett.edu.in")) { err.innerText = "Only login with Bennett id @bennett.edu.in"; return; }
  if (pass.length < 3) { err.innerText = "Password daalo."; return; }
  document.getElementById("loginScreen").classList.add("hidden");
  document.getElementById("app").classList.remove("hidden");
  document.getElementById("userName").innerText = "Hi, " + email.split("@")[0];
  renderCategories();
  renderList();
}

function doLogout() {
  document.getElementById("app").classList.add("hidden");
  document.getElementById("loginScreen").classList.remove("hidden");
}

function renderCategories() {
  document.getElementById("categoryGrid").innerHTML = categories.map(c => `
    <div class="card" onclick="selectCategory('${c.name}')">
      <div class="emoji">${c.emoji}</div><b>${c.name}</b><small>${c.desc}</small>
    </div>`).join("");
}

function selectCategory(name) {
  document.getElementById("fCategory").value = name;
  document.getElementById("formTitle").innerText = "Raise a Complaint — " + name;
  document.getElementById("formBox").scrollIntoView({ behavior: "smooth" });
}

function scrollToForm() {
  document.getElementById("formBox").scrollIntoView({ behavior: "smooth" });
}

function submitComplaint() {
  const name = document.getElementById("fName").value.trim();
  const enroll = document.getElementById("fEnroll").value.trim();
  const title = document.getElementById("fTitle").value.trim();
  const desc = document.getElementById("fDesc").value.trim();
  const msg = document.getElementById("formMsg");
  if (!name || !enroll || !title || !desc) {
    msg.style.color = "red";
    msg.innerText = "Please Fill Name, Enrollment, Title and details .";
    return;
  }
  const id = "QUICO-" + (1024 + complaints.length);
  const newC = {
    id, name, enroll,
    category: document.getElementById("fCategory").value,
    urgency: document.getElementById("fUrgency").value,
    block: document.getElementById("fBlock").value.trim(),
    room: document.getElementById("fRoom").value.trim(),
    title, desc, status: "Pending",
    date: new Date().toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })
  };
  complaints.unshift(newC);
  saveData();
  renderList();
  clearForm();
  msg.style.color = "green";
  msg.innerText = "✅ Complaint Submitted! Your Id is: " + id + " — Note it down.";
}

function clearForm() {
  ["fName", "fEnroll", "fBlock", "fRoom", "fTitle", "fDesc"].forEach(i => document.getElementById(i).value = "");
  document.getElementById("fPhoto").value = "";
}

function setFilter(f, btn) {
  currentFilter = f;
  document.querySelectorAll("#filterRow button").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  renderList();
}

function renderList() {
  const q = document.getElementById("searchId").value.trim().toLowerCase();
  let list = complaints.filter(c => (currentFilter === "All" || c.category === currentFilter) && (!q || c.id.toLowerCase().includes(q) || c.title.toLowerCase().includes(q)));
  document.getElementById("totalCount").innerText = complaints.length;
  document.getElementById("pendingCount").innerText = complaints.filter(c => c.status !== "Resolved").length;
  document.getElementById("resolvedCount").innerText = complaints.filter(c => c.status === "Resolved").length;
  const box = document.getElementById("complaintList");
  if (list.length === 0) { box.innerHTML = "<p style='color:#888; text-align:center; padding:20px;'>Koi complaint nahi mili is filter me.</p>"; return; }
  box.innerHTML = list.map(c => {
    const realIdx = complaints.indexOf(c);
    return `<div class="complaint">
      <div style="display:flex; justify-content:space-between; gap:10px;"><b>${c.title}</b><span class="meta">${c.id}</span></div>
      <p>${c.desc}</p>
      <div class="meta">${c.name} • ${c.enroll} • ${c.category} • Block ${c.block || "-"} Room ${c.room || "-"} • ${c.date}</div>
      <span class="badge ${c.status}">${c.status === "InProgress" ? "In Progress" : c.status}</span>
      <span class="badge ${c.urgency}">${c.urgency} Priority</span>
      <div>
        <button class="small-btn" onclick="changeStatus(${realIdx},'InProgress')">⏳ In Progress</button>
        <button class="small-btn" onclick="changeStatus(${realIdx},'Resolved')">✅ Resolved</button>
        <button class="small-btn" onclick="deleteComplaint(${realIdx})">🗑️ Delete</button>
      </div>
    </div>`;
  }).join("");
}

function changeStatus(i, s) { complaints[i].status = s; saveData(); renderList(); }
function deleteComplaint(i) { if (confirm("should I delete it?")) { complaints.splice(i, 1); saveData(); renderList(); } }*/
//The End//