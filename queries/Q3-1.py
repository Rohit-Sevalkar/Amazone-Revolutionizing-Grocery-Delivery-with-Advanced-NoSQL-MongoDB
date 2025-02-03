from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import bson

client = MongoClient('mongodb+srv://tanya1501:Tanya15@cluster0.9d2w2j9.mongodb.net/')
db = client['UDATA_AMAZONE']


# Assuming you have 'customers', 'products', and 'orders' collections
customers_col = db["customers"]
products_col = db["products"]
orders_col = db["orders"]

# Function to simulate a customer ordering a product
def order_product(customer_id, product_id, quantity):
    # Retrieve customer and product information
    customer = customers_col.find_one({"_id": customer_id})
    product = products_col.find_one({"_id": product_id})

    if customer and product:
        # Simulate adding the product to the cart
        cart_item = {
            "_id": product["_id"],
            "quantity": quantity,
            "total_price": product["standardPrice"] * quantity
        }

        # Simulate making a payment
        payment_info = {
            "payment_method": "Credit Card",
            "amount_paid": cart_item["total_price"],
            "timestamp": datetime.utcnow()
        }

        # Create a new order document
        new_order = {
            
            "orderID": bson.ObjectId(),
            "customerID": customer["_id"],
            "totalCost": cart_item["total_price"],
            "order_date": payment_info["timestamp"],
            "status": "in-transit",
            "orderItems": {
                "productID":product["_id"],
                "quantity":quantity
            }

        }

        # Insert the new order into the 'orders' collection
        orders_col.insert_one(new_order)

        # Update customer's currentOrders
        customers_col.update_one(
            {"_id": customer["_id"]},
            {
                "$push": {
                    "currentOrders": cart_item["_id"]
                    },
                },
        )

        print(f"Order placed successfully for customer: {customer['name'],customer['customerID']}")
        print("\n")
        print(f"Product added to cart: {cart_item}")
        print("\n")
        print(f"Payment successful: {payment_info}")
        print("\n")
        print(f"Order added to 'orders' collection with the Order ID: {new_order['orderID']}")
        print("\n")
    else:
        print("Customer or product not found.")
        
random_customer = customers_col.aggregate([{ "$sample": { "size": 1 } }]).next()
random_product = products_col.aggregate([{ "$sample": { "size": 1 } }]).next()

# Simulate the customer ordering a product
order_product(random_customer["_id"], random_product["_id"], quantity=2)