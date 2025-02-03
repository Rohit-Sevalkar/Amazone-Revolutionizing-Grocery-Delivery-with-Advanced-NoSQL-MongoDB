# Amazone and Morrizon Online Grocery Delivery Service

## Project Overview

This project involves designing a NoSQL database and schema for a joint online grocery delivery service by **Amazone** and **Morrizon**, a UK-based grocery chain. The system introduces immediate delivery services in Manchester, supporting varied business models and functioning smoothly across six Morrizon locations. The database is designed to handle customer orders, product inventory, store locations, delivery partners, and more, ensuring efficient data storage and rapid query processing.

## Key Features

- **NoSQL Schema Design**: The MongoDB schema is designed to prioritize effective data storage and rapid query processing. It uses both embedding and referencing techniques and integrates a geospatial index in the Stores collection for enhanced location-based search capabilities.
  
- **Entity-Relationship Diagram (ERD)**: The ERD was crafted using Lucidchart, providing a graphical depiction of the database architecture.

- **Data Population**: The `faker` library was used to generate realistic testing data, including customer names, addresses, product details, and more.

- **Geospatial Query**: A pipeline query was engineered to retrieve fresh products from proximate stores using `$geoNear` for geospatial indexing, complemented by `$lookup` and `$unwind` for pulling in-depth grocery information.

- **Inventory and Sales Queries**: Queries were formulated to detect products with dwindling stock and to evaluate sales efficacy by category using several aggregation processes such as `$unwind`, `$lookup`, `$match`, and `$group`.

- **Customer Orders**: Random existing and historical orders were created for customers, and the Customers collection was updated with these order specifics.

- **Partners Collection**: Scripts were developed to determine total revenue and delivery numbers for partners, and these figures were updated in the Partners collection.

## Database Schema

The database consists of the following collections:

- **Customers**: Stores customer information, including past and current orders, recommended products, and ratings.
- **Products**: Contains product details such as name, category, price, inventory levels, and customer ratings.
- **Orders**: Tracks customer orders, including order items, total cost, and status.
- **Stores**: Stores information about Morrizon store locations, including available grocery items and geospatial data.
- **Warehouses**: Contains information about warehouse locations and stored products.
- **Partners**: Tracks delivery partners, their current location, status, and delivery statistics.
- **Ratings**: Stores customer ratings for products, including scores and comments.
- **Payments**: Tracks payment details for orders, including payment method and status.

## Data Population

The database was populated with realistic data using the `faker` library. Key data points include:

- **Customers**: At least 20 customers, each with at least 2 current orders and 5 past orders.
- **Products**: At least 10 product samples for each product category (books, CDs, mobile phones, home appliances) and 5 fresh products from each fresh product category.
- **Stores**: At least 5 store locations for fresh product pickup and delivery.
- **Partners**: At least 5 delivery partners for instant pickup and delivery.
- **Ratings**: Each customer has rated at least 3 products, and each product has been rated by at least 2 customers.

## Queries and Aggregations

Several queries were implemented to analyze the data:

1. **Geospatial Query**: Retrieve fresh products from proximate stores using geospatial indexing.
2. **Inventory Query**: Detect products with low stock levels.
3. **Sales Query**: Evaluate sales efficacy by category.
4. **Customer Orders**: Retrieve customer orders and update the Customers collection.
5. **Partner Statistics**: Calculate total revenue and delivery numbers for partners.

## Installation & Usage

### Requirements

- Python 3.9
- MongoDB
- Libraries: `pymongo`, `faker`, `bson`, `datetime`, `random`

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/amazone-morrizon.git
   cd amazone-morrizon