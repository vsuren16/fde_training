// Import Navigate for redirection and Outlet for rendering child routes
import { Navigate, Outlet } from "react-router-dom";

// Component to protect routes that require authentication
function ProtectedRoute() {
  // Read JWT token from localStorage
  // If token exists, user is considered authenticated
  const token = localStorage.getItem("token");

  // If token is present:
  // ➜ render the requested protected route using <Outlet />
  // If token is NOT present:
  // ➜ redirect user to login page
  return token ? <Outlet /> : <Navigate to="/login" />;
}

// Export ProtectedRoute for use in routing configuration
export default ProtectedRoute;