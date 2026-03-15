import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import ProjectAssignment from "../../components/ProjectAssignment";

const EmployeeDetails = ({ employees, departments, projects, onAssignProject }) => {
  const { id } = useParams();
  const navigate = useNavigate();

  const empId = Number(id);
  const employee = employees.find((e) => e.id === empId);

  if (!employee) {
    return (
      <div className="alert alert-danger">
        Employee not found.{" "}
        <button className="btn btn-link p-0" onClick={() => navigate("/employees")}>
          Go back
        </button>
      </div>
    );
  }

  const dept = departments.find((d) => d.id === employee.deptId);
  const assignedProjects = projects.filter((p) => employee.projectIds.includes(p.id));

  const handleAssign = (projectId) => {
    onAssignProject(employee.id, projectId);
  };

  return (
    <div>
      <button className="btn btn-outline-secondary mb-3" onClick={() => navigate("/employees")}>
        ← Back
      </button>

      <h2 className="mb-3">Employee Details</h2>

      <div className="card shadow-sm">
        <div className="card-body">
          <p className="mb-2">
            <strong>Name:</strong> {employee.name}
          </p>
          <p className="mb-2">
            <strong>Department:</strong> {dept ? dept.name : "N/A"}
          </p>

          <div className="mt-3">
            <strong>Assigned Projects:</strong>
            {assignedProjects.length === 0 ? (
              <div className="text-muted mt-1">No projects assigned.</div>
            ) : (
              <ul className="mt-2 mb-0">
                {assignedProjects.map((p) => (
                  <li key={p.id}>
                    {p.name} {p.isActive ? "(Active)" : "(Inactive)"}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>

      {/* Child component */}
      <ProjectAssignment projects={projects} onAssign={handleAssign} />
    </div>
  );
};

export default EmployeeDetails;
