import React from "react";

const Footer = () => {
  const currentYear = new Date().getFullYear();
  const appVersion = "v1.0.0";

  return (
    <footer className="bg-dark text-white text-center py-3 mt-auto">
      <div className="container">
        <small>
          © {currentYear} ERMS. All Rights Reserved.
        </small>
        <br />
        <small>Enterprise ERMS - {appVersion}</small>
      </div>
    </footer>
  );
};

export default Footer;
