//Pipeline for Total sales per category

[
  {
    $unwind: {
      path: "$orderItems",
    },
  },
  {
    $lookup: {
      from: "products",
      localField: "orderItems.productID",
      foreignField: "_id",
      as: "productDetails",
    },
  },
  {
    $unwind: {
      path: "$productDetails",
    },
  },
  {
    $group: {
      _id: "$productDetails.productCategory",
      totalSales: {
        $sum: "$orderItems.quantity",
      },
    },
  },
  {
    $sort: {
      totalSales: -1,
    },
  },
]