const dbName = "ai_commerce";
db = db.getSiblingDB(dbName);

db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ user_id: 1 }, { unique: true });

db.products.createIndex({ product_id: 1 }, { unique: true });
db.products.createIndex({ category: 1 });

db.inventory.createIndex({ inventory_id: 1 }, { unique: true });
db.inventory.createIndex({ product_id: 1 }, { unique: true });

db.carts.createIndex({ cart_id: 1 }, { unique: true });
db.carts.createIndex({ user_id: 1 }, { unique: true });

db.cart_items.createIndex({ cart_item_id: 1 }, { unique: true });
db.cart_items.createIndex({ cart_id: 1, product_id: 1 }, { unique: true });

db.orders.createIndex({ order_id: 1 }, { unique: true });
db.orders.createIndex({ user_id: 1, order_date: -1 });

db.order_items.createIndex({ order_item_id: 1 }, { unique: true });
db.order_items.createIndex({ order_id: 1, product_id: 1 }, { unique: true });

db.search_history.createIndex({ search_id: 1 }, { unique: true });
db.search_history.createIndex({ user_id: 1, timestamp: -1 });
db.search_history.createIndex({ model_version: 1 });

if (db.products.countDocuments() === 0) {
  db.products.insertMany([
    {
      product_id: "P-101",
      title: "Reference Product 101",
      description: "Minimal product reference for inventory foreign-key validation in Milestone 1.",
      category: "reference",
      price: 0,
      rating: 0,
      embedding_vector: [],
      created_at: new Date().toISOString()
    },
    {
      product_id: "P-102",
      title: "Reference Product 102",
      description: "Minimal product reference for inventory foreign-key validation in Milestone 1.",
      category: "reference",
      price: 0,
      rating: 0,
      embedding_vector: [],
      created_at: new Date().toISOString()
    }
  ]);
}
