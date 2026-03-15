// In-memory data (acts like a database)
let users = [];

// GET all users
function getUsers() {
  return users;
}

// GET user by id
function getUserById(id) {
  return users.find(user => user.id === id);
}

// CREATE user
function addUser(user) {
  users.push(user);
  return user;
}

// UPDATE user
function updateUser(id, updatedData) {
  const user = users.find(user => user.id === id);
  if (user) {
    user.name = updatedData.name ?? user.name;
    return user;
  }
  return null;
}

// DELETE user
function deleteUser(id) {
  const index = users.findIndex(user => user.id === id);
  if (index !== -1) {
    return users.splice(index, 1)[0];
  }
  return null;
}

module.exports = {
  getUsers,
  getUserById,
  addUser,
  updateUser,
  deleteUser
};
