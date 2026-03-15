console.log(`Entered orderService.js`);

const Order = require("../models/orderModel");

// Payment processing (Promise-Based)
const processPayment = (amount) => {
  return new Promise((resolve, reject) => {
    console.log(`Processing payment for amount: ${amount}`);
    setTimeout(() => {
      if (amount > 1000) {
        reject(new Error("Payment failed: Amount exceeds 1000"));
      } else {
        resolve("Payment successful");
      }
    }, 3000);
  });
};

// Simulation Helpers
const startCooking = () => {
  return new Promise((resolve) => setTimeout(resolve, 2000));
};

const assignDelivery = () => {
  return new Promise((resolve) => setTimeout(resolve, 2000));
};

const deliverOrder = () => {
  return new Promise((resolve) => setTimeout(resolve, 2000));
};

// GET all orders
async function getAllOrders() {
  return await Order.find();
}

// GET order by id
async function getOrderById(id) {
  return await Order.findById(id);
}

// CREATE order
async function createOrder(orderData) {
  // Event Loop Demonstration
  console.log("Order received");
  setTimeout(() => console.log("Timer completed"), 0); //Macrotask
  Promise.resolve().then(() => console.log("Promise resolved")); //Microtask ahead of macrotask
  console.log("Order processing started");

  const order = new Order(orderData);
  const savedOrder = await order.save();
  console.log(`Order ${savedOrder._id}: Status updated to PLACED`);

  try {
    // 2. Process Payment
    const paymentResult = await processPayment(savedOrder.totalAmount);
    console.log(paymentResult);
    savedOrder.status = "PAID";
    await savedOrder.save();
    console.log(`Order ${savedOrder._id}: Status updated to PAID`);

    // 3. Start Cooking
    await startCooking();
    savedOrder.status = "COOKING";
    await savedOrder.save();
    console.log(`Order ${savedOrder._id}: Status updated to COOKING`);

    // 4. Assign Delivery
    await assignDelivery();
    savedOrder.status = "OUT_FOR_DELIVERY";
    await savedOrder.save();
    console.log(`Order ${savedOrder._id}: Status updated to OUT_FOR_DELIVERY`);

    // 5. Deliver
    await deliverOrder();
    savedOrder.status = "DELIVERED";
    await savedOrder.save();
    console.log(`Order ${savedOrder._id}: Status updated to DELIVERED`);
  } 
    catch (error) {
    console.error(error.message);
    savedOrder.status = "FAILED";
    await savedOrder.save();
    console.log(`Order ${savedOrder._id}: Status updated to FAILED`);
  }
  return savedOrder;
}

module.exports = {
  getAllOrders,
  getOrderById,
  createOrder
};
