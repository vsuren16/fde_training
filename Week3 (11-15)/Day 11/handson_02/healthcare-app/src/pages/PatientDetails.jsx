import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import AppointmentHistory from "../components/AppointmentHistory";
import AssignedDoctor from "../components/AssignedDoctor";

// Demo data
const seedPatients = [
  { id: 1, name: "Asha", age: 29, gender: "Female", phone: "9876543210", assignedDoctorId: 1 },
  { id: 2, name: "Rahul", age: 41, gender: "Male", phone: "9123456780", assignedDoctorId: 2 },
  { id: 3, name: "Meera", age: 35, gender: "Female", phone: "9988776655", assignedDoctorId: 1 },
];

const seedDoctors = [
  { id: 1, name: "Dr. Kumar", specialty: "General", active: true },
  { id: 2, name: "Dr. Joseph", specialty: "Cardiology", active: true },
  { id: 3, name: "Dr. Priya", specialty: "Dermatology", active: false },
];

const seedAppointments = [
  { id: 101, patientId: 1, date: "2026-02-10", time: "10:30", reason: "Fever" },
  { id: 102, patientId: 1, date: "2026-02-16", time: "14:00", reason: "Follow-up" },
  { id: 103, patientId: 2, date: "2026-02-12", time: "09:15", reason: "Checkup" },
];

const PatientDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const patientId = Number(id);

  const [patient, setPatient] = useState(null);
  const [doctors, setDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    setDoctors(seedDoctors);

    const found = seedPatients.find((p) => p.id === patientId);
    setPatient(found || null);

    const patientAppts = seedAppointments.filter((a) => a.patientId === patientId);
    setAppointments(patientAppts);
  }, [patientId]);

  // ✅ Callback from AssignedDoctor (child -> parent)
  const handleDoctorUpdate = (newDoctorId) => {
    setPatient((prev) => {
      if (!prev) return prev;
      return { ...prev, assignedDoctorId: newDoctorId };
    });
  };

  // ✅ Callback from AppointmentHistory (child -> parent)
  const handleAddAppointment = (newAppt) => {
    setAppointments((prev) => [newAppt, ...prev]);
  };

  if (!patient) {
    return (
      <div className="alert alert-warning">
        Patient not found.
        <div className="mt-3">
          <button className="btn btn-outline-primary" onClick={() => navigate("/patients")}>
            Back to Patients
          </button>
        </div>
      </div>
    );
  }

  const assignedDoctor = doctors.find((d) => d.id === patient.assignedDoctorId);

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h3 className="mb-0">Patient Details</h3>
          <small className="text-muted">Patient ID: {patient.id}</small>
        </div>

        <button className="btn btn-outline-secondary" onClick={() => navigate("/patients")}>
          Back
        </button>
      </div>

      {/* Patient Info */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h5 className="card-title mb-3">{patient.name}</h5>

          <div className="row g-3">
            <div className="col-md-3">
              <div className="text-muted small">Age</div>
              <div className="fw-semibold">{patient.age}</div>
            </div>
            <div className="col-md-3">
              <div className="text-muted small">Gender</div>
              <div className="fw-semibold">{patient.gender}</div>
            </div>
            <div className="col-md-3">
              <div className="text-muted small">Phone</div>
              <div className="fw-semibold">{patient.phone}</div>
            </div>
            <div className="col-md-3">
              <div className="text-muted small">Assigned Doctor</div>
              <div className="fw-semibold">
                {assignedDoctor ? `${assignedDoctor.name} (${assignedDoctor.specialty})` : "Not assigned"}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Child Components */}
      <div className="row g-3">
        <div className="col-lg-5">
          <AssignedDoctor
            patient={patient}
            doctors={doctors}
            onDoctorUpdate={handleDoctorUpdate}   // ✅ child -> parent update
          />
        </div>

        <div className="col-lg-7">
          <AppointmentHistory
            patientId={patient.id}
            appointments={appointments}
            onAddAppointment={handleAddAppointment} // ✅ child -> parent update
          />
        </div>
      </div>
    </div>
  );
};

export default PatientDetails;
