// src/auth/authProvider.js
const authProvider = {
    // Called when the user attempts to log in
    login: ({ username, password }) => {
        return fetch('http://127.0.0.1:5000/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email: username, password }),
            headers: new Headers({ 'Content-Type': 'application/json' }),
            credentials: 'include',
        })
            .then(response => {
                if (response.status < 200 || response.status >= 300) {
                    throw new Error(response.statusText);
                }
                return response.json();
            })
            .then(auth => {
                // Store the token in localStorage
                localStorage.setItem('authToken', auth.token);
                localStorage.setItem('user', JSON.stringify(auth.user));
            });
    },
    
    // Called when the user clicks on the logout button
    logout: () => {
        // Make API call to logout endpoint to invalidate the token
        return fetch('http://127.0.0.1:5000/auth/logout', {
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }),
        })
            .then(() => {
                localStorage.removeItem('authToken');
                localStorage.removeItem('user');
                return Promise.resolve();
            })
            .catch(() => {
                // Even if the API call fails, clear local storage
                localStorage.removeItem('authToken');
                localStorage.removeItem('user');
                return Promise.resolve();
            });
    },
    
    // Called when the API returns an error
    checkError: ({ status }) => {
        if (status === 401 || status === 403) {
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
            return Promise.reject();
        }
        return Promise.resolve();
    },
    
    // Called when the user navigates to a new location, to check for authentication
    checkAuth: () => {
        const token = localStorage.getItem('authToken');
        if (!token) {
            return Promise.reject();
        }
        
        // Optional: Verify token on server
        return fetch('http://127.0.0.1:5000/auth/verify-token', {
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }),
        })
            .then(response => {
                if (response.status < 200 || response.status >= 300) {
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('user');
                    return Promise.reject();
                }
                return Promise.resolve();
            })
            .catch(() => {
                localStorage.removeItem('authToken');
                localStorage.removeItem('user');
                return Promise.reject();
            });
    },
    
    // Called when the user navigates to a new location, to check for permissions / roles
    getPermissions: () => {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        return user.role ? Promise.resolve(user.role) : Promise.resolve('user');
    },
    
    // Get the current user's identity from localStorage
    getIdentity: () => {
        try {
            const user = JSON.parse(localStorage.getItem('user') || '{}');
            return Promise.resolve({
                id: user.id,
                fullName: user.name,
                avatar: user.avatar,
            });
        } catch (error) {
            return Promise.reject(error);
        }
    },
};

export default authProvider;