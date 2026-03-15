// Import the user service which contains business logic and database operations
const userService = require("../services/userService");

// =======================
// CREATE USER CONTROLLER
// =======================
const createUser = async (req, res) => {
  try {
    // Call service layer to create a new user using request body data
    const user = await userService.createUser(req.body);

    // Send HTTP 201 (Created) status with the created user as JSON
    res.status(201).json(user);
  } catch (error) {
    // Send HTTP 400 (Bad Request) if user creation fails
    res.status(400).json({ message: error.message });
  }
};

// =======================
// GET ALL USERS CONTROLLER
// =======================
const getUsers = async (req, res) => {
  try {
    // Call service layer to fetch all users from the database
    const users = await userService.getAllUsers();

    // Send the list of users as JSON response
    res.json(users);
  } catch (error) {
    // Send HTTP 500 (Internal Server Error) if something goes wrong
    res.status(500).json({ message: error.message });
  }
};

// =======================
// GET USER BY ID CONTROLLER
// =======================
const getUserById = async (req, res) => {
  try {
    // Call service layer to fetch a user using ID from request parameters
    const user = await userService.getUserById(req.params.id);

    // If user does not exist, return HTTP 404 (Not Found)
    if (!user) {
      return res.status(404).json({ message: "User not found" });
    }

    // Send the found user as JSON response
    res.json(user);
  } catch (error) {
    // Send HTTP 400 (Bad Request) if the ID is invalid or request fails
    res.status(400).json({ message: error.message });
  }
};

// =======================
// UPDATE USER CONTROLLER
// =======================
const updateUser = async (req, res) => {
  try {
    // Call service layer to update a user by ID using new data from request body
    const user = await userService.updateUser(req.params.id, req.body);

    // Send updated user details as JSON response
    res.json(user);
  } catch (error) {
    // Send HTTP 400 (Bad Request) if update fails
    res.status(400).json({ message: error.message });
  }
};

// =======================
// DELETE USER CONTROLLER
// =======================
const deleteUser = async (req, res) => {
  try {
    // Call service layer to delete a user using ID from request parameters
    await userService.deleteUser(req.params.id);

    // Send confirmation message after successful deletion
    res.json({ message: "User deleted" });
  } catch (error) {
    // Send HTTP 400 (Bad Request) if deletion fails
    res.status(400).json({ message: error.message });
  }
};

// Export all controller functions so they can be used in routes
module.exports = {
  createUser,
  getUsers,
  getUserById,
  updateUser,
  deleteUser
};
