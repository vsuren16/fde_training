import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { isLoggedIn, user } = useContext(UserContext);

  // Not logged in → login
  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }

  // Role-based restriction
  if (allowedRoles && allowedRoles.length > 0) {
    const role = user?.role;
    if (!allowedRoles.includes(role)) {
      return <Navigate to="/access-denied" replace />;
    }
  }

  return children;
};

export default ProtectedRoute;
