import React, { useContext, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { DataContext } from "../context/DataContext";
import { AuthContext } from "../context/AuthContext";

const MedicalRecords = () => {
  const { patientId } = useParams();
  const navigate = useNavigate();

  const pid = Number(patientId);

  const { patients, records, addRecord } = useContext(DataContext);
  const { user } = useContext(AuthContext);

  const patient = useMemo(() => patients.find((p) => p.id === pid), [patients, pid]);

  const patientRecords = useMemo(
    () => records.filter((r) => r.patientId === pid).sort((a, b) => (a.date < b.date ? 1 : -1)),
    [records, pid]
  );

  // Add record form (Doctor/Admin)
  const [date, setDate] = useState("");
  const [diagnosis, setDiagnosis] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState("");

  const handleAdd = (e) => {
    e.preventDefault();
    setError("");

    if (!date || !diagnosis.trim() || !notes.trim()) {
      setError("Date, diagnosis, and notes are required.");
      return;
    }

    addRecord({
      id: Date.now(),
      patientId: pid,
      date,
      diagnosis: diagnosis.trim(),
      notes: notes.trim(),
      doctor: user?.role === "Doctor" ? user.name : "Admin",
    });

    setDate("");
    setDiagnosis("");
    setNotes("");
  };

  if (!patient) {
    return (
      <div className="container">
        <div className="alert alert-warning mt-4">
          Patient not found.
          <div className="mt-3">
            <button className="btn btn-outline-primary" onClick={() => navigate("/patients")}>
              Back to Patients
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h3 className="mb-0">Medical Records</h3>
          <small className="text-muted">
            Patient: <span className="fw-semibold">{patient.name}</span> (ID: {patient.id})
          </small>
        </div>

        <button className="btn btn-outline-secondary" onClick={() => navigate(`/patients/${patient.id}`)}>
          Back to Details
        </button>
      </div>

      <div className="row g-3">
        {/* Add Record */}
        <div className="col-lg-4">
          <div className="card shadow-sm">
            <div className="card-body">
              <h5 className="card-title">Add Record</h5>
              <p className="text-muted small mb-3">
                Only Admin and Doctor can add/view medical records.
              </p>

              {error && <div className="alert alert-danger py-2">{error}</div>}

              <form onSubmit={handleAdd}>
                <div className="mb-2">
                  <label className="form-label">Date</label>
                  <input
                    type="date"
                    className="form-control"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                  />
                </div>

                <div className="mb-2">
                  <label className="form-label">Diagnosis</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="e.g., Viral Fever"
                    value={diagnosis}
                    onChange={(e) => setDiagnosis(e.target.value)}
                  />
                </div>

                <div className="mb-3">
                  <label className="form-label">Notes</label>
                  <textarea
                    className="form-control"
                    rows="3"
                    placeholder="Treatment / observations"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                  />
                </div>

                <button className="btn btn-primary w-100" type="submit">
                  Save Record
                </button>
              </form>
            </div>
          </div>
        </div>

        {/* Records Table */}
        <div className="col-lg-8">
          <div className="card shadow-sm">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <h5 className="card-title mb-0">Records List</h5>
                <span className="badge bg-secondary">{patientRecords.length}</span>
              </div>

              <div className="table-responsive">
                <table className="table table-hover align-middle mb-0">
                  <thead className="table-light">
                    <tr>
                      <th>Date</th>
                      <th>Diagnosis</th>
                      <th>Notes</th>
                      <th>Doctor</th>
                    </tr>
                  </thead>
                  <tbody>
                    {patientRecords.length === 0 ? (
                      <tr>
                        <td colSpan="4" className="text-center py-4 text-muted">
                          No medical records found for this patient.
                        </td>
                      </tr>
                    ) : (
                      patientRecords.map((r) => (
                        <tr key={r.id}>
                          <td>{r.date}</td>
                          <td className="fw-semibold">{r.diagnosis}</td>
                          <td>{r.notes}</td>
                          <td>{r.doctor}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>

              <div className="mt-3 text-muted">
                <small>Uses route param <code>:patientId</code> and shared context for data.</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MedicalRecords;
