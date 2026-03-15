// Import the Express framework
const express = require("express");

// Import the CORS middleware to allow cross-origin requests
const cors = require("cors");

// Import user-related routes from the routes folder
const userRoutes = require("./src/routes/userRoutes");

// Create an Express application instance
const app = express();

// Enable CORS for all origins (allows frontend apps from other domains to access this API)
app.use(cors());

// Middleware to parse incoming JSON request bodies
// Converts JSON data into a JavaScript object available in req.body
app.use(express.json());

// Register user routes and prefix them with "/users"
// Example: GET /users, POST /users
app.use("/users", userRoutes);

// Default route (optional – used as a health check)
app.get("/", (req, res) => {
  // Send a simple response to confirm the API is running
  res.send("User API is running");
});

// Export the app so it can be used in another file (like server.js or index.js)
module.exports = app;
