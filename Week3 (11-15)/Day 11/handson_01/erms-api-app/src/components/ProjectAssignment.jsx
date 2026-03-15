import React, { useState } from "react";

const ProjectAssignment = ({ projects, onAssign }) => {
  const [selectedProjectId, setSelectedProjectId] = useState("");

  const handleAssign = () => {
    if (!selectedProjectId) return;
    onAssign(Number(selectedProjectId));
    setSelectedProjectId("");
  };

  return (
    <div className="card mt-3">
      <div className="card-body">
        <h5 className="card-title">Assign Project</h5>

        <div className="row g-2 align-items-end">
          <div className="col-12 col-md-8">
            <label className="form-label">Select Project</label>
            <select
              className="form-select"
              value={selectedProjectId}
              onChange={(e) => setSelectedProjectId(e.target.value)}
            >
              <option value="">-- Choose a project --</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} {p.isActive ? "(Active)" : "(Inactive)"}
                </option>
              ))}
            </select>
          </div>

          <div className="col-12 col-md-4">
            <button
              className="btn btn-success w-100"
              onClick={handleAssign}
              disabled={!selectedProjectId}
            >
              Assign
            </button>
          </div>
        </div>

        <p className="text-muted mt-2 mb-0" style={{ fontSize: 12 }}>
          * This updates the employee’s assigned projects in shared state.
        </p>
      </div>
    </div>
  );
};

export default ProjectAssignment;
