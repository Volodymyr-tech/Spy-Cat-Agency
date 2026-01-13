const toggleForm = id => {
    const f = document.getElementById(id);
    f.style.display = f.style.display === 'none' ? 'flex' : 'none';
};

// --- КОТЫ ---
async function loadCats() {
    const res = await fetch('/cats/all');
    if (!res.ok) return;
    const cats = await res.json();
    const container = document.getElementById('catList');
    container.innerHTML = cats.length ? cats.map(c => `
        <div class="card" onclick="showDetails(${c.id})">
            <strong>${c.name}</strong> <small style="color:var(--muted)">${c.breed}</small>
            <div class="card-actions" onclick="event.stopPropagation()">
                <button class="btn-action" onclick="editSalary(${c.id})">Edit $</button>
                <button class="btn-action btn-delete" onclick="removeCat(${c.id})">Fire</button>
            </div>
        </div>
    `).join('') : '<div class="empty-state">Agency is empty</div>';
}

async function showDetails(id) {
    const res = await fetch(`/cats/${id}`);
    const cat = await res.json();
    const box = document.getElementById('catDetails');
    box.style.display = 'block';
    box.innerHTML = `<h4>Profile: ${cat.name}</h4><p>Breed: ${cat.breed}<br>Salary: $${cat.salary}<br>Exp: ${cat.years_experience}y</p><button onclick="this.parentElement.style.display='none'" class="btn-action">Close</button>`;
}

async function addCat() {
    const data = {
        name: document.getElementById('cName').value,
        years_experience: document.getElementById('cAge').value,
        breed: document.getElementById('cBreed').value,
        salary: parseFloat(document.getElementById('cSalary').value)
    };
    const res = await fetch('/cats/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    if (res.ok) {
        toggleForm('catForm');
        loadCats();
    }
}

async function editSalary(id) {
    const s = prompt("New salary:");
    if (s) {
        await fetch(`/cats/${id}/salary?salary=${s}`, { method: 'PATCH' });
        loadCats();
    }
}

async function removeCat(id) {
    if (confirm("Fire agent?")) {
        await fetch(`/cats/${id}/remove`, { method: 'DELETE' });
        loadCats();
    }
}


function addTargetInput() {
    const container = document.getElementById('targetInputs');
    if (container.querySelectorAll('.target-group').length >= 3) return alert("Max 3 targets");
    const div = document.createElement('div');
    div.className = 'target-group';
    div.innerHTML = `<input type="text" class="t-name" placeholder="Target Name" style="margin-top:5px;"><input type="text" class="t-country" placeholder="Country">`;
    container.appendChild(div);
}

async function createMission() {
    const names = document.querySelectorAll('.t-name');
    const countries = document.querySelectorAll('.t-country');
    const targets = [];
    names.forEach((n, i) => {
        if (n.value.trim()) targets.push({ name: n.value, country: countries[i].value, notes: "", is_completed: false });
    });

    const res = await fetch('/missions/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ targets: targets })
    });
    if (res.ok) {
        toggleForm('missionForm');
        loadMissions();
    } else { alert("Error: 1-3 targets required"); }
}

async function loadMissions() {
    const res = await fetch('/missions/all');
    if (!res.ok) return;
    const missions = await res.json();
    const container = document.getElementById('missionList');

    container.innerHTML = missions.length ? missions.map(m => `
        <div class="card" style="border-left-color: ${m.is_completed ? '#4caf50' : '#D4AF37'}" onclick="event.stopPropagation()">
            <div style="display:flex; justify-content:space-between">
                <strong>Mission #${m.id}</strong>
                <span>${m.is_completed ? '✅' : '🕒'}</span>
            </div>
            <div style="font-size:11px; margin: 5px 0;">Agent: ${m.cat_id ? m.cat_id : `<button class="btn-action" onclick="assignCat(${m.id})">Assign</button>`}</div>
            <div>
                ${m.targets.map(t => `
                    <div class="target-item">
                        <span>${t.is_completed ? '✅' : '🎯'} ${t.name}</span>
                        <div>
                            <button class="btn-action" onclick="editNotes(${t.id})">Notes</button>
                            ${!t.is_completed ? `<button class="btn-action" onclick="completeTarget(${t.id})">Done</button>` : ''}
                        </div>
                    </div>
                    <div style="font-size:10px; color:gray; padding-left:5px;">${t.notes || 'No notes'}</div>
                `).join('')}
            </div>
            ${!m.cat_id ? `<button class="btn-action btn-delete" style="width:100%; margin-top:10px" onclick="deleteMission(${m.id})">Abort</button>` : ''}
        </div>
    `).join('') : '<div class="empty-state">No missions</div>';
}

async function assignCat(mId) {
    const cId = prompt("Enter Cat ID:");
    if (cId) {
        const res = await fetch(`/missions/${mId}/assign/${cId}`, { method: 'PATCH' });
        if (res.ok) loadMissions(); else { const e = await res.json(); alert(e.detail); }
    }
}

async function completeTarget(tId) {
    const res = await fetch(`/missions/target/${tId}/complete`, {
        method: 'PATCH'
    });

    if (res.ok) {
        loadMissions();
    } else {
        alert("Failed to complete target");
    }
}

async function editNotes(tId) {
    const n = prompt("Notes:");
    if (n !== null) {
        const res = await fetch(`/missions/target/${tId}/notes?notes=${encodeURIComponent(n)}`, { method: 'PATCH' });
        if (res.ok) loadMissions(); else { const e = await res.json(); alert(e.detail); }
    }
}

async function deleteMission(id) {
    if (confirm("Delete mission?")) {
        await fetch(`/missions/${id}`, { method: 'DELETE' });
        loadMissions();
    }
}
async function showMissionDetails(id) {
    const res = await fetch(`/missions/${id}`);
    if (!res.ok) return alert("Mission not found");

    const m = await res.json();
    const box = document.getElementById('missionDetails');
    box.style.display = 'block';

    box.innerHTML = missions.length ? missions.map(m => `
        <div class="card" style="border-left-color: ${m.is_completed ? '#4caf50' : '#D4AF37'}" onclick="event.stopPropagation()">
            <div style="display:flex; justify-content:space-between">
                <strong>Mission #${m.id}</strong>
                <span>${m.is_completed ? '✅' : '🕒'}</span>
            </div>
            <div style="font-size:11px; margin: 5px 0;">Agent: ${m.cat_id ? m.cat_id : `<button class="btn-action" onclick="assignCat(${m.id})">Assign</button>`}</div>
            <div>
                ${m.targets.map(t => `
                    <div class="target-item">
                        <span>${t.is_completed ? '✅' : '🎯'} ${t.name}</span>
                        <div>
                            <button class="btn-action" onclick="editNotes(${t.id})">Notes</button>
                            ${!t.is_completed ? `<button class="btn-action" onclick="completeTarget(${t.id})">Done</button>` : ''}
                        </div>
                    </div>
                    <div style="font-size:10px; color:gray; padding-left:5px;">${t.notes || 'No notes'}</div>
                `).join('')}
    `).join('') : '<div class="empty-state">No missions</div>';
}


loadCats();
loadMissions();