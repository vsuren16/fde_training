import React, { useEffect, useState } from "react";

const AssignedDoctor = ({ patient, doctors, onDoctorUpdate }) => {
  const [selectedDoctorId, setSelectedDoctorId] = useState(patient.assignedDoctorId || "");

  useEffect(() => {
    setSelectedDoctorId(patient.assignedDoctorId || "");
  }, [patient.assignedDoctorId]);

  const handleSave = () => {
    if (!selectedDoctorId) return;
    onDoctorUpdate(Number(selectedDoctorId)); // ✅ send update to parent
  };

  return (
    <div className="card shadow-sm h-100">
      <div className="card-body">
        <h5 className="card-title">Assigned Doctor</h5>
        <p className="text-muted small mb-3">
          Update the patient’s assigned doctor.
        </p>

        <label className="form-label">Select Doctor</label>
        <select
          className="form-select mb-3"
          value={selectedDoctorId}
          onChange={(e) => setSelectedDoctorId(e.target.value)}
        >
          <option value="">-- Choose --</option>
          {doctors.map((d) => (
            <option key={d.id} value={d.id} disabled={!d.active}>
              {d.name} — {d.specialty} {!d.active ? "(Inactive)" : ""}
            </option>
          ))}
        </select>

        <button className="btn btn-primary w-100" onClick={handleSave} disabled={!selectedDoctorId}>
          Save Doctor
        </button>
      </div>
    </div>
  );
};

export default AssignedDoctor;
