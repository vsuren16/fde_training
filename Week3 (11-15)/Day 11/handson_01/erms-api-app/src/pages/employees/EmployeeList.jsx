import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../../context/UserContext";

const EmployeeList = ({ employees, onDelete }) => {
  const navigate = useNavigate();
  const { user } = useContext(UserContext);

  const isAdmin = user?.role === "Admin";

  return (
    <div>
      <h2 className="mb-4">Employees</h2>

      <table className="table table-striped table-bordered align-middle">
        <thead className="table-dark">
          <tr>
            <th style={{ width: "80px" }}>ID</th>
            <th>Name</th>
            <th style={{ width: "220px" }}>Actions</th>
          </tr>
        </thead>

        <tbody>
          {employees.length === 0 ? (
            <tr>
              <td colSpan="3" className="text-center py-4">
                No employees found.
              </td>
            </tr>
          ) : (
            employees.map((emp) => (
              <tr key={emp.id}>
                <td>{emp.id}</td>
                <td>{emp.name}</td>
                <td>
                  <button
                    className="btn btn-sm btn-primary me-2"
                    onClick={() => navigate(`/employees/${emp.id}`)}
                  >
                    View
                  </button>

                  {isAdmin && (
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => onDelete(emp.id)}
                    >
                      Delete
                    </button>
                  )}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      {!isAdmin && (
        <div className="alert alert-secondary py-2">
          Delete is available for Admin only.
        </div>
      )}
    </div>
  );
};

export default EmployeeList;
