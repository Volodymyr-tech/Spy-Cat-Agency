
function toggleForm(id) {
    const f = document.getElementById(id);
    f.style.display = f.style.display === 'none' ? 'flex' : 'none';
}


function addTargetInput() {
    const container = document.getElementById('targetInputs');
    if (container.querySelectorAll('.target-group').length >= 3) return alert("Max 3 targets allowed");

    const div = document.createElement('div');
    div.className = 'target-group';
    div.innerHTML = `
        <input type="text" class="t-name" placeholder="Target Name" style="margin-top:5px;">
        <input type="text" class="t-country" placeholder="Country">
    `;
    container.appendChild(div);
}


async function loadCats() {
    const res = await fetch('/cats/all');
    const container = document.getElementById('catList');

    if (res.ok) {
        const cats = await res.json();
        if (cats.length === 0) {
            container.innerHTML = '<div class="empty-state">No agents in the agency.</div>';
            return;
        }

        container.innerHTML = cats.map(c => `
            <div class="card" id="cat-${c.id}">
                <div>
                    <strong>${c.name}</strong> <span class="breed-badge">${c.breed}</span>
                    <div style="font-size:12px; color:var(--muted); margin-top:4px;">
                        Exp: ${c.years_experience}y | Salary: $<span class="salary-val">${c.salary}</span>
                    </div>
                </div>
                <div class="card-actions">
                    <button class="btn-action" onclick="editSalary(${c.id})">Edit $</button>
                    <button class="btn-action btn-delete" onclick="removeCat(${c.id})">Fire</button>
                </div>
            </div>
        `).join('');
    }
}


async function removeCat(id) {
    if (!confirm("Are you sure you want to fire this agent?")) return;

    const res = await fetch(`/cats/${id}/remove`, { method: 'DELETE' });
    if (res.ok) {
        loadCats();
    } else {
        alert("Failed to remove agent");
    }
}


async function editSalary(id) {
    const newSalary = prompt("Enter new salary amount:");
    if (!newSalary || isNaN(newSalary)) return;

    // Отправляем PATCH запрос (убедись, что на бэкенде такой роут есть)
    const res = await fetch(`/cats/${id}/salary?salary=${newSalary}`, {
        method: 'PATCH'
    });

    if (res.ok) {
        loadCats();
    } else {
        alert("Could not update salary");
    }
}


async function addCat() {
    const data = {
        name: document.getElementById('cName').value,
        years_experience: 1, // упростили для теста
        breed: document.getElementById('cBreed').value,
        salary: parseFloat(document.getElementById('cSalary').value)
    };

    const res = await fetch('/cats/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });

    if (res.ok) {
        document.getElementById('cName').value = '';
        toggleForm('catForm');
        loadCats();
    } else {
        const err = await res.json();
        alert("Error: " + (err.detail || "Check breed validation"));
    }
}


async function createMission() {
    const names = document.querySelectorAll('.t-name');
    const countries = document.querySelectorAll('.t-country');
    const targets = [];

    names.forEach((n, i) => {
        if (n.value.trim()) {
            targets.push({
                name: n.value,
                country: countries[i].value,
                notes: "",
                is_completed: false
            });
        }
    });

    const res = await fetch('/missions/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ targets: targets })
    });

    if (res.ok) {
        location.reload();
    } else {
        alert("Error creating mission (min 1, max 3 targets)");
    }
}


loadCats();