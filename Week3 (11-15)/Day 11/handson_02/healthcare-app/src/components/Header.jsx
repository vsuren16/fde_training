import React, { useContext } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Header = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary shadow">
      <div className="container">
        <span className="navbar-brand fw-bold">
          🏥 Smart Healthcare Portal
        </span>

        {user && (
          <>
            <ul className="navbar-nav me-auto">
              <li className="nav-item">
                <NavLink className="nav-link" to="/dashboard">Dashboard</NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/patients">Patients</NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/appointments">Appointments</NavLink>
              </li>
            </ul>

            <div className="text-white">
              <span className="me-3">
                {user.name} ({user.role})
              </span>
              <button
                className="btn btn-sm btn-light"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          </>
        )}
      </div>
    </nav>
  );
};

export default Header;
