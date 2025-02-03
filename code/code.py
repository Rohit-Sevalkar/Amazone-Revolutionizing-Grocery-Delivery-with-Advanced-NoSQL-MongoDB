#!/usr/bin/env python
# coding: utf-8

# 1. at least 20 customers. **(Done)**
# 2. at least 10 product samples for each product (book, CD, mobile phone, and home appliance). **(Done)**
# 3. at least 5 fresh products from each fresh product category. **(Done)**
# 4. at least 5 store locations for fresh products pickup and delivery **(Done)**
# 5. at least 5 partners for instant pickup and delivery
# 6. each customer has at least 2 current orders and at least 5 past orders. **(Done)**
# 7. each customer has rated at least 3 products; at least 2 customers have rated each product. **(Done)**
# 8. recommend each customer with at least 2 products. **(Done)**
# 9. only logs for 2 days of daily inventory levels are needed for each product. **(Done)**
# 10. at least one of the collections should be indexed for an efficient query. You are to decide which of the collections the index should be created and on which field. **(Done)**

from pymongo import MongoClient, GEOSPHERE
from faker import Faker
import random
import datetime
from datetime import date, timedelta
from datetime import datetime, timedelta
import bson
from bson.objectid import ObjectId
import random

fake = Faker()

client = MongoClient('mongodb+srv://vedaantsingh:Od94I8lnqmigxBj2@cluster0.oqdckpj.mongodb.net/')
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

#### Products

products_col.create_index([('productName', 1)])

def generate_inventory_levels(warehouse_locations):
    inventory_levels = []
    quantity = fake.random_number(digits=3)
    date = fake.date_between(start_date='today', end_date='today')
    for i in range(2):
        quantity = quantity - 2
        date = date + timedelta(days=i)
        inventory_levels.append({
            'date': str(date),
            'inventoryQuantity': quantity,
            'warehouseLocation': {"warehouseName": warehouse_locations[0]}
        })
    return inventory_levels

def generate_product_data(product_info, category, warehouse_locations):
    product_data = {
        'productID': bson.ObjectId(),
        'productName': product_info["productName"].split('by')[0] if 'by' in product_info["productName"] else product_info["productName"],
        'shortDescription': product_info["shortDescription"],
        'productDimensions': f"{fake.random_number(digits=2)} x {fake.random_number(digits=2)} x {fake.random_number(digits=2)} cm",
        'productWeight': fake.random_number(digits=3),
        'mainCategory': 'Other' if category in ["Book","CD","Mobile Phone","Home Appliance"] else 'Fresh',
        'productCategory': category,
        'expiryDate': str(fake.date_between(start_date='-2y', end_date='+1y')) if category == 'Fresh' else None,
        'countryOfOrigin': fake.country(),
        'averageCustomerRating': round(random.uniform(1, 5), 1),
        'standardPrice': product_info["price"] + round(random.uniform(1, 5), 2),
        'cost': product_info["price"],
        'dailyInventoryLevels': generate_inventory_levels(warehouse_locations)
    }

    if category == "Book":
        product_data.update({
            'authorName': product_info["authorName"],
            'publisher': product_info["publisher"],
            'yearOfPublication': product_info["yearOfPublication"],
            'ISBN': str(fake.random_number(digits=13))
        })
    elif category == "CD":
        product_data.update({
            'artistName': product_info["artistName"],
            'publisher': product_info["publisher"]
        })
    elif category == "Mobile Phone":
        product_data.update({
            'brand': product_info["brand"],
            'model': product_info["model"],
            'color': product_info["color"],
            'features': product_info["features"]
        })
    elif category == "Home Appliance":
        product_data.update({
            'color': product_info['color'],
            'voltage': product_info['voltage'],
            'style': product_info['style']
        })

    return product_data

def generate_products(category, count, products, warehouse_locations):
    products_insert = [generate_product_data(product, category, warehouse_locations) for product in products[category][:count]]
    return products_insert

warehouse_locations = ['Amazon Warehouse Manchester']  # Example warehouse locations

products = {
    "Book": [
        {'productName': 'The Great Gatsby', 'price': 10.99, 'category': 'Book', 'shortDescription': 'A novel of wealth, lust, and betrayal set in the roaring 20s.', 'authorName': 'F. Scott Fitzgerald', 'publisher': "Charles Scribner's Sons", 'yearOfPublication': 1925},
        {'productName': 'To Kill a Mockingbird', 'price': 7.99, 'category': 'Book', 'shortDescription': 'A tale of race and injustice in the Deep South.', 'authorName': 'Harper Lee', 'publisher': 'J. B. Lippincott & Co.', 'yearOfPublication': 1960},
        {'productName': '1984', 'price': 8.99, 'category': 'Book', 'shortDescription': 'A dystopian novel about the dangers of totalitarianism.', 'authorName': 'George Orwell', 'publisher': 'Secker & Warburg', 'yearOfPublication': 1949},
        {'productName': 'Pride and Prejudice', 'price': 9.99, 'category': 'Book', 'shortDescription': 'A romantic novel of manners.', 'authorName': 'Jane Austen', 'publisher': 'T. Egerton, Whitehall', 'yearOfPublication': 1813},
        {'productName': 'The Catcher in the Rye', 'price': 12.99, 'category': 'Book', 'shortDescription': 'A story about the struggles of adolescence.', 'authorName': 'J.D. Salinger', 'publisher': 'Little, Brown and Company', 'yearOfPublication': 1951},
        {'productName': 'The Hobbit', 'price': 10.99, 'category': 'Book', 'shortDescription': 'A fantasy novel and prelude to The Lord of the Rings.', 'authorName': 'J.R.R. Tolkien', 'publisher': 'George Allen & Unwin', 'yearOfPublication': 1937},
        {'productName': 'Fahrenheit 451', 'price': 7.99, 'category': 'Book', 'shortDescription': 'A dystopian novel presenting a future American society where books are outlawed.', 'authorName': 'Ray Bradbury', 'publisher': 'Ballantine Books', 'yearOfPublication': 1953},
        {'productName': 'Jane Eyre', 'price': 9.99, 'category': 'Book', 'shortDescription': 'A novel following the emotions and experiences of its eponymous heroine.', 'authorName': 'Charlotte Brontë', 'publisher': 'Smith, Elder & Co.', 'yearOfPublication': 1847},
        {'productName': 'Moby Dick', 'price': 11.99, 'category': 'Book', 'shortDescription': 'A novel about the voyage of the whaling ship Pequod.', 'authorName': 'Herman Melville', 'publisher': 'Richard Bentley', 'yearOfPublication': 1851},
        {'productName': 'War and Peace', 'price': 13.99, 'category': 'Book', 'shortDescription': 'A novel that chronicles the French invasion of Russia.', 'authorName': 'Leo Tolstoy', 'publisher': 'The Russian Messenger', 'yearOfPublication': 1869}
    ],
    "CD": [
        {'productName': 'Thriller by Michael Jackson', 'price': 9.99, 'category': 'CD', 'shortDescription': 'The best-selling album of all time.', 'artistName': 'Michael Jackson', 'publisher': 'Epic Records'},
        {'productName': 'Back in Black by AC/DC', 'price': 8.99, 'category': 'CD', 'shortDescription': 'The second best-selling album of all time.', 'artistName': 'AC/DC', 'publisher': 'Atlantic Records'},
        {'productName': 'The Dark Side of the Moon by Pink Floyd', 'price': 11.99, 'category': 'CD', 'shortDescription': 'A concept album known for its sonic experimentation.', 'artistName': 'Pink Floyd', 'publisher': 'Harvest Records'},
        {'productName': 'The Bodyguard by Whitney Houston', 'price': 10.99, 'category': 'CD', 'shortDescription': 'The soundtrack album from the motion picture.', 'artistName': 'Whitney Houston', 'publisher': 'Arista Records'},
        {'productName': 'Rumours by Fleetwood Mac', 'price': 7.99, 'category': 'CD', 'shortDescription': 'An album that produced four U.S. Top 10 singles.', 'artistName': 'Fleetwood Mac', 'publisher': 'Warner Bros. Records'},
        {'productName': 'Abbey Road by The Beatles', 'price': 12.99, 'category': 'CD', 'shortDescription': 'The eleventh studio album by the English rock band.', 'artistName': 'The Beatles', 'publisher': 'Apple Records'},
        {'productName': 'Led Zeppelin IV by Led Zeppelin', 'price': 10.99, 'category': 'CD', 'shortDescription': 'One of the best-selling albums worldwide.', 'artistName': 'Led Zeppelin', 'publisher': 'Atlantic Records'},
        {'productName': 'Hotel California by Eagles', 'price': 9.99, 'category': 'CD', 'shortDescription': 'The fifth studio album by the American rock band.', 'artistName': 'Eagles', 'publisher': 'Asylum Records'},
        {'productName': 'The Wall by Pink Floyd', 'price': 11.99, 'category': 'CD', 'shortDescription': 'A rock opera that explores abandonment and isolation.', 'artistName': 'Pink Floyd', 'publisher': 'Harvest Records'},
        {'productName': 'Born in the U.S.A. by Bruce Springsteen', 'price': 8.99, 'category': 'CD', 'shortDescription': 'The seventh studio album by the American rock singer.', 'artistName': 'Bruce Springsteen', 'publisher': 'Columbia Records'}
    ],
    "Mobile Phone": [
        {'productName': 'iPhone 12 Pro Max', 'price': 1099.00, 'category': 'Mobile Phone', 'shortDescription': '5G capable phone with A14 Bionic chip.', 'brand': 'Apple', 'model': '12 Pro Max', 'color': 'Pacific Blue', 'features': 'Super Retina XDR display'},
        {'productName': 'Samsung Galaxy S21', 'price': 799.00, 'category': 'Mobile Phone', 'shortDescription': 'High-quality camera and display.', 'brand': 'Samsung', 'model': 'Galaxy S21', 'color': 'Phantom Gray', 'features': '8K video recording'},
        {'productName': 'Google Pixel 5', 'price': 699.00, 'category': 'Mobile Phone', 'shortDescription': 'Pure Android experience with excellent camera.', 'brand': 'Google', 'model': 'Pixel 5', 'color': 'Just Black', 'features': 'Water-resistant'},
        {'productName': 'OnePlus 9', 'price': 729.00, 'category': 'Mobile Phone', 'shortDescription': 'Fast and smooth performance.', 'brand': 'OnePlus', 'model': '9', 'color': 'Winter Mist', 'features': 'Hasselblad Camera for Mobile'},
        {'productName': 'Xiaomi Mi 11', 'price': 749.00, 'category': 'Mobile Phone', 'shortDescription': 'Top-tier performance at a competitive price.', 'brand': 'Xiaomi', 'model': 'Mi 11', 'color': 'Horizon Blue', 'features': '108MP triple camera'},
        {'productName': 'Sony Xperia 1 II', 'price': 1199.00, 'category': 'Mobile Phone', 'shortDescription': 'Designed for speed with a professional camera.', 'brand': 'Sony', 'model': 'Xperia 1 II', 'color': 'Black', 'features': '4K HDR OLED display'},
        {'productName': 'Motorola Edge Plus', 'price': 999.00, 'category': 'Mobile Phone', 'shortDescription': 'Immersive display with Endless Edge screen.', 'brand': 'Motorola', 'model': 'Edge Plus', 'color': 'Thunder Grey', 'features': '108 MP sensor camera'},
        {'productName': 'LG V60 ThinQ', 'price': 899.00, 'category': 'Mobile Phone', 'shortDescription': 'Best for multitasking with dual screen option.', 'brand': 'LG', 'model': 'V60 ThinQ', 'color': 'Classy Blue', 'features': '32-bit Hi-Fi Quad DAC'},
        {'productName': 'ASUS ROG Phone 5', 'price': 999.00, 'category': 'Mobile Phone', 'shortDescription': 'Gaming powerhouse with advanced cooling.', 'brand': 'ASUS', 'model': 'ROG Phone 5', 'color': 'Phantom Black', 'features': '144 Hz display refresh rate'},
        {'productName': 'Huawei P40 Pro', 'price': 899.00, 'category': 'Mobile Phone', 'shortDescription': 'Visionary photography with Ultra Vision Leica.', 'brand': 'Huawei', 'model': 'P40 Pro', 'color': 'Silver Frost', 'features': '50x SuperSensing Zoom'}
    ],
    "Home Appliance": [
        {'productName': 'Dyson V11 Torque Drive', 'price': 599.99, 'category': 'Home Appliance', 'shortDescription': 'Intelligent cleaning with real-time reporting.', 'color': 'Nickel/Blue', 'voltage': 220, 'style': 'High Torque cleaner head'},
        {'productName': 'LG WM3900HWA Washer', 'price': 899.00, 'category': 'Home Appliance', 'shortDescription': 'Ultra-large capacity with AI Fabric sensor.', 'color': 'White', 'voltage': 110, 'style': 'SmartThinQ Technology'},
        {'productName': 'Samsung RF28R7351SG Refrigerator', 'price': 2799.00, 'category': 'Home Appliance', 'shortDescription': 'Modern design with a Food Showcase Door.', 'color': 'Black Stainless Steel', 'voltage': 110, 'style': 'FlexZone Drawer'},
        {'productName': 'KitchenAid KSM150PSER Artisan Stand Mixer', 'price': 379.00, 'category': 'Home Appliance', 'shortDescription': 'Make up to 9 dozen cookies in a single batch.', 'color': 'Empire Red', 'voltage': 110, 'style': '10-speed slide control'},
        {'productName': 'Instant Pot Duo 7-in-1 Electric Pressure Cooker', 'price': 89.00, 'category': 'Home Appliance', 'shortDescription': 'Multi-use programmable pressure cooker.', 'color': 'Stainless Steel', 'voltage': 110, 'style': '14 one-touch smart programs'},
        {'productName': 'iRobot Roomba 960', 'price': 499.99, 'category': 'Home Appliance', 'shortDescription': 'Robot vacuum with Wi-Fi Connectivity.', 'color': 'Graphite', 'voltage': 110, 'style': 'iAdapt 2.0 Navigation with vSLAM technology'},
        {'productName': 'Breville BES870XL Barista Express', 'price': 599.95, 'category': 'Home Appliance', 'shortDescription': 'Espresso machine with integrated grinder.', 'color': 'Brushed Stainless Steel', 'voltage': 110, 'style': 'Dose-Control Grinding'},
        {'productName': 'Philips HD9641/96 Airfryer', 'price': 249.95, 'category': 'Home Appliance', 'shortDescription': 'Healthy cooking with TurboStar Technology.', 'color': 'Black', 'voltage': 110, 'style': 'QuickClean basket'},
        {'productName': 'Bose QuietComfort 35 II', 'price': 299.00, 'category': 'Home Appliance', 'shortDescription': 'Wireless noise-cancelling headphones.', 'color': 'Silver', 'voltage': None, 'style': 'Alexa-enabled for voice access'},
        {'productName': 'Nest Learning Thermostat', 'price': 249.00, 'category': 'Home Appliance', 'shortDescription': 'Smart thermostat with HVAC monitoring.', 'color': 'Stainless Steel', 'voltage': None, 'style': 'Remote control through the app'}
    ],
    "Drinks": [
        {'productName': 'Pure Spring Water', 'price': 0.99, 'category': 'Drinks', 'shortDescription': 'Naturally filtered spring water.', 'volume': '500ml'},
        {'productName': 'Organic Apple Juice', 'price': 2.49, 'category': 'Drinks', 'shortDescription': 'Sweet and refreshing juice from organic apples.', 'volume': '1L'},
        {'productName': 'Fair Trade Coffee', 'price': 5.99, 'category': 'Drinks', 'shortDescription': 'Rich ground coffee with fair trade certification.', 'volume': '500g'},
        {'productName': 'Green Tea', 'price': 3.99, 'category': 'Drinks', 'shortDescription': 'Calming green tea with natural antioxidants.', 'volume': '100g'},
        {'productName': 'Chocolate Almond Milk', 'price': 3.49, 'category': 'Drinks', 'shortDescription': 'Deliciously smooth chocolate-flavored almond milk.', 'volume': '1L'},
    ],
    "Fruits and Vegetables": [
        {'productName': 'Organic Bananas', 'price': 0.29, 'category': 'Fruits', 'shortDescription': 'Rich in potassium and naturally sweet.', 'countryOfOrigin': 'Ecuador'},
        {'productName': 'Strawberries', 'price': 2.99, 'category': 'Fruits', 'shortDescription': 'Fresh and sweet strawberries perfect for desserts.', 'countryOfOrigin': 'Mexico'},
        {'productName': 'Navel Oranges', 'price': 1.99, 'category': 'Fruits', 'shortDescription': 'Seedless and packed with Vitamin C.', 'countryOfOrigin': 'Florida'},
        {'productName': 'Spinach', 'price': 1.99, 'category': 'Vegetables', 'shortDescription': 'Fresh spinach leaves rich in iron.', 'countryOfOrigin': 'USA'},
        {'productName': 'Tomatoes', 'price': 2.49, 'category': 'Vegetables', 'shortDescription': 'Ripe and juicy tomatoes for salads and sandwiches.', 'countryOfOrigin': 'Mexico'},
    ],
    "Bakery": [
        {'productName': 'Sourdough Bread', 'price': 3.99, 'category': 'Bakery', 'shortDescription': 'Crusty bread with a tangy flavor.', 'weight': '500g'},
        {'productName': 'Chocolate Chip Cookies', 'price': 2.49, 'category': 'Bakery', 'shortDescription': 'Soft cookies loaded with chocolate chips.', 'weight': '300g'},
        {'productName': 'Blueberry Muffins', 'price': 4.49, 'category': 'Bakery', 'shortDescription': 'Moist muffins with fresh blueberries.', 'weight': '400g'},
        {'productName': 'Croissants', 'price': 3.99, 'category': 'Bakery', 'shortDescription': 'Buttery and flaky French pastries.', 'weight': '350g'},
        {'productName': 'Bagels', 'price': 3.49, 'category': 'Bakery', 'shortDescription': 'Chewy bagels perfect for a cream cheese spread.', 'weight': '450g'},
    ]
}

categories = ["Book", "CD", "Mobile Phone", "Home Appliance", "Drinks", "Fruits and Vegetables", "Bakery"]
for category in categories:
    products_col.insert_many(generate_products(category, 10, products, warehouse_locations))

# products_col.delete_many({})


#### Customers

manchester_postcodes = [
    "M1 1AA", "M1 1AB", "M1 1AD", "M1 1AE", "M1 1AF", "M1 1AG",
    "M2 2AA", "M2 2AB", "M2 2AD", "M2 2AE", "M2 2AF", "M2 2AG",
    "M3 3AA", "M3 3AB", "M3 3AD", "M3 3AE", "M3 3AF", "M3 3AG",
    "M4 4AA", "M4 4AB", "M4 4AD", "M4 4AE", "M4 4AF", "M4 4AG",
]

manchester_streets = [
    "Oxford Street", "Deansgate", "Market Street", "Piccadilly", "Albert Square",
    "King Street", "Portland Street", "Princess Street", "Mosley Street", "St Ann's Square",
    "Castlefield", "Northern Quarter", "Ancoats", "Spinningfields", "Exchange Square",
    "Great Ducie Street", "Chepstow Street", "Peter Street", "Whitworth Street", "Chapel Street",
]

def generate_manchester_addresses():
    addresses = []

    separate_addresses = random.choice([True, False])

    if separate_addresses:
        addresses.append({
            "_id": bson.ObjectId(),
            "type": "Billing",
            "houseNumber": fake.building_number(),
            "street": random.choice(manchester_streets),
            "city": "Manchester",
            "postcode": random.choice(manchester_postcodes)
        })
        addresses.append({
            "_id": bson.ObjectId(),
            "type": "Shipping",
            "houseNumber": fake.building_number(),
            "street": random.choice(manchester_streets),
            "city": "Manchester",
            "postcode": random.choice(manchester_postcodes)
        })
    else:
        addresses.append({
            "_id": bson.ObjectId(),
            "type": "Billing/Shipping",
            "houseNumber": fake.building_number(),
            "street": random.choice(manchester_streets),
            "city": "Manchester",
            "postcode": random.choice(manchester_postcodes)
        })

    return addresses

def generate_customers(count):
    customers = []
    for _ in range(count):
        customers.append({
            'customerID': bson.ObjectId(),
            'name': fake.name(),
            'gender': random.choice(['Male', 'Female', 'Other']),
            'age': random.randint(18, 99),
            'address': generate_manchester_addresses(),
            'pastOrders': [],  # To be populated later
            'currentOrders': [],  # To be populated later
            'recommendedProducts': [],  # To be populated later
        })
    return customers

customers_col.insert_many(generate_customers(20))

# customers_col.delete_many({})

#### Ratings

customer_ids = [customer['customerID'] for customer in customers_col.find({}, {'customerID': 1, '_id': 0})]
product_ids = [product['productID'] for product in products_col.find({}, {'productID': 1, '_id': 0})]

customer_rating_percentage = 0.001  # 0.1%
product_rating_percentage = 0.01  # 1%

def generate_ratings(customerID, productID, score):
    return {
        'ratingID': bson.ObjectId(),
        'customerID': customerID,
        'productID': productID,
        'score': score,
        'comment': fake.sentence(),
        'ratingDate': str(fake.date_between(start_date='-1y', end_date='today'))
    }

ratings_batch = []

for product_id in product_ids:
    num_customer_ratings = max(1, int(len(customer_ids) * product_rating_percentage))
    customers_to_rate = random.sample(customer_ids, num_customer_ratings)
    for customer_id in customers_to_rate:
        score = random.randint(1, 5)  # Random score between 1 and 5
        rating = generate_ratings(customer_id, product_id, score)
        ratings_batch.append(rating)

ratings_col.insert_many(ratings_batch)

# ratings_col.delete_many({})

#### Updating Average Rating of Products

# Run after Ratings have been populated
ratings_col = db['ratings']
products_col = db['products']
def update_average_ratings():
    pipeline = [
        {
            "$group": {
                "_id": "$productID",
                "averageRating": {"$avg": "$score"}
            }
        }
    ]
   
    product_ratings = ratings_col.aggregate(pipeline)
    for product_rating in product_ratings:
        product_id = product_rating["_id"]
        average_rating = product_rating["averageRating"]


        products_col.update_one(
            {"productID": product_id},
            {"$set": {"averageCustomerRating": round(average_rating, 1)}}
        )

update_average_ratings()

#### Orders

# Function to create a random order for a customer
def create_order(customer_id, is_past_order=False):
    days_ago = random.randint(1, 365) if is_past_order else 0
    order_date = datetime.now() - timedelta(days=days_ago)
    status = "delivered" if is_past_order else "in transit"
    
    num_products = random.randint(1, 5)
    selected_products = products_col.aggregate([{"$sample": {"size": num_products}}])

    total_cost = 0
    order_items = []
    for product in selected_products:
        quantity = random.randint(1, 5)  # Random quantity for each product
        total_cost += product["standardPrice"] * quantity
        order_items.append({
            "productID": product["_id"],
            "quantity": quantity
        })

    return {
        "orderID": ObjectId(),
        "customerID": customer_id,
        "totalCost": total_cost,
        "orderDate": order_date,
        "status": status,
        "orderItems": order_items
    }

for customer in customers_col.find():
    current_orders = [create_order(customer["_id"]) for _ in range(random.randint(2, 10))]

    past_orders = [create_order(customer["_id"], True) for _ in range(random.randint(5, 200))]

    current_order_ids = [orders_col.insert_one(order).inserted_id for order in current_orders]
    past_order_ids = [orders_col.insert_one(order).inserted_id for order in past_orders]

    customers_col.update_one(
        {"_id": customer["_id"]},
        {
            "$set": {
                "currentOrders": current_order_ids,
                "pastOrders": past_order_ids
            }
        }
    )

# orders_col.delete_many({})


# ### Recommending 2 Products for each customer

def get_customer_preferences(customer_id):
    # Get ratings given by the customer
    customer_ratings = ratings_col.find({"customerID": customer_id})

    # Extract product IDs and corresponding ratings
    product_ratings = {rating["productID"]: rating["rating"] for rating in customer_ratings}

    return product_ratings


def recommend_products(customer_id, num_recommendations=2):
    customer_preferences = get_customer_preferences(customer_id)

    unrated_products = list(products_col.aggregate([
        {"$match": {"_id": {"$nin": list(customer_preferences.keys())}}},
        {"$sample": {"size": num_recommendations}}
    ]))

    unrated_products.sort(key=lambda x: x["averageCustomerRating"], reverse=True)

    recommendations = []
    for product in unrated_products[:num_recommendations]:
        recommendations.append({
            "productName": product["productName"],
            "price": product["standardPrice"],
            "category": product["productCategory"],
            "averageCustomerRating": product["averageCustomerRating"]
        })

    return recommendations

for customer in customers_col.find():
    customer_id = customer["_id"]

    recommendations = recommend_products(customer_id, num_recommendations=2)

    customers_col.update_one(
        {"_id": customer_id},
        {"$set": {"recommendedProducts": recommendations}}
    )


# ### Payment data for orders

# Function to generate payment data for orders
def generate_payments_for_orders(orders):
    payments = []

    for order in orders:
        # Check if "totalCost" is present in the order
        if "totalCost" in order:
            payment = {
                "paymentID": bson.ObjectId(),  # Generating a new ObjectId for paymentID
                "orderID": order["_id"],
                "amount": order["totalCost"],
                "paymentDate": order["orderDate"] + timedelta(minutes=random.randint(1, 59)),
                "paymentMethod": random.choice(["Credit Card", "PayPal", "Bitcoin"]),
                "status": "completed"
            }

            payments.append(payment)

    return payments

all_orders_cursor = orders_col.find()
all_orders = list(all_orders_cursor)

all_payments = generate_payments_for_orders(all_orders)

db.payments.insert_many(all_payments)


# ### Stores

# Insert sample data for 5 Morrizons stores
stores_data = [
    {
        "storeID": ObjectId(),
        "address": {
            "houseNumber": "25",
            "street": "Piccadilly Gardens",
            "city": "Manchester",
            "postcode": "M1 1LU"
        },
        "location": {
            "latitude": 53.4808,
            "longitude": -2.2426
        },
        "availableGroceryItems": []
    },
    {
        "storeID": ObjectId(),
        "address": {
            "houseNumber": "15",
            "street": "Grafton Street",
            "city": "Manchester",
            "postcode": "M13 9NU"
        },
        "location": {
            "latitude": 53.4612,
            "longitude": -2.1924
        },
        "availableGroceryItems": []
    },
    {
        "storeID": ObjectId(),
        "address": {
            "houseNumber": "40",
            "street": "Wilbraham Road",
            "city": "Manchester",
            "postcode": "M21 0UA"
        },
        "location": {
            "latitude": 53.4407,
            "longitude": -2.2726
        },
        "availableGroceryItems": []
    },
    {
        "storeID": ObjectId(),
        "address": {
            "houseNumber": "1",
            "street": "Lime Square",
            "city": "Manchester",
            "postcode": "M11 1ND"
        },
        "location": {
            "latitude": 53.4766,
            "longitude": -2.1843
        },
        "availableGroceryItems": []
    },
    {
        "storeID": ObjectId(),
        "address": {
            "houseNumber": "10",
            "street": "Poplar Street",
            "city": "Manchester",
            "postcode": "M35 0HY"
        },
        "location": {
            "latitude": 53.5095,
            "longitude": -2.1683
        },
        "availableGroceryItems": []
    }
]


stores_col.insert_many(stores_data)

# Function to get all grocery products
def get_grocery_products(products_col):
    grocery_categories = ["Fruits and Vegetables", "Drinks", "Bakery"]
    return list(products_col.find({"productCategory": {"$in": grocery_categories}}, {"_id": 1}))

# Function to randomly assign grocery items to a store
def assign_grocery_items_to_store(store_id, grocery_products, stores_col):
    selected_items = random.sample(grocery_products, random.randint(5, 15))  # Randomly select 5-15 items
    availableGroceryItems = [{"productID": item['_id'], "stockLevel": random.randint(10, 100)} for item in selected_items]
    
    stores_col.update_one(
        {"_id": store_id},
        {"$set": {"availableGroceryItems": availableGroceryItems}}
    )

# Main script
grocery_products = get_grocery_products(products_col)

for store in stores_col.find():
    assign_grocery_items_to_store(store['_id'], grocery_products, stores_col)

# stores_col.delete_many({})


# ### Warehouses

product_names = products_col.find({}, {"productName": 1, "_id": 0})
product_names_list = [product['productName'] for product in product_names]

warehouse_data = {
    "warehouseID": ObjectId(),
    "warehouseName": "Amazon Warehouse Manchester",
    "address": {
        "street": "Trafford Park",
        "city": "Manchester",
        "postcode": "M17 1TN",
        "country": "England"
    },
    "storedProducts": product_names_list
}

warehouses_col.insert_one(warehouse_data)

# warehouses_col.delete_many({})

# ### Partners

# Function to insert a new partner
def insert_partner(name, gender, age, status):
    new_partner = {
        "partnerID": ObjectId(),
        "name": name,
        "gender": gender,
        "age": age,
        "currentLocation": {
            "latitude": random.uniform(-90, 90),  # Random latitude
            "longitude": random.uniform(-180, 180)  # Random longitude
        },
        "status": status,
        "deliveryErrands": [],
        "deliveredItems": [],
        "statistics": {
            "totalDeliveries": 0,
            "totalEarnings": 0.0
        }
    }
    return partners_col.insert_one(new_partner).inserted_id

def assign_orders_to_partners():
    in_transit_orders = list(orders_col.find({"status": "in transit"}))

    active_partners = list(partners_col.find({"status": "active"}))

    for partner in active_partners:
        if in_transit_orders:
            selected_order = random.choice(in_transit_orders)
            in_transit_orders.remove(selected_order)

            partners_col.update_one(
                {"partnerID": partner["partnerID"]},
                {"$push": {"deliveryErrands": selected_order["orderID"]}}
            )

partner_names = ["John Doe", "Jane Smith", "Alex Johnson", "Maria Garcia", "Chris Brown"]
partner_genders = ["Male", "Female", "Male", "Female", "Male"]
partner_ages = [30, 28, 35, 32, 29]
partner_statuses = ["idle", "active", "idle", "active", "active"]

partner_ids = []
for name, gender, age, status in zip(partner_names, partner_genders, partner_ages, partner_statuses):
    partner_id = insert_partner(name, gender, age, status)
    partner_ids.append(partner_id)

partners_col.update_many({}, {"$set": {"deliveryErrands": []}})

assign_orders_to_partners()

delivered_orders = list(orders_col.find({"status": "delivered"}))
all_partners = list(partners_col.find({}))

for i, order in enumerate(delivered_orders):
    partner_index = i % len(all_partners)
    partner_id = all_partners[partner_index]["partnerID"]

    partners_col.update_one(
        {"partnerID": partner_id},
        {"$push": {"deliveredItems": {"orderID": order["orderID"], "deliveryDate": order["orderDate"]}}}
    )

for partner in partners_col.find():
    lat = partner['currentLocation']['latitude']
    lng = partner['currentLocation']['longitude']

    # Update the document with the new structure
    partners_col.update_one(
        {'_id': partner['_id']},
        {'$set': {'currentLocation': {'type': 'Point', 'coordinates': [lng, lat]}}}
    )

partners_col.create_index([("currentLocation", "2dsphere")])

# partners_col.delete_many({})

# ### Filling in the statistics of each Partner

# Calculate and update total earnings for each partner
for partner in all_partners:
    total_earnings = 0.0
    total_deliveries = 0

    for item in partner.get("deliveredItems", []):
        order = orders_col.find_one({"orderID": item["orderID"]})
        if order and order.get("status") == "delivered":
            earnings = 0.1 * order.get("totalCost", 0)  # 10% of the total cost
            total_earnings += earnings
            total_deliveries += 1

    partners_col.update_one(
        {"partnerID": partner["partnerID"]},
        {"$set": {"statistics.totalEarnings": total_earnings, "statistics.totalDeliveries": total_deliveries}}
    )
