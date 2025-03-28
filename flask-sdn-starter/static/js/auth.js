/**
 * auth.js - Handles token management for protected routes
 */
// Add this at the top of your auth.js file
console.log("auth.js loaded successfully");
window.authJsLoaded = true;

document.addEventListener('DOMContentLoaded', function() {
    // Don't run on login page
    if (window.location.pathname === '/' || window.location.pathname === '/login') {
        return;
    }
    
    console.log("Auth.js is loaded on page: " + window.location.pathname);
    
    // Check if we have a token
    const accessToken = localStorage.getItem('access_token');
    console.log("Token status:", accessToken ? "Found" : "Not found");
    
    if (!accessToken) {
        console.log("No token found, redirecting to login");
        window.location.href = '/';
        return;
    }
    
    // Add token to all XHR requests
    const originalXHR = window.XMLHttpRequest.prototype.open;
    window.XMLHttpRequest.prototype.open = function() {
        originalXHR.apply(this, arguments);
        this.addEventListener('loadstart', function() {
            const token = localStorage.getItem('access_token');
            if (token) {
                console.log("Adding token to XHR request");
                this.setRequestHeader('Authorization', 'Bearer ' + token);
            }
        });
    };
    
    // Add token to all fetch requests
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
        options = options || {};
        options.headers = options.headers || {};
        
        const token = localStorage.getItem('access_token');
        if (token) {
            console.log("Adding token to fetch request");
            options.headers['Authorization'] = 'Bearer ' + token;
        }
        
        return originalFetch(url, options);
    };
    
    // Add token to all links that lead to protected routes
    document.querySelectorAll('a').forEach(link => {
        // Skip login/logout links
        const href = link.getAttribute('href');
        if (!href || href === '/' || href === '/login' || href === '/logout') {
            return;
        }
        
        // Add click handler to intercept navigation
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Create a form to POST to the destination with the token
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = href;
            
            const tokenInput = document.createElement('input');
            tokenInput.type = 'hidden';
            tokenInput.name = 'token';
            tokenInput.value = accessToken;
            
            form.appendChild(tokenInput);
            document.body.appendChild(form);
            form.submit();
        });
    });
    
    // Setup logout handler
    const logoutLink = document.querySelector('a[href="/logout"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Call logout API to invalidate token
            fetch('/auth/logout', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + accessToken,
                    'Content-Type': 'application/json'
                }
            }).catch(err => console.error('Error during logout:', err));
            
            // Clear tokens
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            
            // Redirect to login page
            window.location.href = '/';
        });
    }
});