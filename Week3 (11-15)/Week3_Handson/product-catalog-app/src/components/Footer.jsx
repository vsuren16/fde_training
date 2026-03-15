import React from "react";
import { Link } from "react-router-dom";

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-dark text-white text-center py-3 mt-auto shadow-sm">
      <div className="container d-flex flex-column gap-2">
        <small>
          © {year} Product Catalog App. All Rights Reserved.
        </small>
        <div>
          <Link to="/privacy" className="text-white text-decoration-none me-3">Privacy Policy</Link>
          <Link to="/contact" className="text-white text-decoration-none">Contact Us</Link>
        </div>
        <small>Version 1.0.0</small>
      </div>
    </footer>
  );
};

export default Footer;
