/**
 * Robust API helper for Annesana
 * Handles 500 errors, non-JSON responses, and network failures.
 */
const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://127.0.0.1:8000/api'
    : '/api';

async function fetchAPI(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;

    // Set default headers if not provided
    const headers = {
        'Accept': 'application/json',
        ...(options.headers || {})
    };

    // Auto-inject JWT token if it exists
    const token = localStorage.getItem('token');
    if (token && !headers['Authorization']) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(url, { ...options, headers });

        // Handle non-JSON responses (like Vercel error pages)
        const contentType = response.headers.get('content-type');
        let data;

        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            // If it's not JSON, it's likely a 500 HTML page or 404
            const text = await response.text();
            console.error('Non-JSON response received:', text);
            throw new Error(`Server returned a non-JSON response (${response.status}). Please check backend logs.`);
        }

        if (!response.ok) {
            // Extract error message from JSON if possible
            const errorMsg = data.detail || data.error || data.message || `Request failed with status ${response.status}`;
            throw new Error(errorMsg);
        }

        return data;
    } catch (error) {
        if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
            throw new Error('Network error: Is the backend server running?');
        }
        throw error;
    }
}
