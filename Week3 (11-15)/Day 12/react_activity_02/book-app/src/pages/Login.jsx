import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  function handleLogin(e) {
    e.preventDefault();
    if (username === "admin" && password === "admin123") {
      localStorage.setItem("loggedIn", "true");
      navigate("/books");
    } else {
      setError("Invalid credentials");
    }
  }

  return (
    <div className="container mt-5 col-md-4">
      <h3 className="text-center">Login</h3>
      {error && <p className="text-danger">{error}</p>}
      <form onSubmit={handleLogin}>
        <input className="form-control mb-2" placeholder="Username"
          onChange={(e) => setUsername(e.target.value)} />
        <input type="password" className="form-control mb-3" placeholder="Password"
          onChange={(e) => setPassword(e.target.value)} />
        <button className="btn btn-primary w-100">Login</button>
      </form>
    </div>
  );
}

export default Login;

