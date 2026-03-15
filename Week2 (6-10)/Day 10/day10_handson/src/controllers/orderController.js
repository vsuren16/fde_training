console.log(`Entered orderController.js`);
const orderService = require("../services/orderService");

// GET all orders
async function getOrders(req, res) {
  try {
    const orders = await orderService.getAllOrders();
    res.json(orders);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
}

// GET order by id
async function getOrderById(req, res) {
  try {
    const id = req.params.id;
    const order = await orderService.getOrderById(id);
    if (!order) return res.status(404).json({ message: "Order not found" });
    res.json(order);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
}

// CREATE order
async function createOrder(req, res) {
  try {
    const order = await orderService.createOrder(req.body);
    res.status(201).json(order);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
}


module.exports = {
  getOrders,
  getOrderById,
  createOrder
};
