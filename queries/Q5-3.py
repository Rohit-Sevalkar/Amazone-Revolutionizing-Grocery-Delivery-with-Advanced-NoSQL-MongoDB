from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import bson

client = MongoClient('mongodb+srv://rsevalkar2002:rohit1234567@cluster0.xz2soun.mongodb.net/')
db = client['amazone']


# Using 'orders' collection
top_customers_query = [
    {
        '$group': {
            '_id': '$customerID',
            'totalPurchases': {'$sum': '$totalCost'}
        }
    },
    {
        '$sort': {'totalPurchases': -1}
    },
    {
        '$limit': 5
    }
]


# Execute the query
top_customers_result = list(db.orders.aggregate(top_customers_query))


# Convert the result to a Pandas DataFrame
top_customers_df = pd.DataFrame(top_customers_result)
top_customers_df.set_index('_id', inplace=True)


# Visualize top customers with the highest total purchases
top_customers_df.plot(kind='bar', title='Top 5 Customers with the Highest Total Purchases')
plt.xlabel('Customer ID')
plt.ylabel('Total Purchases')
plt.show()
