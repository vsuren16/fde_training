import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Login = () => {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [role, setRole] = useState("Receptionist");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    const trimmed = username.trim();
    if (!trimmed) {
      setError("Username is required.");
      return;
    }

    // Store user info in Context
    login({
      name: trimmed,
      role,
    });

    // Redirect to dashboard after login
    navigate("/dashboard");
  };

  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: "75vh" }}>
      <div className="card shadow" style={{ maxWidth: 420, width: "100%" }}>
        <div className="card-body p-4">
          <h3 className="card-title mb-3 text-center">Login</h3>
          <p className="text-muted text-center mb-4">
            Smart Healthcare Appointment & Records Portal
          </p>

          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {/* Username */}
            <div className="mb-3">
              <label className="form-label">Username</label>
              <input
                type="text"
                className="form-control"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            {/* Role */}
            <div className="mb-4">
              <label className="form-label">Role</label>
              <select
                className="form-select"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                <option value="Admin">Admin</option>
                <option value="Doctor">Doctor</option>
                <option value="Receptionist">Receptionist</option>
              </select>
            </div>

            <button type="submit" className="btn btn-primary w-100">
              Sign In
            </button>
          </form>

          {/* Optional helper text */}
          <div className="mt-3 text-center">
            <small className="text-muted">
              Demo login: pick any username and role.
            </small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
