const userModel = require("../models/userModel");

// GET all users
function getAllUsers() {
  return userModel.getUsers();
}

// GET user by id
function getUserById(id) {
  const user = userModel.getUserById(id);
  if (!user) {
    throw new Error("User not found");
  }
  return user;
}

// CREATE user
function createUser(id, name) {
  if (!id || !name) {
    throw new Error("Invalid input");
  }

  const existingUser = userModel.getUserById(id);
  if (existingUser) {
    throw new Error("User already exists");
  }

  const user = { id, name };
  return userModel.addUser(user);
}

// UPDATE user
function updateUser(id, name) {
  const updatedUser = userModel.updateUser(id, { name });
  if (!updatedUser) {
    throw new Error("User not found");
  }
  return updatedUser;
}

// DELETE user
function deleteUser(id) {
  const deletedUser = userModel.deleteUser(id);
  if (!deletedUser) {
    throw new Error("User not found");
  }
  return deletedUser;
}

module.exports = {
  getAllUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser
};
