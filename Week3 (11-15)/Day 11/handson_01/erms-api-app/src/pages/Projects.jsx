import React, { useMemo, useState } from "react";
import ProjectDetails from "../components/ProjectDetails";

const Projects = ({ projects, employees }) => {
  const [selectedProjectId, setSelectedProjectId] = useState(null);

  const selectedProject = projects.find((p) => p.id === selectedProjectId) || null;

  const getAssignedEmployees = (projectId) =>
    employees.filter((e) => e.projectIds.includes(projectId));

  const assignedEmployeesForSelected = selectedProject
    ? getAssignedEmployees(selectedProject.id)
    : [];

  // Precompute counts (nice + clean)
  const projectRows = useMemo(() => {
    return projects.map((p) => {
      const count = employees.filter((e) => e.projectIds.includes(p.id)).length;
      return { ...p, assignedCount: count };
    });
  }, [projects, employees]);

  return (
    <div>
      <h2 className="mb-4">Projects</h2>

      <div className="row g-3">
        {/* Project List */}
        <div className="col-12 col-md-6">
          <div className="card shadow-sm">
            <div className="card-body">
              <h5 className="card-title mb-3">Project List</h5>

              <table className="table table-striped table-bordered align-middle mb-0">
                <thead className="table-dark">
                  <tr>
                    <th>Project Name</th>
                    <th style={{ width: "220px" }}>Assigned Employees</th>
                  </tr>
                </thead>
                <tbody>
                  {projectRows.length === 0 ? (
                    <tr>
                      <td colSpan="2" className="text-center py-4">
                        No projects found.
                      </td>
                    </tr>
                  ) : (
                    projectRows.map((p) => (
                      <tr
                        key={p.id}
                        role="button"
                        style={{ cursor: "pointer" }}
                        className={selectedProjectId === p.id ? "table-primary" : ""}
                        onClick={() => setSelectedProjectId(p.id)}
                      >
                        <td>
                          {p.name}{" "}
                          {p.isActive ? (
                            <span className="badge bg-success ms-2">Active</span>
                          ) : (
                            <span className="badge bg-secondary ms-2">Inactive</span>
                          )}
                        </td>
                        <td>{p.assignedCount}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>

              {selectedProjectId && (
                <button
                  className="btn btn-outline-secondary btn-sm mt-3"
                  onClick={() => setSelectedProjectId(null)}
                >
                  Clear Selection
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Child Component for Project Details */}
        <div className="col-12 col-md-6">
          <ProjectDetails
            project={selectedProject}
            assignedEmployees={assignedEmployeesForSelected}
          />
        </div>
      </div>
    </div>
  );
};

export default Projects;
