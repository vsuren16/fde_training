import { useEffect, useState } from "react";
import { getEmployees } from "../services/employeeservice";
import EmployeeCard from "../components/EmployeeCard";

function EmployeeDirectory() {
  const [employees, setEmployees] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  const employeesPerPage = 9;

  // Fetch employees once on load (Axios inside service)
  useEffect(() => {
    getEmployees()
      .then((data) => setEmployees(data))
      .catch((err) => console.error(err));
  }, []);

  // Pagination logic
  const lastIndex = currentPage * employeesPerPage;
  const firstIndex = lastIndex - employeesPerPage;
  const currentEmployees = employees.slice(firstIndex, lastIndex);

  const totalPages = Math.ceil(employees.length / employeesPerPage);

  return (
    <div className="container my-4">
      <h2 className="mb-4">Employee Directory</h2>

      <div className="row">
        {currentEmployees.map((emp) => (
          <div className="col-md-4 mb-4" key={emp.id}>
            <EmployeeCard employee={emp} />
          </div>
        ))}
      </div>

      {/* Pagination */}
      <div className="d-flex justify-content-center">
        <nav>
          <ul className="pagination">
            {[...Array(totalPages)].map((_, index) => (
              <li
                key={index}
                className={`page-item ${currentPage === index + 1 ? "active" : ""}`}
              >
                <button
                  className="page-link"
                  onClick={() => setCurrentPage(index + 1)}
                >
                  {index + 1}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </div>
  );
}

export default EmployeeDirectory;
