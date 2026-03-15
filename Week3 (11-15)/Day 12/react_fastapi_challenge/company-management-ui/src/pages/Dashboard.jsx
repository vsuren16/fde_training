import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Dashboard() {
  const [employeeCount, setEmployeeCount] = useState(0);
  const [departmentCount, setDepartmentCount] = useState(0);
  const navigate = useNavigate();

 // React hook that runs side effects in a functional component
useEffect(() => {
  // Call loadStats when the component is mounted
  // This is typically used to fetch data from an API
  loadStats();

  // Empty dependency array []
  // ➜ Means this effect runs ONLY ONCE
  // ➜ Similar to componentDidMount in class components
}, []);

  // Async function to load dashboard statistics (employees & departments)
async function loadStats() {
  try {
    // Fetch all employees from backend API
    const empRes = await api.get("/employees");

    // Fetch all departments from backend API
    const depRes = await api.get("/departments");

    // Update state with total number of employees
    // empRes.data is expected to be an array
    setEmployeeCount(empRes.data.length);

    // Update state with total number of departments
    // depRes.data is expected to be an array
    setDepartmentCount(depRes.data.length);

  } catch (err) {
    // Log error details for debugging purposes
    console.error("Failed to load dashboard data", err);

    //  If backend returns 401 (Unauthorized),
    // it means the JWT token is missing, invalid, or expired
    if (err.response?.status === 401) {
      // Remove invalid token from localStorage
      localStorage.removeItem("token");

      // Redirect user to login page
      // navigate comes from react-router-dom's useNavigate hook
      navigate("/login");
    }
  }
}
  function logout() {
    localStorage.removeItem("token");
    navigate("/login");
  }

  return (
    <div>
      <h2 className="mb-4">Dashboard</h2>

      {/* Summary Cards */}
      <div className="row mb-4">
        <div className="col-md-6">
          <div className="card text-bg-primary">
            <div className="card-body">
              <h5 className="card-title">Employees</h5>
              <h2>{employeeCount}</h2>
              <button
                className="btn btn-light mt-2"
                onClick={() => navigate("/employees")}
              >
                View Employees
              </button>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card text-bg-success">
            <div className="card-body">
              <h5 className="card-title">Departments</h5>
              <h2>{departmentCount}</h2>
              <button
                className="btn btn-light mt-2"
                onClick={() => navigate("/departments")}
              >
                View Departments
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="card p-3">
        <h5>Quick Actions</h5>
        <div className="d-flex gap-2 mt-2">
          <button
            className="btn btn-outline-primary"
            onClick={() => navigate("/employees")}
          >
            Manage Employees
          </button>

          <button
            className="btn btn-outline-success"
            onClick={() => navigate("/departments")}
          >
            Manage Departments
          </button>

          <button
            className="btn btn-outline-danger ms-auto"
            onClick={logout}
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;