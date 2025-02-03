#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pymongo import MongoClient, GEOSPHERE
from faker import Faker
import random
import datetime
from datetime import date, timedelta
from datetime import datetime, timedelta
import bson
import random

fake = Faker()

client = MongoClient('mongodb+srv://kharyalkashish3:Kashish0301@cluster0.hevoqie.mongodb.net/')
db = client['amazone']

customers_col = db['customers']
ratings_col = db['ratings']
customers_col = db['customers']
products_col = db['products']
orders_col = db['orders']
stores_col = db['stores']
warehouses_col = db['warehouses']
partners_col = db['partners']
payments_col = db['payments']


# ### 3. 1 query that indicates a customer ordering a product, adding it to the cart and making payment. 
# 

# In[3]:


import datetime
from pprint import pprint

# Create a payment collection
payments_col = db['payments']

# Step 1: Choose a random customer
specific_customer = customers_col.aggregate([{"$sample": {"size": 1}}]).next()

# Step 2: Select 2-3 random products
num_products = random.randint(2, 3)
random_products = list(products_col.aggregate([{"$sample": {"size": num_products}}]))

# Step 3: Add the selected products to the customer's cart with specified quantities
cart_items = [
    {
        "productID": product["_id"],
        "productName": product["productName"],  # Include product name for the invoice
        "quantity": random.randint(1, 5),
        "price": product["standardPrice"]
    }
    for product in random_products
]

# Step 4: Create an order for the selected products and customer with the chosen quantities
order_date = datetime.datetime.now()
order_items = [
    {"productID": item["productID"], "quantity": item["quantity"]} for item in cart_items
]
total_cost = sum(item["quantity"] * item["price"] for item in cart_items)

order = {
    "orderID": bson.ObjectId(),
    "customerID": specific_customer["_id"],
    "totalCost": total_cost,
    "orderDate": order_date,
    "status": "in transit",
    "orderItems": order_items
}
order_id = orders_col.insert_one(order).inserted_id

# Step 5: Make a payment for the created order
payment = {
    "paymentID": bson.ObjectId(),
    "customerID": specific_customer["_id"],
    "orderID": order_id,
    "amount": order["totalCost"],
    "paymentDate": order_date,
    "paymentMethod": random.choice(["Credit Card", "PayPal", "Bitcoin"]),
    "status": "completed"
}
payments_col.insert_one(payment)

# Step 6: Update the orders collection and the customer's current order section
customers_col.update_one(
    {"_id": specific_customer["_id"]},
    {"$push": {"currentOrders": order_id}}
)

# Print the invoice details
print("\nInvoice Details")
print("\nCustomer Name:", specific_customer["name"])
print("Order Date:", order_date.strftime("%Y-%m-%d %H:%M:%S"))
print("\nCart Items:")
for item in cart_items:
    print(f"Product: {item['productName']}, Quantity: {item['quantity']}, Price: ${item['price']:.2f}")

# Print the details of the order, cart, and payment
result = db.orders.aggregate([
    {
        '$match': {'_id': order_id}
    },
    {
        '$lookup': {
            'from': 'customers',
            'localField': 'customerID',
            'foreignField': 'customerID',
            'as': 'customerDetails',
        },
    },
    {
        '$lookup': {
            'from': 'payments',
            'localField': '_id',
            'foreignField': 'orderID',
            'as': 'paymentDetails',
        },
    },
    {
        '$project': {
            '_id': 1,
            'orderID': 1,
            'customerID': 1,
            'status': 1,
            'paymentDetails': {'$arrayElemAt': ['$paymentDetails', 0]},
        },
    },
])

# Print the result
pprint(result.next())

