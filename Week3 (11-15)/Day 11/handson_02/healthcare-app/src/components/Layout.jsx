import React from "react";
import { Outlet } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";

const Layout = () => {
  return (
    <div className="d-flex flex-column min-vh-100">
      <Header />

      <main className="container my-4 flex-grow-1">
        <div className="card shadow-sm p-4">
          <Outlet />
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Layout;
