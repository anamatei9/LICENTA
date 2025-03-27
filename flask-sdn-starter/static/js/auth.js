/**
 * auth.js - Handles token management and refresh
 * Place this file in your static/js/ directory
 * Include in base.html with: <script src="{{ url_for('static', filename='js/auth.js') }}"></script>
 */

document.addEventListener('DOMContentLoaded', function() {
    // Don't run on login page
    if (window.location.pathname === '/' || window.location.pathname === '/login') {
        return;
    }
    
    // Initialize token management
    initializeTokenManagement();
    
    // Setup logout handler
    setupLogout();
    
    // Initialize automatic token refresh
    setupTokenRefresh();
});

/**
 * Setup interceptor to add Authorization header to all requests
 */
function initializeTokenManagement() {
    const accessToken = localStorage.getItem('access_token');
    
    // No token means user isn't logged in
    if (!accessToken) {
        window.location.href = '/';
        return;
    }
    
    // Override fetch to automatically include token
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
        // Skip token for auth endpoints
        if (url.includes('/auth/login') || url.includes('/auth/register')) {
            return originalFetch(url, options);
        }
        
        // Add Authorization header
        options.headers = options.headers || {};
        options.headers['Authorization'] = 'Bearer ' + accessToken;
        
        return originalFetch(url, options)
            .then(response => {
                // If we get a 401 Unauthorized, redirect to login
                if (response.status === 401) {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    window.location.href = '/';
                    return Promise.reject('Session expired');
                }
                return response;
            });
    };
}

/**
 * Handle logout functionality
 */
function setupLogout() {
    const logoutLink = document.querySelector('a[href="/logout"]');
    if (!logoutLink) return;
    
    logoutLink.addEventListener('click', function(e) {
        e.preventDefault();
        
        const accessToken = localStorage.getItem('access_token');
        
        // Call backend logout to invalidate token
        if (accessToken) {
            fetch('/auth/logout', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + accessToken,
                    'Content-Type': 'application/json'
                }
            }).catch(err => console.error('Error during logout:', err));
        }
        
        // Clear tokens from localStorage
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        // Redirect to login page
        window.location.href = '/';
    });
}

/**
 * Setup automatic token refresh before expiration
 */
function setupTokenRefresh() {
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!accessToken || !refreshToken) return;
    
    // Parse JWT payload
    function parseJwt(token) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
            return JSON.parse(jsonPayload);
        } catch (e) {
            console.error('Error parsing JWT:', e);
            return null;
        }
    }
    
    // Get token expiration time
    const decodedToken = parseJwt(accessToken);
    if (!decodedToken || !decodedToken.exp) return;
    
    // Calculate when to refresh (5 minutes before expiration)
    const expirationTime = decodedToken.exp * 1000; // Convert to milliseconds
    const currentTime = Date.now();
    const timeUntilExpiration = expirationTime - currentTime;
    const refreshTime = Math.max(timeUntilExpiration - (5 * 60 * 1000), 0); // 5 min before expiration
    
    // Set timer to refresh token
    setTimeout(function() {
        refreshAccessToken();
    }, refreshTime);
}

/**
 * Call the refresh token endpoint to get a new access token
 */
function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return;
    
    fetch('/auth/refresh', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + refreshToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Refresh failed');
        }
        return response.json();
    })
    .then(data => {
        if (data.access_token) {
            // Update the access token
            localStorage.setItem('access_token', data.access_token);
            console.log('Token refreshed successfully');
            
            // Setup next refresh
            setupTokenRefresh();
        }
    })
    .catch(error => {
        console.error('Token refresh error:', error);
        // Token refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
    });
}