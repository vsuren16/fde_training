import React from "react";

const Footer = () => {
  return (
    <footer className="bg-dark text-white text-center py-3 mt-auto">
      <div className="container">
        <small>
          © {new Date().getFullYear()} Smart Healthcare Portal | Version 1.0
        </small>
      </div>
    </footer>
  );
};

export default Footer;
