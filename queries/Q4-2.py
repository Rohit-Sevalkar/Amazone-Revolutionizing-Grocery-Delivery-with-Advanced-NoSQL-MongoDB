#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# ### 1 Query indicating a manager checking sales and performance using pandas and matplotlib

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt

# Query to get monthly sales trend
monthly_sales_query = [
    {
        "$group": {
            "_id": {
                "$dateToString": {
                    "format": "%Y-%m",
                    "date": "$orderDate"
                }
            },
            "totalSales": {"$sum": "$totalCost"}
        }
    },
    {
        "$project": {
            "month": "$_id",
            "totalSales": 1,
            "_id": 0
        }
    },
    {
        "$sort": {"month": 1}
    }
]

monthly_sales_result = list(db.orders.aggregate(monthly_sales_query))

# Visualize the result using Pandas
df_monthly_sales = pd.DataFrame(monthly_sales_result)
print(df_monthly_sales)

# Line chart
df_monthly_sales.plot(x='month', y='totalSales', marker='o',color='red')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()


#_________________________________________________________________________________

# Query to get total sales per product category
total_sales_per_category_query = [
    {
        "$unwind": "$orderItems"
    },
    {
        "$lookup": {
            "from": "products",
            "localField": "orderItems.productID",
            "foreignField": "_id",
            "as": "productDetails"
        }
    },
    {
        "$unwind": "$productDetails"
    },
    {
        "$group": {
            "_id": "$productDetails.productCategory",
            "totalSales": {"$sum": {"$multiply": ["$orderItems.quantity", "$productDetails.standardPrice"]}}
        }
    }
]

total_sales_per_category_result = list(db.orders.aggregate(total_sales_per_category_query))

# Visualize the result using Pandas
df_total_sales_per_category = pd.DataFrame(total_sales_per_category_result)
print("Total Sales per Product Category:")
print(df_total_sales_per_category)

# Bar chart for total sales per product category
plt.bar(df_total_sales_per_category['_id'], df_total_sales_per_category['totalSales'])
plt.title('Total Sales price per Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')
plt.show()


#________________________________________________________________________

import pandas as pd
import matplotlib.pyplot as plt

# Query to get total sales per main category
total_sales_per_category_query = [
    {
        "$unwind": "$orderItems"
    },
    {
        "$group": {
            "_id": "$orderItems.productID",
            "totalQuantity": {"$sum": "$orderItems.quantity"}
        }
    },
    {
        "$lookup": {
            "from": "products",
            "localField": "_id",
            "foreignField": "_id",
            "as": "productDetails"
        }
    },
    {
        "$unwind": "$productDetails"
    },
    {
        "$group": {
            "_id": "$productDetails.mainCategory",
            "totalSales": {"$sum": {"$multiply": ["$totalQuantity", "$productDetails.standardPrice"]}}
        }
    }
]

total_sales_per_category_result = list(db.orders.aggregate(total_sales_per_category_query))

# Visualize the result using Pandas
df_total_sales_per_category = pd.DataFrame(total_sales_per_category_result)
print("Total Sales per MainCategory:")
print(df_total_sales_per_category)

# Pie chart for total sales per mainCategory
df_total_sales_per_category.plot.pie(y='totalSales', labels=df_total_sales_per_category['_id'], autopct='%1.1f%%')
plt.title('Total Sales per MainCategory')
plt.show()


# In[ ]:




