function toggleForm(id) {
    const f = document.getElementById(id);
    f.style.display = f.style.display === 'none' ? 'flex' : 'none';
}

function addTargetInput() {
    const container = document.getElementById('targetInputs');
    if (container.querySelectorAll('.target-group').length >= 3) return alert("Max 3 targets");

    const div = document.createElement('div');
    div.className = 'target-group';
    div.innerHTML = `
        <input type="text" class="t-name" placeholder="Target Name" style="margin-top:5px;">
        <input type="text" class="t-country" placeholder="Country">
    `;
    container.appendChild(div);
}

async function addCat() {
    const data = {
        name: document.getElementById('cName').value,
        years_experience: 1,
        breed: document.getElementById('cBreed').value,
        salary: parseFloat(document.getElementById('cSalary').value)
    };

    const res = await fetch('/cats/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });

    if (res.ok) {
        location.reload();
    } else {
        alert("Check breed or auth");
    }
}

async function createMission() {
    const names = document.querySelectorAll('.t-name');
    const countries = document.querySelectorAll('.t-country');

    const targets = [];
    for (let i = 0; i < names.length; i++) {
        if (names[i].value) {
            targets.push({
                name: names[i].value,
                country: countries[i].value,
                notes: "",
                is_completed: false
            });
        }
    }

    const res = await fetch('/missions/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ targets: targets })
    });

    if (res.ok) {
        location.reload();
    } else {
        alert("Error creating mission");
    }
}

// Рендер при загрузке
async function init() {
    const res = await fetch('/cats/all');
    if (res.ok) {
        const cats = await res.json();
        if (cats.length > 0) {
            document.getElementById('catList').innerHTML = cats.map(c => `
                <div class="card">
                    <strong>${c.name}</strong> <small>${c.breed}</small>
                    <div style="font-size:12px; color:var(--muted)">$${c.salary}</div>
                </div>
            `).join('');
        }
    }
}
init();