export default function UserList() {
  const users = ["Alice", "Bob", "Charlie"];
  return (
    <ul className="list-group">
      {users.map((u, i) => (
        <li key={i} className="list-group-item">{u}</li>
      ))}
    </ul>
  );
}