import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import EmployeeDirectory from "./pages/employeeDirectorymployeeDirectory";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function NotFound() {
  return (
    <div className="text-center">
      <h2 className="mb-3">404 - Page Not Found</h2>
      <p className="text-muted">
        The page you are looking for does not exist.
      </p>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="d-flex flex-column min-vh-100">
        
        {/* Header */}
        <Header />

        {/* Main Content */}
        <div className="container my-4 flex-grow-1">
          <Routes>
            {/* Default Route */}
            <Route path="/" element={<Navigate to="/employees" replace />} />

            {/* Employee Directory */}
            <Route path="/employees" element={<EmployeeDirectory />} />

            {/* 404 */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>

        {/* Footer */}
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
