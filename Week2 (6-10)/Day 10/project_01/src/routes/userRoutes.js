const express = require("express");
const router = express.Router();
const userController = require("../controllers/userController");

// GET all users
router.get("/", userController.getUsers);

// GET user by id
router.get("/:id", userController.getUserById);

// CREATE user
router.post("/", userController.createUser);

// UPDATE user
router.put("/:id", userController.updateUser);

// DELETE user
router.delete("/:id", userController.deleteUser);

module.exports = router;
