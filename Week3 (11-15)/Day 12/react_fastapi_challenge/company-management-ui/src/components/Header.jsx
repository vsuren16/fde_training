import { Link } from "react-router-dom";

function Header() {
  return (
    <nav className="navbar navbar-dark bg-dark">
      <div className="container d-flex align-items-center">
        
        {/* LEFT SIDE */}
        <div className="d-flex align-items-center">
          <Link className="navbar-brand me-4" to="/dashboard">
            Company
          </Link>

          <Link className="nav-link text-light me-3" to="/employees">
            Employees
          </Link>

          <Link className="nav-link text-light" to="/departments">
            Departments
          </Link>
        </div>

        {/* RIGHT SIDE */}
        <div className="ms-auto">
          <Link className="nav-link text-light" to="/login">
            Login
          </Link>
        </div>

      </div>
    </nav>
  );
}

export default Header;