import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Welcome from "./pages/Welcome";
import UserList from "./pages/UserList";
import Counter from "./pages/Counter";
import Login from "./pages/Login";

export default function App() {
  return (
    <>
      <Header />
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<Welcome />} />
          <Route path="/users" element={<UserList />} />
          <Route path="/counter" element={<Counter />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
      <Footer />
    </>
  );
}