import React, { useState } from "react";

const AppointmentHistory = ({ patientId, appointments, onAddAppointment }) => {
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [reason, setReason] = useState("");
  const [error, setError] = useState("");

  const handleAdd = (e) => {
    e.preventDefault();
    setError("");

    if (!date || !time || !reason.trim()) {
      setError("Date, time, and reason are required.");
      return;
    }

    const newAppt = {
      id: Date.now(), // demo unique id
      patientId,
      date,
      time,
      reason: reason.trim(),
    };

    onAddAppointment(newAppt); // ✅ send update to parent

    // reset form
    setDate("");
    setTime("");
    setReason("");
  };

  return (
    <div className="card shadow-sm h-100">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-center mb-2">
          <h5 className="card-title mb-0">Appointment History</h5>
          <span className="badge bg-secondary">{appointments.length}</span>
        </div>

        {error && <div className="alert alert-danger py-2">{error}</div>}

        {/* Add Appointment */}
        <form onSubmit={handleAdd} className="row g-2 mb-3">
          <div className="col-md-4">
            <input
              type="date"
              className="form-control"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>
          <div className="col-md-3">
            <input
              type="time"
              className="form-control"
              value={time}
              onChange={(e) => setTime(e.target.value)}
            />
          </div>
          <div className="col-md-5">
            <input
              type="text"
              className="form-control"
              placeholder="Reason"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            />
          </div>
          <div className="col-12">
            <button className="btn btn-outline-primary w-100" type="submit">
              Add Appointment
            </button>
          </div>
        </form>

        {/* Appointments Table */}
        <div className="table-responsive">
          <table className="table table-sm table-hover align-middle mb-0">
            <thead className="table-light">
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody>
              {appointments.length === 0 ? (
                <tr>
                  <td colSpan="3" className="text-center py-3 text-muted">
                    No appointments yet.
                  </td>
                </tr>
              ) : (
                appointments
                  .slice()
                  .sort((a, b) => (a.date < b.date ? 1 : -1))
                  .map((a) => (
                    <tr key={a.id}>
                      <td>{a.date}</td>
                      <td>{a.time}</td>
                      <td>{a.reason}</td>
                    </tr>
                  ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AppointmentHistory;
