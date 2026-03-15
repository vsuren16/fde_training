import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import PatientList from "../pages/PatientList";
import PatientDetails from "../pages/PatientDetails";
import DoctorList from "../pages/DoctorList";
import AppointmentList from "../pages/AppointmentList";
import MedicalRecords from "../pages/MedicalRecords";
import UserProfile from "../pages/UserProfile";

import Layout from "../components/Layout";
import ProtectedRoute from "./ProtectedRoute";
import RoleProtectedRoute from "./RoleProtectedRoute";
import { ROLE } from "../utils/rbac";

const AppRoutes = () => {
  return (
    <Routes>
      {/* ✅ Default route */}
      <Route path="/" element={<Navigate to="/login" replace />} />

      {/* ✅ Public */}
      <Route path="/login" element={<Login />} />

      {/* ✅ Protected */}
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          {/* Common (All logged-in roles) */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<UserProfile />} />

          {/* Admin + Doctor: Patients */}
          <Route
            element={
              <RoleProtectedRoute allowedRoles={[ROLE.ADMIN, ROLE.DOCTOR]} />
            }
          >
            <Route path="/patients" element={<PatientList />} />
            <Route path="/patients/:id" element={<PatientDetails />} />
          </Route>

          {/* Admin only: Doctors */}
          <Route element={<RoleProtectedRoute allowedRoles={[ROLE.ADMIN]} />}>
            <Route path="/doctors" element={<DoctorList />} />
          </Route>

          {/* Admin + Receptionist: Appointments */}
          <Route
            element={
              <RoleProtectedRoute
                allowedRoles={[ROLE.ADMIN, ROLE.RECEPTIONIST]}
              />
            }
          >
            <Route path="/appointments" element={<AppointmentList />} />
          </Route>

          {/* Admin + Doctor: Records */}
          <Route
            element={
              <RoleProtectedRoute allowedRoles={[ROLE.ADMIN, ROLE.DOCTOR]} />
            }
          >
            <Route path="/records/:patientId" element={<MedicalRecords />} />
          </Route>
        </Route>
      </Route>

      {/* ✅ Single fallback (ONLY ONE!) */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
};

export default AppRoutes;
