# Creates a fake data to test the visualization

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
np.random.seed(42)
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365)]

# Generate fake data
data = {
    'Date': dates,
    'Product': np.random.choice(['Widget A', 'Widget B', 'Widget C', 'Widget D'], 365),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 365),
    'Sales': np.random.randint(50, 500, 365).astype(float),  # Convert to float
    'Units': np.random.randint(1, 50, 365),
    'Customer_Satisfaction': np.random.uniform(3.0, 5.0, 365).round(2)
}

df = pd.DataFrame(data)

df['Revenue'] = df['Sales'] * df['Units']

df.loc[df['Date'].dt.month.isin([11, 12]), 'Sales'] *= 1.5  # Holiday season boost
df.loc[df['Date'].dt.dayofweek.isin([5, 6]), 'Sales'] *= 0.7  # Weekend dip

df.loc[df['Customer_Satisfaction'] > 4.5, 'Sales'] *= 1.2 
numeric_columns = ['Sales', 'Units', 'Customer_Satisfaction', 'Revenue']
df[numeric_columns] = df[numeric_columns].astype(float)
excel_file = 'fake_sales_data.xlsx'
df.to_excel(excel_file, index=False)

print(f"Fake sales data has been generated and saved to {excel_file}")
print(df.head())
print(df.info())