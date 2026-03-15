console.log(`Entered server.js`);
const app = require("./app");
const mongoose = require("mongoose");

const PORT = 3000;

mongoose.connect("mongodb://localhost:27017/order_db")
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("MongoDB connection error:", err));

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT} from server.js`);
});