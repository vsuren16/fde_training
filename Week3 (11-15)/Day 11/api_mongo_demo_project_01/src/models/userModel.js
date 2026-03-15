// Import the mongoose library to define schemas and models
const mongoose = require("mongoose");

// Create a schema that defines the structure of the User collection
const userSchema = new mongoose.Schema({
  // Name field for the user
  name: {
    // Data type of the name field
    type: String,

    // Makes the name field mandatory
    required: true
  },

  // Email field for the user
  email: {
    // Data type of the email field
    type: String,

    // Makes the email field mandatory
    required: true,

    // Ensures that each email value is unique in the database
    unique: true
  }
});

// Create and export the User model using the schema
// "User" is the model name and will map to the "users" collection in MongoDB
module.exports = mongoose.model("User", userSchema);
