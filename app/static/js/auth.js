document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => showTab(tab.dataset.tab));
});

function showTab(tabName) {
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.form').forEach(form => form.classList.remove('active'));

    document.querySelector(`.tab[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}Form`).classList.add('active');
}

const validateForm = fields => fields.every(field => field.trim() !== '');

const sendRequest = async (url, data) => {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message || 'Успешно');
            return result;
        } else {

            console.error("Validation Error Details:", result.detail);
            alert(result.message || 'Ошибка данных (проверьте длину пароля/имени)');
            return null;
        }
    } catch (error) {
        console.error("Network/Server Error:", error);
        alert('Ошибка сервера');
    }
};

const handleFormSubmit = async (formType, url, data) => {

    if (!validateForm(Object.values(data))) {
        alert('Заполните все поля');
        return;
    }

    const result = await sendRequest(url, data);

    if (result && formType === 'login') {

        window.location.href = '/';
    }
};


document.getElementById('loginButton').addEventListener('click', async (event) => {
    event.preventDefault();

    const email = document.querySelector('#loginForm input[type="email"]').value;
    const password = document.querySelector('#loginForm input[type="password"]').value;

    const loginData = {
        email: email,
        password: password
    };


    await handleFormSubmit('login', '/auth/login/', loginData);
});


document.getElementById('registerButton').addEventListener('click', async (event) => {
    event.preventDefault();

    const email = document.querySelector('#registerForm input[type="email"]').value;
    const name = document.querySelector('#registerForm input[type="text"]').value;
    const password = document.querySelectorAll('#registerForm input[type="password"]')[0].value;
    const password_check = document.querySelectorAll('#registerForm input[type="password"]')[1].value;

    if (password !== password_check) {
        alert('Password incorrect');
        return;
    }

    const registerData = {
        email: email,
        name: name,
        password: password,
        password_check: password_check
    };

    await handleFormSubmit('register', '/auth/register/', registerData);
});