import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// Demo data (replace with API later)
const seedPatients = [
  { id: 1, name: "Asha", age: 29, gender: "Female", phone: "9876543210" },
  { id: 2, name: "Rahul", age: 41, gender: "Male", phone: "9123456780" },
  { id: 3, name: "Meera", age: 35, gender: "Female", phone: "9988776655" },
];

const PatientList = () => {
  const navigate = useNavigate();
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    // Simulate data fetch
    setPatients(seedPatients);
  }, []);

  const goToDetails = (id) => {
    navigate(`/patients/${id}`);
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h3 className="mb-0">Patients</h3>
        <span className="badge bg-primary">{patients.length} Total</span>
      </div>

      <div className="card shadow-sm">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover align-middle mb-0">
              <thead className="table-light">
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Age</th>
                  <th>Gender</th>
                  <th>Phone</th>
                  <th className="text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                {patients.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="text-center py-4 text-muted">
                      No patients found.
                    </td>
                  </tr>
                ) : (
                  patients.map((p) => (
                    <tr
                      key={p.id}
                      role="button"
                      onClick={() => goToDetails(p.id)}
                      style={{ cursor: "pointer" }}
                    >
                      <td>{p.id}</td>
                      <td className="fw-semibold">{p.name}</td>
                      <td>{p.age}</td>
                      <td>{p.gender}</td>
                      <td>{p.phone}</td>
                      <td className="text-end" onClick={(e) => e.stopPropagation()}>
                        <button
                          className="btn btn-sm btn-outline-primary"
                          onClick={() => goToDetails(p.id)}
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          <div className="mt-3 text-muted">
            <small>Tip: Click anywhere on a row to open patient details.</small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientList;
