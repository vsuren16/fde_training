import React, { useContext } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const RoleProtectedRoute = ({ allowedRoles = [] }) => {
  const { user } = useContext(AuthContext);
  const location = useLocation();

  // not logged in
  if (!user) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // role not allowed
  if (!allowedRoles.includes(user.role)) {
    return (
      <div className="container">
        <div className="alert alert-danger mt-4">
          <h5 className="mb-1">Access Denied</h5>
          <p className="mb-0">
            This page is restricted to: {allowedRoles.join(", ")}.
          </p>
        </div>
      </div>
    );
  }

  return <Outlet />;
};

export default RoleProtectedRoute;
