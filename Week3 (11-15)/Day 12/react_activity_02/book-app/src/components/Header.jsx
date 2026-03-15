function Header() {
  function logout() {
    localStorage.removeItem("loggedIn");
    window.location.href = "/";
  }

  return (
    <nav className="navbar navbar-dark bg-dark px-3">
      <span className="navbar-brand">Book App</span>
      <button className="btn btn-danger" onClick={logout}>
        Logout
      </button>
    </nav>
  );
}

export default Header;
