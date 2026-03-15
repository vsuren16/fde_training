import React, { useEffect, useMemo, useState } from "react";

// Demo data (replace with API later)
const seedPatients = [
  { id: 1, name: "Asha" },
  { id: 2, name: "Rahul" },
  { id: 3, name: "Meera" },
];

const seedDoctors = [
  { id: 1, name: "Dr. Kumar", specialty: "General", active: true },
  { id: 2, name: "Dr. Joseph", specialty: "Cardiology", active: true },
  { id: 3, name: "Dr. Priya", specialty: "Dermatology", active: false },
];

const seedAppointments = [
  { id: 201, patientId: 1, doctorId: 1, date: "2026-02-16", time: "10:30", reason: "Fever" },
  { id: 202, patientId: 2, doctorId: 2, date: "2026-02-16", time: "14:00", reason: "Checkup" },
  { id: 203, patientId: 3, doctorId: 1, date: "2026-02-17", time: "09:15", reason: "Skin rash" },
];

const AppointmentList = () => {
  const [patients, setPatients] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);

  // Create form state
  const [patientId, setPatientId] = useState("");
  const [doctorId, setDoctorId] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [reason, setReason] = useState("");
  const [error, setError] = useState("");

  // Filters
  const [filterDate, setFilterDate] = useState("");
  const [filterDoctorId, setFilterDoctorId] = useState("");

  useEffect(() => {
    setPatients(seedPatients);
    setDoctors(seedDoctors);
    setAppointments(seedAppointments);
  }, []);

  const patientNameById = useMemo(() => {
    const map = new Map(patients.map((p) => [p.id, p.name]));
    return (id) => map.get(id) || "Unknown";
  }, [patients]);

  const doctorNameById = useMemo(() => {
    const map = new Map(doctors.map((d) => [d.id, d.name]));
    return (id) => map.get(id) || "Unknown";
  }, [doctors]);

  const handleCreate = (e) => {
    e.preventDefault();
    setError("");

    if (!patientId || !doctorId || !date || !time || !reason.trim()) {
      setError("All fields are required.");
      return;
    }

    const selectedDoctor = doctors.find((d) => d.id === Number(doctorId));
    if (selectedDoctor && !selectedDoctor.active) {
      setError("Selected doctor is inactive. Please choose an active doctor.");
      return;
    }

    const newAppt = {
      id: Date.now(),
      patientId: Number(patientId),
      doctorId: Number(doctorId),
      date,
      time,
      reason: reason.trim(),
    };

    setAppointments((prev) => [newAppt, ...prev]);

    // Reset form
    setPatientId("");
    setDoctorId("");
    setDate("");
    setTime("");
    setReason("");
  };

  const filteredAppointments = useMemo(() => {
    return appointments.filter((a) => {
      const matchesDate = filterDate ? a.date === filterDate : true;
      const matchesDoctor = filterDoctorId ? a.doctorId === Number(filterDoctorId) : true;
      return matchesDate && matchesDoctor;
    });
  }, [appointments, filterDate, filterDoctorId]);

  const clearFilters = () => {
    setFilterDate("");
    setFilterDoctorId("");
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h3 className="mb-0">Appointments</h3>
        <span className="badge bg-primary">{filteredAppointments.length} Shown</span>
      </div>

      <div className="row g-3">
        {/* Create Appointment */}
        <div className="col-lg-4">
          <div className="card shadow-sm">
            <div className="card-body">
              <h5 className="card-title">Create Appointment</h5>
              <p className="text-muted small mb-3">
                Add a new appointment and assign a doctor.
              </p>

              {error && <div className="alert alert-danger py-2">{error}</div>}

              <form onSubmit={handleCreate}>
                <div className="mb-2">
                  <label className="form-label">Patient</label>
                  <select
                    className="form-select"
                    value={patientId}
                    onChange={(e) => setPatientId(e.target.value)}
                  >
                    <option value="">-- Select Patient --</option>
                    {patients.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="mb-2">
                  <label className="form-label">Doctor</label>
                  <select
                    className="form-select"
                    value={doctorId}
                    onChange={(e) => setDoctorId(e.target.value)}
                  >
                    <option value="">-- Select Doctor --</option>
                    {doctors.map((d) => (
                      <option key={d.id} value={d.id} disabled={!d.active}>
                        {d.name} — {d.specialty} {!d.active ? "(Inactive)" : ""}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="row g-2 mb-2">
                  <div className="col-6">
                    <label className="form-label">Date</label>
                    <input
                      type="date"
                      className="form-control"
                      value={date}
                      onChange={(e) => setDate(e.target.value)}
                    />
                  </div>
                  <div className="col-6">
                    <label className="form-label">Time</label>
                    <input
                      type="time"
                      className="form-control"
                      value={time}
                      onChange={(e) => setTime(e.target.value)}
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label className="form-label">Reason</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="e.g., Follow-up"
                    value={reason}
                    onChange={(e) => setReason(e.target.value)}
                  />
                </div>

                <button className="btn btn-primary w-100" type="submit">
                  Add Appointment
                </button>
              </form>
            </div>
          </div>
        </div>

        {/* Filters + Table */}
        <div className="col-lg-8">
          <div className="card shadow-sm mb-3">
            <div className="card-body">
              <h5 className="card-title">Filters</h5>

              <div className="row g-2 align-items-end">
                <div className="col-md-5">
                  <label className="form-label">Filter by Date</label>
                  <input
                    type="date"
                    className="form-control"
                    value={filterDate}
                    onChange={(e) => setFilterDate(e.target.value)}
                  />
                </div>

                <div className="col-md-5">
                  <label className="form-label">Filter by Doctor</label>
                  <select
                    className="form-select"
                    value={filterDoctorId}
                    onChange={(e) => setFilterDoctorId(e.target.value)}
                  >
                    <option value="">All Doctors</option>
                    {doctors.map((d) => (
                      <option key={d.id} value={d.id}>
                        {d.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="col-md-2 d-grid">
                  <button className="btn btn-outline-secondary" onClick={clearFilters}>
                    Clear
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="card shadow-sm">
            <div className="card-body">
              <h5 className="card-title">Appointment List</h5>

              <div className="table-responsive">
                <table className="table table-hover align-middle mb-0">
                  <thead className="table-light">
                    <tr>
                      <th>Date</th>
                      <th>Time</th>
                      <th>Patient</th>
                      <th>Doctor</th>
                      <th>Reason</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredAppointments.length === 0 ? (
                      <tr>
                        <td colSpan="5" className="text-center py-4 text-muted">
                          No appointments match the filter.
                        </td>
                      </tr>
                    ) : (
                      filteredAppointments
                        .slice()
                        .sort((a, b) => (a.date < b.date ? 1 : -1))
                        .map((a) => (
                          <tr key={a.id}>
                            <td>{a.date}</td>
                            <td>{a.time}</td>
                            <td className="fw-semibold">{patientNameById(a.patientId)}</td>
                            <td>{doctorNameById(a.doctorId)}</td>
                            <td>{a.reason}</td>
                          </tr>
                        ))
                    )}
                  </tbody>
                </table>
              </div>

              <div className="mt-3 text-muted">
                <small>
                  Tip: Use filters to quickly view appointments by date or doctor.
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AppointmentList;
