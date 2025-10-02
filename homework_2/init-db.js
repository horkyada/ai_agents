// MongoDB initialization script
// This runs when the container starts for the first time

db = db.getSiblingDB('homework2');

// Create products collection with sample data
db.products.insertMany([
  {
    _id: "1",
    title: "Wireless Bluetooth Headphones",
    description: "Over-ear noise-cancelling headphones with 20h battery life",
    category: "electronics",
    price: 99.99
  },
  {
    _id: "2",
    title: "Gaming Laptop",
    description: "High-performance laptop with RTX 3060 GPU and 16GB RAM",
    category: "computers",
    price: 1299.99
  },
  {
    _id: "3",
    title: "Smart Home Security Camera",
    description: "1080p WiFi indoor camera with motion detection and mobile alerts",
    category: "smart-home",
    price: 149.99
  },
  {
    _id: "4",
    title: "Fitness Tracker Watch",
    description: "Tracks steps, heart rate, and sleep with 7-day battery",
    category: "wearables",
    price: 199.99
  },
  {
    _id: "5",
    title: "Mechanical Keyboard",
    description: "RGB backlit mechanical keyboard with tactile switches",
    category: "accessories",
    price: 129.99
  }
]);

print("Sample products inserted successfully!");

// Create index for better query performance
db.products.createIndex({ "category": 1 });
db.products.createIndex({ "title": "text", "description": "text" });

print("Database initialization completed!");