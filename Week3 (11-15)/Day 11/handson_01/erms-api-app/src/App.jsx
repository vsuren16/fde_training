import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";

import Header from "./components/Header";
import Footer from "./components/Footer";
import ProtectedRoute from "./components/ProtectedRoute";
import "./App.css";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import AccessDenied from "./pages/AccessDenied";

import EmployeeList from "./pages/employees/EmployeeList";
import EmployeeDetails from "./pages/employees/EmployeeDetails";

import Departments from "./pages/Departments";
import Projects from "./pages/Projects";
import Profile from "./pages/Profile";

import {
  employees as employeesData,
  departments as departmentsData,
  projects as projectsData,
} from "./data/mockdata";

function App() {
  // App-level shared state (mock)
  const [employees, setEmployees] = useState(employeesData);
  const [departments] = useState(departmentsData);
  const [projects] = useState(projectsData);

  const handleDeleteEmployee = (employeeId) => {
    setEmployees((prev) => prev.filter((e) => e.id !== employeeId));
  };

  const handleAssignProject = (employeeId, projectId) => {
    setEmployees((prev) =>
      prev.map((e) => {
        if (e.id !== employeeId) return e;
        if (e.projectIds.includes(projectId)) return e;
        return { ...e, projectIds: [...e.projectIds, projectId] };
      })
    );
  };

  return (
    <BrowserRouter>
      <div className="d-flex flex-column min-vh-100">
        <Header />

        <div className="container my-4 flex-grow-1">
          <Routes>
            {/* Default */}
            <Route path="/" element={<Navigate to="/login" replace />} />

            {/* Public */}
            <Route path="/login" element={<Login />} />

            {/* Access denied */}
            <Route
              path="/access-denied"
              element={
                <ProtectedRoute>
                  <AccessDenied />
                </ProtectedRoute>
              }
            />

            {/* Dashboard: Admin, Manager, Employee */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute allowedRoles={["Admin", "Manager", "Employee"]}>
                  <Dashboard employees={employees} departments={departments} projects={projects} />
                </ProtectedRoute>
              }
            />

            {/* Employees: Admin, Manager */}
            <Route
              path="/employees"
              element={
                <ProtectedRoute allowedRoles={["Admin", "Manager"]}>
                  <EmployeeList employees={employees} onDelete={handleDeleteEmployee} />
                </ProtectedRoute>
              }
            />

            {/* Employee details: Admin, Manager */}
            <Route
              path="/employees/:id"
              element={
                <ProtectedRoute allowedRoles={["Admin", "Manager"]}>
                  <EmployeeDetails
                    employees={employees}
                    departments={departments}
                    projects={projects}
                    onAssignProject={handleAssignProject}
                  />
                </ProtectedRoute>
              }
            />

            {/* Departments: Admin, Manager */}
            <Route
              path="/departments"
              element={
                <ProtectedRoute allowedRoles={["Admin", "Manager"]}>
                  <Departments departments={departments} employees={employees} />
                </ProtectedRoute>
              }
            />

            {/* Projects: Admin, Manager */}
            <Route
              path="/projects"
              element={
                <ProtectedRoute allowedRoles={["Admin", "Manager"]}>
                  <Projects projects={projects} employees={employees} />
                </ProtectedRoute>
              }
            />

            {/* Profile: Admin, Manager, Employee */}
            <Route
              path="/profile"
              element={
                <ProtectedRoute allowedRoles={["Admin", "Manager", "Employee"]}>
                  <Profile />
                </ProtectedRoute>
              }
            />

            {/* NotFound */}
            <Route path="*" element={<h2>404 - Page Not Found</h2>} />
          </Routes>
        </div>

        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
