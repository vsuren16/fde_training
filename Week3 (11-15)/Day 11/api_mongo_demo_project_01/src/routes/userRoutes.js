// Import the Express framework
const express = require("express");

// Create a new router object to define modular routes
const router = express.Router();

// Import user controller functions that handle request logic
const userController = require("../controllers/userController");

// =======================
// CREATE USER ROUTE
// =======================
// Handles POST requests to /users
router.post("/", userController.createUser);

// =======================
// GET ALL USERS ROUTE
// =======================
// Handles GET requests to /users
router.get("/", userController.getUsers);

// =======================
// GET USER BY ID ROUTE
// =======================
// Handles GET requests to /users/:id
// :id is a dynamic route parameter
router.get("/:id", userController.getUserById);

// =======================
// UPDATE USER ROUTE
// =======================
// Handles PUT requests to /users/:id
router.put("/:id", userController.updateUser);

// =======================
// DELETE USER ROUTE
// =======================
// Handles DELETE requests to /users/:id
router.delete("/:id", userController.deleteUser);

// Export the router so it can be used in app.js
module.exports = router;
