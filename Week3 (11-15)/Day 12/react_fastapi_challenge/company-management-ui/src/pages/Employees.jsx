import { useEffect, useState } from "react";
import api from "../api/axios";

function Employees() {
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [name, setName] = useState("");
  const [departmentId, setDepartmentId] = useState("");

  // Fetch employees and departments when the component is first mounted
useEffect(() => {
  // Get all employees from backend API
  api.get("/employees")
    .then(res => {
      // Store employees data in state
      setEmployees(res.data);
    });

  // Get all departments from backend API
  api.get("/departments")
    .then(res => {
      // Store departments data in state
      setDepartments(res.data);
    });

  // Empty dependency array []
  // ➜ This effect runs only once when the component loads
}, []);

// Function to add a new employee
function addEmployee() {
  // Send POST request to backend to create a new employee
  api.post("/employees", {
    // Employee name from input field
    name,

    // Convert departmentId (string from dropdown) into number
    // Backend usually expects numeric IDs
    department_id: Number(departmentId)
  })
  .then(() => {
    // Clear input fields after successful creation
    setName("");
    setDepartmentId("");

    // Re-fetch employees list to show latest data
    api.get("/employees")
      .then(res => {
        // Update employees state with fresh data
        setEmployees(res.data);
      });
  });
}
  return (
    <div>
      <h2>Employees</h2>

      <input className="form-control mb-2"
        placeholder="Employee Name"
        value={name}
        onChange={e => setName(e.target.value)} />

      <select className="form-select mb-2"
        value={departmentId}
        onChange={e => setDepartmentId(e.target.value)}>
        <option value="">Select Department</option>
        {departments.map(d => (
          <option key={d.id} value={d.id}>{d.name}</option>
        ))}
      </select>

      <button className="btn btn-primary mb-3" onClick={addEmployee}>
        Add Employee
      </button>

      <ul className="list-group">
        {employees.map(e => (
          <li key={e.id} className="list-group-item">
            {e.name} — {e.department_name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Employees;