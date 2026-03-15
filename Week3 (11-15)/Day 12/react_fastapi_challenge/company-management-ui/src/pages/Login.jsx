import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

 // Async function to handle login form submission
async function login(e) {
  // Prevent default form submit (page reload)
  e.preventDefault();

  // Clear any previous error message
  setError("");

  // Enable loading state (used to disable button / show spinner)
  setLoading(true);

  try {
    // ✅ Send login credentials as JSON (NOT FormData)
    // Backend expects JSON body: { username, password }
    const res = await api.post("/auth/login", {
      username,
      password,
    });

    // ✅ Store JWT access token in localStorage
    // This token will be sent automatically in future API requests
    localStorage.setItem("token", res.data.access_token);

    // Optional: store token type (usually "bearer")
    localStorage.setItem("token_type", res.data.token_type);

    // Redirect user to dashboard after successful login
    navigate("/dashboard");

  } catch (err) {
    // If backend returns 401 → invalid credentials
    if (err.response?.status === 401) {
      setError("Invalid username or password");
    } 
    // Any other error (server down, network issue, etc.)
    else {
      setError("Something went wrong. Please try again.");
    }
  } finally {
    // Stop loading state whether login succeeds or fails
    setLoading(false);
  }
}

  return (
    <div className="card p-4 col-md-4 mx-auto mt-5">
      <h3 className="mb-3 text-center">Login</h3>

      {error && (
        <div className="alert alert-danger py-2">
          {error}
        </div>
      )}

      <form onSubmit={login}>
        <input
          className="form-control mb-3"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          type="password"
          className="form-control mb-3"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          className="btn btn-primary w-100"
          disabled={loading}
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
}

export default Login;