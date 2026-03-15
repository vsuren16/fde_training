//routes
// GET all order
router.get("/", userController.getOrders);

//controller
// GET all orders
function getOrders(req, res) {
  try {
    const orders = userService.getAllOrders();
    res.json(orders);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
}

//service 
// GET all orders
function getAllOrders() {
  return userModel.getOrders();
}

//model
// GET all orders
function getAllOrders() {
  return users;
}