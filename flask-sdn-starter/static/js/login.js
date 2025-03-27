/**
 * login.js - Handles user authentication
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the login page
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Send API request
        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                // Store tokens for later use
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                
                // Redirect to dashboard
                window.location.href = '/dashboard';
            } else {
                // Handle error message
                alert('Authentication failed: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Login error:', error);
            alert('Login failed. Please check your credentials.');
        });
    });
});