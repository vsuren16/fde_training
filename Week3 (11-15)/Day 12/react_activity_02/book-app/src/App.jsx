import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Books from "./pages/Books";
import Header from "./components/Header";
import Footer from "./components/Footer";

function ProtectedRoute({ children }) {
  const isAuth = localStorage.getItem("loggedIn");
  return isAuth ? children : <Navigate to="/" />;
}

function App() {
  return (
    <BrowserRouter>
      <Header />
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route
            path="/books"
            element={
              <ProtectedRoute>
                <Books />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
      <Footer />
    </BrowserRouter>
  );
}

export default App;