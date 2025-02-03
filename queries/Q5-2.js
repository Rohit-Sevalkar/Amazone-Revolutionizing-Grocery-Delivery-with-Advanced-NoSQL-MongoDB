//Filtering Morrizons stores with low stock level products ( <100 items)​

[
  {
    $unwind:
      
      {
        path: "$availableGroceryItems",
      },
  },
  {
    $lookup:
      
      {
        from: "products",
        localField:
          "availableGroceryItems.productID",
        foreignField: "_id",
        as: "productDetails",
      },
  },
  {
    $unwind:
      
      {
        path: "$productDetails",
      },
  },
  {
    $match:
      
      {
        "availableGroceryItems.stockLevel": {
          $lte: 100,
        },
      },
  },
  {
    $project:
      
      {
        storeID: "$storeID",
        productID:
          "$availableGroceryItems.productID",
        productName:
          "$productDetails.productName",
        stockLevel:
          "$availableGroceryItems.stockLevel",
      },
  },
  {
    $sort:
      
      {
        stockLevel: 1,
      },
  },
  {
    $limit:
      
      100,
  },
]