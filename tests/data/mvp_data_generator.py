import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Services will become our products
products = {
    'P001': {'name': 'Basic Cut', 'price': 36, 'cost': 15},
    'P002': {'name': 'Mens Cut', 'price': 29, 'cost': 10},
    'P003': {'name': 'Color Base', 'price': 50, 'cost': 20},
    'P004': {'name': 'Balayage', 'price': 90, 'cost': 35},
    'P005': {'name': 'Styling', 'price': 41, 'cost': 15}
}

# Generate one year of data
data = {
    'date': [],
    'product_id': [],
    'quantity': [],
    'price': [],
    'cost': []
}

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
current_date = start_date

# Belgian holidays 2024 (we'll use these to add some patterns)
holidays = [
    '2024-01-01', '2024-04-01', '2024-05-01', '2024-05-09',
    '2024-05-20', '2024-07-21', '2024-08-15', '2024-11-01',
    '2024-11-11', '2024-12-25'
]

while current_date <= end_date:
    # Skip Sundays
    if current_date.weekday() == 6:
        current_date += timedelta(days=1)
        continue
    
    # Number of transactions for the day
    if current_date.strftime('%Y-%m-%d') in holidays:
        num_transactions = 0  # Closed on holidays
    elif current_date.weekday() in [4, 5]:  # Friday and Saturday
        num_transactions = np.random.randint(8, 15)  # Busier days
    else:
        num_transactions = np.random.randint(5, 10)  # Regular days
    
    # Generate transactions for the day
    for _ in range(num_transactions):
        # Add seasonal patterns
        month = current_date.month
        if month in [12, 1]:  # Winter holidays
            weights = [0.3, 0.2, 0.2, 0.1, 0.2]  # More basic cuts and styling
        elif month in [6, 7]:  # Summer
            weights = [0.2, 0.1, 0.2, 0.4, 0.1]  # More balayage
        else:
            weights = [0.25, 0.25, 0.2, 0.15, 0.15]  # Regular distribution
        
        # Select product
        product_id = np.random.choice(list(products.keys()), p=weights)
        product = products[product_id]
        
        # Most services have quantity=1, but some might buy products
        quantity = np.random.choice([1, 2], p=[0.9, 0.1])
        
        data['date'].append(current_date.strftime('%Y-%m-%d'))
        data['product_id'].append(product_id)
        data['quantity'].append(quantity)
        data['price'].append(product['price'])
        data['cost'].append(product['cost'])
    
    current_date += timedelta(days=1)

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('test_sales.csv', index=False)

# Print some basic statistics
print(f"Total transactions: {len(df)}")
print("\nProducts breakdown:")
print(df['product_id'].value_counts())
print("\nRevenue by month:")
df['month'] = pd.to_datetime(df['date']).dt.month
monthly_revenue = df.groupby('month').apply(
    lambda x: (x['price'] * x['quantity']).sum()
).round(2)
print(monthly_revenue)
