const express = require("express");
const userRoutes = require("./src/routes/userRoutes");

const app = express();

// Middleware to parse JSON requests
app.use(express.json()); //use add middleware 

// Register routes
app.use("/users", userRoutes);

// Default route (optional – for testing)
app.get("/", (req, res) => {
  res.send("User API is running");
});

module.exports = app;
