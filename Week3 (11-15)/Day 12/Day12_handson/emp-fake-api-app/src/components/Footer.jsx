import React from "react";

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-dark text-white text-center py-3 mt-auto shadow-sm">
      <div className="container">
        <small>
          © {year} Employee Management Portal. All Rights Reserved.
        </small>
        <br />
        <small>Version 1.0.0</small>
      </div>
    </footer>
  );
};

export default Footer;
