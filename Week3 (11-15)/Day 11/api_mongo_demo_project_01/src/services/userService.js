// Import the User model to interact with the MongoDB users collection
const User = require("../models/usermodel");

// =======================
// CREATE USER SERVICE
// =======================
const createUser = async (data) => {
  // Create a new User document using the provided data
  const user = new User(data);

  // Save the user document to the database and return the saved user
  return await user.save();
};

// =======================
// GET ALL USERS SERVICE
// =======================
const getAllUsers = async () => {
  // Fetch and return all user documents from the database
  return await User.find();
};

// =======================
// GET USER BY ID SERVICE
// =======================
const getUserById = async (id) => {
  // Find and return a user document by its unique ID
  return await User.findById(id);
};

// =======================
// UPDATE USER SERVICE
// =======================
const updateUser = async (id, data) => {
  // Find a user by ID and update it with new data
  // { new: true } ensures the updated document is returned
  return await User.findByIdAndUpdate(id, data, { new: true });
};

// =======================
// DELETE USER SERVICE
// =======================
const deleteUser = async (id) => {
  // Find a user by ID and delete it from the database
  return await User.findByIdAndDelete(id);
};

// Export all service functions so they can be used in controllers
module.exports = {
  createUser,
  getAllUsers,
  getUserById,
  updateUser,
  deleteUser
};
