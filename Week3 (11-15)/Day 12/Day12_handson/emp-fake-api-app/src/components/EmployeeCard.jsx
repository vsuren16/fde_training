import React from "react";

const EmployeeCard = ({ employee }) => {
  return (
    <div className="card h-100 shadow-sm">
      <div className="card-body d-flex flex-column">
        <h5 className="card-title">{employee.name}</h5>

        <p className="mb-2">
          <strong>Email:</strong> {employee.email}
        </p>
        <p className="mb-2">
          <strong>Phone:</strong> {employee.phone}
        </p>
        <p className="mb-0">
          <strong>Company:</strong> {employee.companyName}
        </p>

        <button className="btn btn-primary mt-auto mt-3">
          View Profile
        </button>
      </div>
    </div>
  );
};

export default EmployeeCard;
