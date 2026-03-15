import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import ProductDirectory from "./pages/Home";
import "bootstrap/dist/css/bootstrap.min.css";

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

function About() {
  return (
    <div className="text-center">
      <h2 className="mb-3">About Us</h2>
      <p>Welcome to the product catalog application.</p>
    </div>
  );
}

function PrivacyPolicy() {
  return (
    <div className="text-center">
      <h2 className="mb-3">Privacy Policy</h2>
      <p>This is a dummy privacy policy for the product catalog application.</p>
    </div>
  );
}

function ContactUs() {
  return (
    <div className="text-center">
      <h2 className="mb-3">Contact Us</h2>
      <p>Email: productcatalog@gmail.com</p>
      <p>Phone: +1 234 567 890</p>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="d-flex flex-column min-vh-100 w-100">
        
        {/* Header */}
        <Header />

        {/* Main Content */}
        <div className="container my-4 flex-grow-1">
          <Routes>
            {/* Default Route */}
            <Route path="/" element={<Navigate to="/Home" replace />} />

            {/* Product Directory */}
            <Route path="/Home" element={<ProductDirectory />} />
            <Route path="/products" element={<ProductDirectory />} />
            <Route path="/about" element={<About />} />
            <Route path="/privacy" element={<PrivacyPolicy />} />
            <Route path="/contact" element={<ContactUs />} />

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
