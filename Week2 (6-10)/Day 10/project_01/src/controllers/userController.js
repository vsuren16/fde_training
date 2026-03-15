const userService = require("../services/userService");

// GET all users
function getUsers(req, res) {
  try {
    const users = userService.getAllUsers();
    res.json(users);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
}

// GET user by id
function getUserById(req, res) {
  try {
    const id = parseInt(req.params.id);
    const user = userService.getUserById(id);
    res.json(user);
  } catch (error) {
    res.status(404).json({ message: error.message });
  }
}

// CREATE user
function createUser(req, res) {
  try {
    const { id, name } = req.body;
    const user = userService.createUser(id, name);
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
}

// UPDATE user
function updateUser(req, res) {
  try {
    const id = parseInt(req.params.id);
    const { name } = req.body;
    const updatedUser = userService.updateUser(id, name);
    res.json(updatedUser);
  } catch (error) {
    res.status(404).json({ message: error.message });
  }
}

// DELETE user
function deleteUser(req, res) {
  try {
    const id = parseInt(req.params.id);
    const deletedUser = userService.deleteUser(id);
    res.json(deletedUser);
  } catch (error) {
    res.status(404).json({ message: error.message });
  }
}

module.exports = {
  getUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser
};
