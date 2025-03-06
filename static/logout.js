async function logout() {
    const response = await fetch('/logout', {
        method: 'POST',
        credentials: 'include'
    });

    if (response.ok) {
        window.location.href = '/login';
    } else {
        alert('No se pudo cerrar la sesión');
    }

    alert('Tu sesión se ha cerrado correctamente');
    window.location.href = '/login';
}