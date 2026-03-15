console.log(`Entered app.js`);
const express = require('express');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');
const orderRoutes = require("./src/routes/orderRoutes");
const cors = require("cors");

// Swagger configuration options
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Day 10 Hands-on API',
      version: '1.0.0',
      description: 'API Documentation for Node.js MongoDB App',
    },
    servers: [
      {
        url: '/', // Relative path uses the current host (localhost or 127.0.0.1)
      },
    ],
  },
  // Path to the API docs (points to your route files)
  apis: ['./src/routes/*.js'], // OR ['./index.js'] if routes are in the main file
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);

const app = express();

// Enable CORS
app.use(cors());

// Serve Swagger UI
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// Middleware to parse JSON requests
app.use(express.json()); //use add middleware 

// Register routes
app.use("/orders", orderRoutes);

console.log(`orderRoutes registered in app.js`);

// Default route (optional – for testing)
app.get("/", (req, res) => {
  res.send("Order API is running");
});

// app.listen(3000, () => console.log('Server running on port 3000 from app.js'));

module.exports = app
