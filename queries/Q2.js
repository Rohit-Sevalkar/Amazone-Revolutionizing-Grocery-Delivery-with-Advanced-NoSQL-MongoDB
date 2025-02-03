//User searching for available fresh products. The products are displayed based on the user’s location. ​

[
  {
    $geoNear:
      {
        near: {
          type: "Point",
          coordinates: [53.4612, -2.1924],
        },
        distanceField: "distance",
        spherical: true,
      },
  },
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
        as: "product",
      },
  },
  {
    $unwind:
      
      {
        path: "$product",
      },
  },
  {
    $match:
      
      {
        "product.mainCategory": "Fresh",
      },
  },
  {
    $project:
      
      {
        storeID: 1,
        StoreAddress: "$address",
        productName: "$product.productName",
        price: "$product.cost",
        maincategory: "$product.mainCategory",
        subcategory: "$product.productCategory",
        AverageCustomerRating:
          "$product.averageCustomerRating",
      },
  },
]