// Import the mongoose library to interact with MongoDB
const mongoose = require("mongoose");

// Define an asynchronous function to connect to the MongoDB database
const connectDB = async () => {
  try {
    // Attempt to connect to MongoDB using the connection URL
    // userdb is the name of the database
    await mongoose.connect("mongodb://127.0.0.1:27017/userdb");

    // Log success message if the database connection is established
    console.log("MongoDB connected");
  } catch (error) {
    // Log an error message if the database connection fails
    console.error("MongoDB connection failed:", error.message);

    // Exit the Node.js process with failure code (1)
    // This stops the application if the database is not connected
    process.exit(1);
  }
};

// Export the database connection function so it can be used in other files
module.exports = connectDB;
