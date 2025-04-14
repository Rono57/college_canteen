// core/static/js/main.js
// Placeholder for API calls
const token = localStorage.getItem('access_token');
if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login/';
}