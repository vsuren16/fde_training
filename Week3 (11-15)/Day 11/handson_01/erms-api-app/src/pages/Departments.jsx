import React, { useState } from "react";

const Departments = ({ departments, employees }) => {
  const [selectedDeptId, setSelectedDeptId] = useState(null);

  const selectedDept = departments.find((d) => d.id === selectedDeptId);
  const deptEmployees = selectedDeptId
    ? employees.filter((e) => e.deptId === selectedDeptId)
    : [];

  return (
    <div>
      <h2 className="mb-4">Departments</h2>

      <div className="row g-3">
        {/* Department List */}
        <div className="col-12 col-md-4">
          <div className="card shadow-sm">
            <div className="card-body">
              <h5 className="card-title mb-3">Department List</h5>

              <div className="list-group">
                {departments.map((dept) => (
                  <button
                    key={dept.id}
                    type="button"
                    className={`list-group-item list-group-item-action ${
                      selectedDeptId === dept.id ? "active" : ""
                    }`}
                    onClick={() => setSelectedDeptId(dept.id)}
                  >
                    {dept.name}
                  </button>
                ))}
              </div>

              {selectedDeptId && (
                <button
                  className="btn btn-outline-secondary btn-sm mt-3"
                  onClick={() => setSelectedDeptId(null)}
                >
                  Clear Selection
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Employees for Selected Department */}
        <div className="col-12 col-md-8">
          <div className="card shadow-sm">
            <div className="card-body">
              <h5 className="card-title mb-3">
                {selectedDept ? `Employees in ${selectedDept.name}` : "Select a Department"}
              </h5>

              {!selectedDept ? (
                <div className="text-muted">Click a department to view its employees.</div>
              ) : deptEmployees.length === 0 ? (
                <div className="alert alert-warning mb-0">No employees in this department.</div>
              ) : (
                <table className="table table-striped table-bordered align-middle mb-0">
                  <thead className="table-dark">
                    <tr>
                      <th style={{ width: "90px" }}>ID</th>
                      <th>Name</th>
                    </tr>
                  </thead>
                  <tbody>
                    {deptEmployees.map((emp) => (
                      <tr key={emp.id}>
                        <td>{emp.id}</td>
                        <td>{emp.name}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Departments;
