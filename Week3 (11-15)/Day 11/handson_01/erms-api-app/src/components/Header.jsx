import React, { useContext } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";

const Header = () => {
  const { user, isLoggedIn, logout } = useContext(UserContext);
  const navigate = useNavigate();

  const role = user?.role;

  const canSeeEmployees = role === "Admin" || role === "Manager";
  const canSeeDepartments = role === "Admin" || role === "Manager";
  const canSeeProjects = role === "Admin" || role === "Manager";
  const canSeeDashboard = role === "Admin" || role === "Manager" || role === "Employee";
  const canSeeProfile = role === "Admin" || role === "Manager" || role === "Employee";

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <NavLink className="navbar-brand fw-bold" to={isLoggedIn ? "/dashboard" : "/login"}>
        ERMS
      </NavLink>

      <button
        className="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span className="navbar-toggler-icon"></span>
      </button>

      <div className="collapse navbar-collapse" id="navbarNav">
        {isLoggedIn && (
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            {canSeeDashboard && (
              <li className="nav-item">
                <NavLink className="nav-link" to="/dashboard">
                  Dashboard
                </NavLink>
              </li>
            )}

            {canSeeEmployees && (
              <li className="nav-item">
                <NavLink className="nav-link" to="/employees">
                  Employees
                </NavLink>
              </li>
            )}

            {canSeeDepartments && (
              <li className="nav-item">
                <NavLink className="nav-link" to="/departments">
                  Departments
                </NavLink>
              </li>
            )}

            {canSeeProjects && (
              <li className="nav-item">
                <NavLink className="nav-link" to="/projects">
                  Projects
                </NavLink>
              </li>
            )}

            {canSeeProfile && (
              <li className="nav-item">
                <NavLink className="nav-link" to="/profile">
                  Profile
                </NavLink>
              </li>
            )}
          </ul>
        )}

        <div className="d-flex align-items-center text-white">
          {isLoggedIn && user ? (
            <>
              <span className="me-3">
                {user.name} ({user.role})
              </span>
              <button className="btn btn-outline-light btn-sm" onClick={handleLogout}>
                Logout
              </button>
            </>
          ) : (
            <span className="me-3">Guest</span>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Header;
