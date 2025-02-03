from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

client = MongoClient('mongodb+srv://tanya1501:Tanya15@cluster0.9d2w2j9.mongodb.net/')
db = client['UDATA_AMAZONE']

products_col = db["products"]

# Assuming you have a 'products' collection with field 'dailyInventoryLevels'
inventory_query = [
    {
        '$unwind': '$dailyInventoryLevels'
    },
    {
        '$group': {
            '_id': {'productId': '$productID', 'date': '$dailyInventoryLevels.date'},
            'averageInventory': {'$avg': '$dailyInventoryLevels.inventoryQuantity'}
        }
    },
    {
        '$sort': {'_id': 1}
    }
]

# Execute the query
inventory_result = list(products_col.aggregate(inventory_query))

# Convert the result to a Pandas DataFrame
inventory_df = pd.DataFrame(inventory_result)
inventory_df[['productId', 'date']] = pd.DataFrame(inventory_df['_id'].tolist())
inventory_df['date'] = pd.to_datetime(inventory_df['date'])

# Pivot the DataFrame for plotting
pivot_df = inventory_df.pivot(index='productId', columns='date', values='averageInventory')

# Get product IDs with maximum and minimum inventory
max_inventory_product = pivot_df.idxmax(axis=0)
min_inventory_product = pivot_df.idxmin(axis=0)

# Plotting a grouped bar plot with different colors for max and min inventory
ax = pivot_df.plot(kind='bar', width=0.8, figsize=(12, 6))

# Highlighting max inventory with a different color
for date, product_id in max_inventory_product.iteritems():
    ax.get_legend().legendHandles[pivot_df.columns.get_loc(date)].set_color('red')

# Highlighting min inventory with a different color
for date, product_id in min_inventory_product.iteritems():
    ax.get_legend().legendHandles[pivot_df.columns.get_loc(date)].set_color('green')

plt.title('Inventory Performance for Products on Given Dates')
plt.xlabel('Product ID')
plt.ylabel('Average Inventory Quantity')
plt.legend(title='Date')
plt.show()
