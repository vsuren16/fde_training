import React from "react";
import { useNavigate } from "react-router-dom";

const AccessDenied = () => {
  const navigate = useNavigate();

  return (
    <div className="text-center">
      <h2 className="mb-3 text-danger">Access Denied</h2>
      <p className="text-muted mb-4">
        You do not have permission to access this page.
      </p>

      <button
        className="btn btn-primary me-2"
        onClick={() => navigate("/dashboard")}
      >
        Go to Dashboard
      </button>

      <button
        className="btn btn-outline-secondary"
        onClick={() => navigate("/profile")}
      >
        Go to Profile
      </button>
    </div>
  );
};

export default AccessDenied;
