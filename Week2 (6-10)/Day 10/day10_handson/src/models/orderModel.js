console.log(`Entered orderModel.js`);

const mongoose = require("mongoose");

const orderSchema = new mongoose.Schema({
  order_id: { type: Number, unique: true },
  _id: Number,
  customerName: { type: String, required: true },
  items: [String],
  totalAmount: Number,
  status: { type: String, default: "PLACED" },
  createdAt: { type: Date, default: Date.now }
}, { versionKey: false, collection: 'orders' });

orderSchema.pre("save", async function () {
  if (!this.isNew) return;
  const lastOrder = await this.constructor.findOne().sort({ _id: -1 });
  this._id = lastOrder && lastOrder._id ? lastOrder._id + 1 : 1;
  this.order_id = this._id;
});

module.exports = mongoose.model("Order", orderSchema);
