// Import axios library for making HTTP requests (GET, POST, PUT, DELETE, etc.)
import axios from "axios";

// Create a reusable axios instance
// baseURL is the common backend URL for all API calls
const api = axios.create({
  baseURL: "http://127.0.0.1:8060",
});

// Add a request interceptor
// This runs automatically BEFORE every API request is sent
api.interceptors.request.use(
  (config) => {
    // Get the JWT token stored in browser localStorage after login
    const token = localStorage.getItem("token");

    // If token exists, attach it to the request headers
    // "Authorization" header is required for protected backend APIs
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Return the modified config so the request can continue
    return config;
  },
  (error) => {
    // Handle any request errors before the request is sent
    return Promise.reject(error);
  }
);

// Export the configured axios instance
// This will be imported and used in services/components
export default api;