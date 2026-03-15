console.log(`Entered orderRoutes.js`);
const express = require("express");
const router = express.Router();
const orderController = require("../controllers/orderController");

// GET all orders
/**
 * @swagger
 * /orders:
 *   get:
 *     tags: [Orders]
 *     summary: Retrieve a list of orders
 *     responses:
 *       200:
 *         description: A list of orders.
 */
router.get("/", orderController.getOrders);

console.log(`Completed getOrders route in orderRoutes.js`);

// GET order by id
/**
 * @swagger
 * /orders/{id}:
 *   get:
 *     tags: [Orders]
 *     summary: Get a specific order by ID
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Order details
 */
router.get("/:id", orderController.getOrderById);

// CREATE order
/**
 * @swagger
 * /orders:
 *   post:
 *     tags: [Orders]
 *     summary: Create a new order
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               customerName:
 *                 type: string
 *               items:
 *                 type: array
 *                 items:
 *                   type: string
 *               totalAmount:
 *                 type: number
 *     responses:
 *       201:
 *         description: Order created successfully
 */
router.post("/", orderController.createOrder);

module.exports = router;
