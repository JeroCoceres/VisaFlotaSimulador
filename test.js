// Obtener el token CSRF
fetch('https://f455-190-226-28-168.ngrok.io/api/get-csrf-token/')
    .then(response => response.json())
    .then(data => {
        const csrfToken = data.csrfToken;

        // Usar el token CSRF en las solicitudes
        fetch('https://f455-190-226-28-168.ngrok.io/accounts/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ username: 'admin', password: 'admin' })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
