import pandas as pd
import os

# create sample data
data = {
    'date': ['2025-01-12', '2025-01-12', '2025-01-13', '2025-01-15'],
    'product_id': ['Product1', 'Product2', 'Product1', 'Product3'],
    'quantity':[1, 3, 2, 7],
    'price':[9.49, 2.99, 9.49, 1.63],
    'cost':[5.03, 1.20, 5.03, 0.20]
}

df = pd.DataFrame(data)

# ensure that file is created inside "tests/data/" directory
output_path = os.path.join('tests', 'data', 'test_sales.csv')

df.to_csv(output_path, index=False)

print(f"CSV file created at: {output_path}")
