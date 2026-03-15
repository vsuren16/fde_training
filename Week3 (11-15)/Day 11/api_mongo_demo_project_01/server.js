// Import the Express app instance from the app.js file
const app = require("./app");

// Import the database connection function from the config/db file
const connectDB = require("./src/config/db");

// Define the port number on which the server will run
const PORT = 3000;

// Call the function to establish a connection with the database
connectDB();

// Start the Express server and listen for incoming requests on the given port
app.listen(PORT, () => {
  // Log a message to the console once the server starts successfully
  console.log(`Server running on http://localhost:${PORT}`);
});
