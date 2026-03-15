import React from "react";
import { BrowserRouter } from "react-router-dom";

import AppRoutes from "./routes/route";
import AuthProvider from "./context/AuthContext";
import DataProvider from "./context/DataContext";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <DataProvider>
          <AppRoutes />
        </DataProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
