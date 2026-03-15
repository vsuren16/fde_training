import { useEffect, useState } from "react";
import api from "../api/axios";

function Departments() {
  const [departments, setDepartments] = useState([]);
  const [name, setName] = useState("");

 // Load departments when the component is first mounted
useEffect(() => {
  // Call backend API to fetch all departments
  api.get("/departments")
    .then(res => {
      // Update state with departments received from backend
      setDepartments(res.data);
    });

  // Empty dependency array []
  // ➜ This effect runs only once when the component loads
}, []);

// Function to add a new department
function addDepartment() {
  // Send POST request to backend with new department name
  api.post("/departments", { name })
    .then(() => {
      // Clear the input field after successful creation
      setName("");

      // Re-fetch the departments list
      // This ensures UI shows the latest data from backend
      api.get("/departments")
        .then(res => {
          // Update state with updated departments list
          setDepartments(res.data);
        });
    });
}

  return (
    <div>
      <h2>Departments</h2>

      <input
        className="form-control mb-2"
        placeholder="Department Name"
        value={name}
        onChange={e => setName(e.target.value)}
      />

      <button className="btn btn-success mb-3" onClick={addDepartment}>
        Add Department
      </button>

      <ul className="list-group">
        {departments.map(d => (
          <li key={d.id} className="list-group-item">{d.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default Departments;