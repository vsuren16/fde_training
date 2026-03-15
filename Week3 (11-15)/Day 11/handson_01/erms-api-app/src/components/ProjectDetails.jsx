import React from "react";

const ProjectDetails = ({ project, assignedEmployees }) => {
  if (!project) {
    return (
      <div className="text-muted">
        Click a project to view details.
      </div>
    );
  }

  return (
    <div className="card shadow-sm">
      <div className="card-body">
        <h5 className="card-title mb-3">Project Details</h5>

        <p className="mb-2">
          <strong>Project:</strong> {project.name}
        </p>

        <p className="mb-3">
          <strong>Status:</strong> {project.isActive ? "Active" : "Inactive"}
        </p>

        <div>
          <strong>Assigned Employees:</strong>
          {assignedEmployees.length === 0 ? (
            <div className="text-muted mt-1">No employees assigned.</div>
          ) : (
            <ul className="mt-2 mb-0">
              {assignedEmployees.map((emp) => (
                <li key={emp.id}>
                  {emp.name} (ID: {emp.id})
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProjectDetails;
