import React, { useEffect, useState } from "react";

const DoctorList = () => {
  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
    // Demo data
    setDoctors([
      { id: 1, name: "Dr. Kumar", specialty: "General Medicine", active: true },
      { id: 2, name: "Dr. Joseph", specialty: "Cardiology", active: true },
      { id: 3, name: "Dr. Priya", specialty: "Dermatology", active: false },
    ]);
  }, []);

  return (
    <div>
      <h3 className="mb-3">Doctors</h3>

      <div className="card shadow-sm">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover align-middle mb-0">
              <thead className="table-light">
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Specialty</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {doctors.length === 0 ? (
                  <tr>
                    <td colSpan="4" className="text-center py-4 text-muted">
                      No doctors available.
                    </td>
                  </tr>
                ) : (
                  doctors.map((doctor) => (
                    <tr key={doctor.id}>
                      <td>{doctor.id}</td>
                      <td className="fw-semibold">{doctor.name}</td>
                      <td>{doctor.specialty}</td>
                      <td>
                        <span
                          className={`badge ${
                            doctor.active ? "bg-success" : "bg-secondary"
                          }`}
                        >
                          {doctor.active ? "Active" : "Inactive"}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DoctorList;
