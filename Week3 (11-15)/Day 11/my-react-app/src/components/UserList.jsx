import { useState } from "react";

function UserList() {
  const [users, setUsers] = useState([
    "Alice",
    "Bob",
    "Charlie"
  ]);

  const [newUser, setNewUser] = useState("");

  function addUser() {
    if (newUser.trim() === "") return;

    setUsers([...users, newUser]);
    setNewUser("");
  }

  return (
    <div>
      <h2>User List</h2>

      <input
        type="text"
        placeholder="Enter username"
        value={newUser}
        onChange={(e) => setNewUser(e.target.value)}
      />

      <button onClick={addUser}>Add User</button>

      <ul>
        {users.map((user, index) => (
          <li key={index}>{user}</li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;