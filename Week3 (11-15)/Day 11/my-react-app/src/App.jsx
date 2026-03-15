import Counter from "./components/Counter";
import Login from "./components/Login";
import UserList from "./components/UserList";
import Welcome from "./components/Welcome";

function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>React Basics Demo</h1>

      <Welcome name="Samatha" />

      <Counter />

      <Login />

      <UserList />
    </div>
  );
}

export default App;