import pymongo
from pymongo import MongoClient, GEOSPHERE
from bson.objectid import ObjectId
import random
from datetime import datetime, timedelta
import math

def convert_address_to_lat_long(address):
    # Implement actual conversion logic here, using a geocoding service
    return {"latitude": -40.162534, "longitude": -10.842245}  # Example coordinates

def calculate_eta(distance_km):
    dt = datetime.now() + timedelta(hours=distance_km / 10)
    hours = dt.hour
    minutes = dt.minute
    if hours<=12:
        return str(hours)+":"+str(minutes)+" AM"
    else:
        return str(hours)+":"+str(minutes)+" PM"

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c

    return distance

# Connect to MongoDB
client = MongoClient('mongodb+srv://vedaantsingh:Od94I8lnqmigxBj2@cluster0.oqdckpj.mongodb.net/')
db = client['amazone']

customer = db.customers.aggregate([{"$sample": {"size": 1}}]).next()
customer_location = convert_address_to_lat_long(customer["address"])

fresh_product = db.products.find_one({"mainCategory": "Fresh"})

nearest_partner = db.partners.find({
    "currentLocation": {
        "$nearSphere": {
            "$geometry": {
                "type": "Point",
                "coordinates": [customer_location["longitude"], customer_location["latitude"]]
            }
        }
    },
    "status": "active"
}).sort("ratings", -1).limit(1)

if nearest_partner:
    partner = nearest_partner.next()
    distance = haversine(partner["currentLocation"]["coordinates"][0], partner["currentLocation"]["coordinates"][1], customer_location["latitude"], customer_location["longitude"])
    result = {
        "customer_id": customer["_id"],
        "product_ordered": fresh_product["productName"],
        "partner_name": partner["name"],
        "estimated_distance": str(distance) + " kms",
        "ETA": calculate_eta(distance),
        "product_cost": fresh_product["cost"],
        "product_cost_original": fresh_product["standardPrice"],
        "product_main_category": fresh_product["mainCategory"],
        "product_origin": fresh_product["countryOfOrigin"],
    }
    print(result)
else:
    print("No available partner found")