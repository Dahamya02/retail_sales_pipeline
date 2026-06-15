from enum import nonmember

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

NUM_RECORDS = 1000

random.seed(42)
np.random.seed(42)

products = ["Laptop","Phone","Tablet","Headphones","Monitor","Keyboard","Mouse","Charger","Smartwatch","Speaker"]
cities = ["Colombo","Kandy","Galle","Jaffna","Negombo"]
Regions =  {
    "Colombo": "Western",
    "Negombo": "Western",
    "Kandy":   "Central",
    "Galle":   "Southern",
    "Jaffna":  "Northern"
}
price_map = {
    "Laptop":     1200,
    "Phone":       800,
    "Tablet":      500,
    "Headphones":  150,
    "Monitor":     350,
    "Keyboard":     80,
    "Mouse":        40,
    "Charger":      30,
    "Smartwatch":  250,
    "Speaker":     120
}
#sales will be dated across the whole year 2025
start_date =  datetime(2025, 1, 1)
rows = []

for i in range(1, NUM_RECORDS + 1):

    product = random.choice(products)
    city = random.choice(cities)
    quantity = random.randint(1,10)
    price = price_map[product]

#adding missing values(intentionally) to stimulate real world dirty data
    if random.random() < 0.03: #3% chance this order has no quantity
        quantity = None
    if  random.random() < 0.03: #3% chance this order has no price
        price = None

    rows.append({
        "OrderID" : f"ORD-{i:04d}",
        "Product" : product,
        "CustomerID" : f"CUST-{random.randint(100, 999)}",
        "Date" : (start_date + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d"),
        "Price" : price,
        "Quantity" :  quantity,
        "City" : city,
        "Region" : Regions[city]
    })
df = pd.DataFrame(rows)
os.makedirs("data", exist_ok=True)
df.to_csv("data/retail_sales_data.csv", index=False)

print(f"Dataset generated successfully")
print(f" Total rows : {len(df)}")
print(f" Total columns : {len(df.columns)}")
print(f" Missing values: {df.isnull().sum().sum()}")
print(f" File saved to : data/retail_sales.csv")

