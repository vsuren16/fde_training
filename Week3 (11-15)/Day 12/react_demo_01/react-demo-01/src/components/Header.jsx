import { Link } from "react-router-dom";

export default function Header() {
  return (
    <nav className="navbar navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">MyApp</Link>
        <div>
          <Link className="nav-link d-inline text-white" to="/">Home</Link>
          <Link className="nav-link d-inline text-white" to="/users">Users</Link>
          <Link className="nav-link d-inline text-white" to="/counter">Counter</Link>
          <Link className="nav-link d-inline text-white" to="/login">Login</Link>
        </div>
      </div>
    </nav>
  );
}